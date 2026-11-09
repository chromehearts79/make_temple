"""Merge single-page HWPX files built with hwpx_layout into one multi-section document.

Each input becomes its own section (구역), so every page keeps its own page settings and starts
on a new page. Styles that a page added on top of the shared seed (border fills, character and
paragraph properties, fonts) are renumbered so they do not collide; seed styles are shared.

usage: python3 scripts/merge_hwpx.py merged.hwpx page1.hwpx page2.hwpx ...
"""

import argparse
from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree as E

SEED = Path(__file__).resolve().parents[1] / "assets" / "blank-layout-seed.zip"
NS = {
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "opf": "http://www.idpf.org/2007/opf/",
}
# (container in header.xml, attribute that references it)
GROUPS = [("borderFill", "hh:borderFills", "borderFillIDRef"),
          ("charPr", "hh:charProperties", "charPrIDRef"),
          ("paraPr", "hh:paraProperties", "paraPrIDRef")]
PARSER = E.XMLParser(resolve_entities=False, no_network=True)


def parse(blob):
    return E.fromstring(blob, PARSER)


def seed_limits():
    with ZipFile(SEED) as z:
        head = parse(z.read("Contents/header.xml"))
    limits = {key: max(int(e.get("id")) for e in head.find(f".//{tag}", NS)) for key, tag, _ in GROUPS}
    fonts = {f.get("lang"): max(int(x.get("id")) for x in f) for f in head.iterfind(".//hh:fontface", NS)}
    return limits, fonts


def merge_fonts(master, head, font_limits):
    """Map page-added fonts to the master's font of the same face, appending missing faces."""
    mapping = {}
    for family in head.iterfind(".//hh:fontface", NS):
        lang = family.get("lang")
        target = master.find(f".//hh:fontface[@lang='{lang}']", NS)
        faces = {f.get("face"): f.get("id") for f in target}
        mapping[lang] = {}
        for font in family:
            if int(font.get("id")) <= font_limits[lang]:
                continue
            if font.get("face") not in faces:
                new = deepcopy(font)
                new.set("id", str(max(int(f.get("id")) for f in target) + 1))
                target.append(new)
                target.set("fontCnt", str(len(target)))
                faces[font.get("face")] = new.get("id")
            mapping[lang][font.get("id")] = faces[font.get("face")]
    return mapping


def merge_styles(master, head, limits, font_map):
    maps = {}
    for key, tag, _ in GROUPS:
        source, target = head.find(f".//{tag}", NS), master.find(f".//{tag}", NS)
        maps[key] = {}
        for item in source:
            if int(item.get("id")) <= limits[key]:
                continue
            new = deepcopy(item)
            new.set("id", str(max(int(e.get("id")) for e in target) + 1))
            for el in new.iter():
                ref = el.get("borderFillIDRef")
                if ref in maps.get("borderFill", {}):
                    el.set("borderFillIDRef", maps["borderFill"][ref])
            if key == "charPr":
                font_ref = new.find("hh:fontRef", NS)
                for attr, value in font_ref.attrib.items():
                    lang = attr.upper()
                    if value in font_map.get(lang, {}):
                        font_ref.set(attr, font_map[lang][value])
            target.append(new)
            target.set("itemCnt", str(len(target)))
            maps[key][item.get("id")] = new.get("id")
    return maps


def remap_section(section, maps):
    for el in section.iter():
        for key, _, attr in GROUPS:
            value = el.get(attr)
            if value in maps[key]:
                el.set(attr, maps[key][value])


def validate(master, sections):
    known = {attr: {e.get("id") for e in master.find(f".//{tag}", NS)} for _, tag, attr in GROUPS}
    for number, section in enumerate(sections):
        for el in section.iter():
            for attr, ids in known.items():
                if el.get(attr) is not None and el.get(attr) not in ids:
                    raise ValueError(f"section{number}: dangling {attr}={el.get(attr)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("output", type=Path)
    ap.add_argument("inputs", type=Path, nargs="+")
    args = ap.parse_args()
    if args.output.suffix.lower() != ".hwpx":
        ap.error("Output path must end in .hwpx")
    limits, font_limits = seed_limits()

    with ZipFile(args.inputs[0]) as first:
        master = parse(first.read("Contents/header.xml"))
        content = parse(first.read("Contents/content.hpf"))
        sections = [parse(first.read("Contents/section0.xml"))]
    for path in args.inputs[1:]:
        with ZipFile(path) as z:
            head, section = parse(z.read("Contents/header.xml")), parse(z.read("Contents/section0.xml"))
        maps = merge_styles(master, head, limits, merge_fonts(master, head, font_limits))
        remap_section(section, maps)
        sections.append(section)
    validate(master, sections)

    # Object ids must be unique across the document.
    for number, table in enumerate((t for s in sections for t in s.iter(f"{{{NS['hp']}}}tbl")), 1001):
        table.set("id", str(number))
    master.set("secCnt", str(len(sections)))

    manifest, spine = content.find("opf:manifest", NS), content.find("opf:spine", NS)
    for el in list(manifest) + list(spine):
        if (el.get("id") or el.get("idref") or "").startswith("section"):
            el.getparent().remove(el)
    header_item = manifest.find("opf:item[@id='header']", NS)
    for number in reversed(range(len(sections))):
        item = E.Element(f"{{{NS['opf']}}}item", id=f"section{number}",
                         href=f"Contents/section{number}.xml", attrib={"media-type": "application/xml"})
        header_item.addnext(item)
    for number in range(len(sections)):
        E.SubElement(spine, f"{{{NS['opf']}}}itemref", idref=f"section{number}", linear="yes")

    def xml(node):
        return E.tostring(node, encoding="UTF-8", xml_declaration=True)

    text = "\n".join(t for s in sections for t in s.xpath(".//hp:t/text()", namespaces=NS))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.inputs[0]) as src, ZipFile(args.output, "w") as dst:
        for info in src.infolist():
            if info.filename == "Contents/section0.xml":
                for number, section in enumerate(sections):
                    dst.writestr(f"Contents/section{number}.xml", xml(section), ZIP_DEFLATED)
            elif info.filename == "Contents/header.xml":
                dst.writestr(info, xml(master))
            elif info.filename == "Contents/content.hpf":
                dst.writestr(info, xml(content))
            elif info.filename == "Preview/PrvText.txt":
                dst.writestr(info, text.encode("utf-8"))
            else:
                dst.writestr(info, src.read(info))
    print(f"{args.output}: {len(sections)} sections")


if __name__ == "__main__":
    main()
