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


def normalized(text):
    return re.sub(r"[\s➜①②③❶❷❸❹]", "", unicodedata.normalize("NFC", text))


def require(condition, message):
    if not condition:
        raise ValueError(message)


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
    if args.pdf:
        import pymupdf
        with pymupdf.open(args.pdf) as pdf:
            require(1 <= args.page <= len(pdf), "PDF page out of range")
            lines = [line for line in pdf[args.page - 1].get_text().splitlines() if normalized(line)]
        missing = [line for line in lines if normalized(line) not in actual]
        print(f"PDF lines matched: {len(lines) - len(missing)}/{len(lines)}")
        if missing:
            print("Review unmatched lines (may include moved/split labels):")
            print("\n".join(missing))
            raise SystemExit(1)
    print("Visual verification in the target Hancom editor is still required.")


if __name__ == "__main__":
    main()
