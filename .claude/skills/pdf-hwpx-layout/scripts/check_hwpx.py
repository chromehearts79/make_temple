"""Check an HWPX package and, optionally, compare against PDF text lines."""

import argparse
from pathlib import Path, PurePosixPath
import re
import unicodedata
from zipfile import ZipFile

from lxml import etree as E

REQUIRED = {
    "mimetype", "version.xml", "settings.xml", "Contents/header.xml",
    "Contents/content.hpf", "Contents/section0.xml", "META-INF/container.xml",
    "META-INF/manifest.xml",
}


# Decorative glyphs a recipe may add between source lines; ignored when matching text.
DECORATIONS = r"[\s➜①-⑩❶-❾→▶▼■□▣◎]"


# Symbol-font private-use characters in PDF text and the KS X 1001 character the builder writes.
PUA_MAP = str.maketrans({"\uf09e": "·"})


def normalized(text):
    # Runs of "··" are TOC dot leaders; recipes draw them as a dotted cell border instead.
    text = re.sub(r"·{2,}", "", unicodedata.normalize("NFC", text).translate(PUA_MAP))
    return re.sub(DECORATIONS, "", text)


def unsafe_symbols(text):
    """Non-ASCII, non-Hangul characters outside KS X 1001 (not encodable as EUC-KR)."""
    seen = []
    for ch in text:
        if ord(ch) < 0x80 or "\uac00" <= ch <= "\ud7a3" or ch in seen:
            continue
        try:
            ch.encode("euc_kr")
        except UnicodeEncodeError:
            seen.append(ch)
    return seen


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_text(path):
    """All run text of the document sections, in order."""
    with ZipFile(path) as package:
        root = E.fromstring(package.read("Contents/content.hpf"),
                            E.XMLParser(resolve_entities=False, no_network=True))
        hrefs = {i.get("id"): i.get("href") for i in root.xpath('.//*[local-name()="item"]')}
        text = []
        for ref in root.xpath('.//*[local-name()="itemref"]'):
            href = hrefs[ref.get("idref")]
            if PurePosixPath(href).name.startswith("section"):
                section = E.fromstring(package.read(href), E.XMLParser(resolve_entities=False, no_network=True))
                text += section.xpath('.//*[local-name()="t"]/text()')
    return "".join(text)


def check(path):
    with ZipFile(path) as package:
        names = set(package.namelist())
        require(len(names) == len(package.namelist()), "Duplicate ZIP entries")
        require(REQUIRED <= names, f"Missing package files: {sorted(REQUIRED - names)}")
        require(package.testzip() is None, "Invalid ZIP CRC")
        require(package.read("mimetype") == b"application/hwp+zip", "Unexpected mimetype")
        trees = {name: E.fromstring(package.read(name), E.XMLParser(resolve_entities=False, no_network=True))
                 for name in names if name.endswith((".xml", ".hpf", ".rdf"))}
    content = trees["Contents/content.hpf"]
    manifest = content.xpath('.//*[local-name()="manifest"]/*[local-name()="item"]')
    paths = {item.get("id"): item.get("href") for item in manifest}
    require(all(p in names for p in paths.values()), f"Missing manifest target: {paths}")
    require(all(e.get("idref") in paths for e in content.xpath('.//*[local-name()="itemref"]')),
            "Broken spine reference")
    container = trees["META-INF/container.xml"]
    require(all(e.get("full-path") in names for e in container.xpath('.//*[@full-path]')),
            "Broken container reference")
    sections = [trees[paths[e.get("idref")]] for e in content.xpath('.//*[local-name()="itemref"]')
                if PurePosixPath(paths[e.get("idref")]).name.startswith("section")]
    require(bool(sections), "No document section in spine")
    for section in sections:
        for image in section.xpath('.//*[@binaryItemIDRef]'):
            require(image.get("binaryItemIDRef") in paths, "Broken image reference")
    chunks = [t for section in sections for t in section.xpath('.//*[local-name()="t"]/text()')]
    tables = sum(len(section.xpath('.//*[local-name()="tbl"]')) for section in sections)
    require(bool(normalized("".join(chunks))) or tables == 0, "Tables exist but all text is empty")
    print(f"Package OK. Sections: {len(sections)}. Tables: {tables}. Text characters: {sum(map(len, chunks))}.")
    return normalized("".join(chunks))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hwpx", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()
    actual = check(args.hwpx)
    unsafe = unsafe_symbols(read_text(args.hwpx))
    failed = False
    if args.pdf:
        import pymupdf
        with pymupdf.open(args.pdf) as pdf:
            require(1 <= args.page <= len(pdf), "PDF page out of range")
            source = pdf[args.page - 1].get_text()
            lines = [line for line in source.splitlines() if normalized(line)]
        missing = [line for line in lines if normalized(line) not in actual]
        print(f"PDF lines matched: {len(lines) - len(missing)}/{len(lines)}")
        if missing:
            print("Review unmatched lines (may include moved/split labels):")
            print("\n".join(missing))
            failed = True
        added = [ch for ch in unsafe if ch not in source]
        kept = [ch for ch in unsafe if ch in source]
        if kept:
            print("Note: source text has symbols outside KS X 1001, kept as-is: " + " ".join(kept))
        if added:
            print("Symbols outside KS X 1001 added by the recipe: " + " ".join(added))
            print("  Hancom draws them from a fallback font, so they drift. Use → ▶ ▼ ① ■ □ ▣ ◎ ※ instead.")
            failed = True
    elif unsafe:
        print("Warning: symbols outside KS X 1001: " + " ".join(unsafe))
    if failed:
        raise SystemExit(1)
    print("Visual verification in the target Hancom editor is still required.")


if __name__ == "__main__":
    main()
