"""Small, editable HWPX layout builder. Dimensions are in 1/100 point."""

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as E

SEED = Path(__file__).resolve().parents[1] / "assets" / "blank-layout-seed.zip"

# A cell holding only one of these glyphs is a connector between boxes. Its left/right padding
# is made equal so the glyph sits on the cell centre line (the default padding is 320/180).
CONNECTORS = frozenset("+▶◀▲▼→←↑↓↔⇒")

# Symbol-font private-use characters that PDFs carry in their text layer, mapped to the KS X 1001
# character they show. Without the symbol font the editor draws a blank or a box.
PUA_MAP = {"\uf09e": "·"}       # Wingdings middle dot


def unsafe_symbols(text):
    """Non-ASCII, non-Hangul characters outside KS X 1001 (not encodable as EUC-KR).

    KoPub돋움체 and similar Korean fonts cover KS X 1001. Hancom draws other symbols (➜ ❶ ✓ ▪ ☑ ▬)
    from a fallback font, so their size and baseline drift and arrows look misaligned.
    """
    seen = []
    for ch in text:
        if ord(ch) < 0x80 or "\uac00" <= ch <= "\ud7a3" or ch in seen:
            continue
        try:
            ch.encode("euc_kr")
        except UnicodeEncodeError:
            seen.append(ch)
    return seen


class Layout:
    """Build one HWPX section from editable paragraphs and tables."""

    def __init__(self, *, width=61200, height=85900, left=5660, right=5640,
                 top=3180, bottom=2300, regular="KoPub돋움체 Medium",
                 bold="KoPub돋움체 Bold"):
        with ZipFile(SEED) as package:
            self.header = E.fromstring(package.read("Contents/header.xml"))
            self.section = E.fromstring(package.read("Contents/section0.xml"))
        self.ns = self.header.nsmap
        refs = self.get(self.header, "hh:refList")
        self.characters = self.get(refs, "hh:charProperties")
        self.paragraphs = self.get(refs, "hh:paraProperties")
        self.borders = self.get(refs, "hh:borderFills")
        self.font_ids = {}
        for family in self.get(refs, "hh:fontfaces"):
            language = family.get("lang").lower()
            for is_bold, face in ((False, regular), (True, bold)):
                font = deepcopy(family[0])
                ident = str(max(int(f.get("id")) for f in family) + 1)
                font.set("id", ident)
                font.set("face", face)
                self.get(font, "hh:typeInfo").set("weight", "9" if is_bold else "6")
                family.append(font)
                family.set("fontCnt", str(len(family)))
                self.font_ids[language, is_bold] = ident

        self.old_table = self.section.xpath(".//hp:tbl", namespaces=self.ns)[0]
        self.old_cell = self.old_table.xpath(".//hp:tc", namespaces=self.ns)[0]
        initial = deepcopy(self.section[0][0])
        for child in initial.findall("hp:t", self.ns):
            initial.remove(child)
        self.section[:] = []
        page = initial.find(".//hp:pagePr", self.ns)
        page.set("width", str(width))
        page.set("height", str(height))
        margins = dict(left=left, right=right, top=top, bottom=bottom, header=0, footer=0)
        self.get(page, "hp:margin").attrib.update({k: str(v) for k, v in margins.items()})
        self.anchor = self.add_text(size=100, line=100)
        self.anchor.insert(0, initial)

    def q(self, tag):
        prefix, name = tag.split(":")
        return f"{{{self.ns[prefix]}}}{name}"


    def sub(self, parent, tag, **attrs):
        return E.SubElement(parent, self.q(tag), {k:str(v) for k,v in attrs.items()})


    def get(self, parent, tag):
        return parent.find(tag, self.ns)


    def append_style(self, group, item):
        ident = str(max(int(node.get("id")) for node in group) + 1)
        item.set("id", ident)
        group.append(item)
        group.set("itemCnt", str(len(group)))
        return ident


    @lru_cache(None)
    def char(self, size, bold=False, color="#161616", ratio=93):
        el = deepcopy(self.characters[int(bold)])
        el.set("height", str(size))
        el.set("textColor", color)
        for name in self.get(el, "hh:ratio").attrib:
            self.get(el, "hh:ratio").set(name, str(ratio))
        font_ref = self.get(el,"hh:fontRef")
        for language in font_ref.attrib:
            font_ref.set(language,self.font_ids[language,bold])
        for decoration in ("hh:bold","hh:italic"):
            item = self.get(el,decoration)
            if item is not None:
                el.remove(item)
        return self.append_style(self.characters, el)


    @lru_cache(None)
    def para(self, align, line, before=0, after=0):
        el = deepcopy(self.paragraphs[0])
        self.get(el, "hh:align").set("horizontal", align)
        self.get(el, "hh:lineSpacing").set("type", "PERCENT" if line==0 else "FIXED")
        self.get(el, "hh:lineSpacing").set("value", str(line or 100))
        margin = self.get(el, "hh:margin")
        self.get(margin,"hc:prev").set("value",str(before))
        self.get(margin,"hc:next").set("value",str(after))
        return self.append_style(self.paragraphs, el)


    @lru_cache(None)
    def border(self, fill=None, top=None, bottom=None, sides=None, pattern=False):
        el = deepcopy(self.borders[0])
        for direction, kind in [("top",top),("bottom",bottom),("left",sides),("right",sides)]:
            if kind:
                edge = self.get(el, "hh:"+direction+"Border")
                typ, width, color = {"strong":("SOLID","0.3 mm","#555555"),
                                      "soft":("SOLID","0.1 mm","#ABABAB"),
                                      "dot":("DOT","0.1 mm","#BCBCBC")}[kind]
                for key,val in zip(("type","width","color"),(typ,width,color)):
                    edge.set(key,val)
        if fill:
            b = self.sub(el,"hc:fillBrush")
            a = dict(faceColor=fill,hatchColor="#E1E1E1",alpha="0")
            if pattern: a["hatchStyle"] = "BACK_SLASH"
            self.sub(b,"hc:winBrush",**a)
        return self.append_style(self.borders,el)


    def p(self, text="",size=1090,bold=False,color="#161616",align="LEFT",line=1220,before=0,after=0,ratio=93):
        el = E.Element(self.q("hp:p"), paraPrIDRef=self.para(align,line,before,after), styleIDRef="0")
        self.sub(self.sub(el,"hp:run",charPrIDRef=self.char(size,bold,color,ratio)),"hp:t").text=text
        return el


    def add_text(self, *args,**kw):
        el=self.p(*args,**kw)
        self.section.append(el)
        return el


    def table(self, rows, *, gap=0):
        """Build a table placed like a character, without adding it to the page."""
        # Every cell specifies its width, height, content self.paragraphs, and fill.
        table = deepcopy(self.old_table)
        for row in table.findall("hp:tr", self.ns): table.remove(row)
        # Unique within the page, also for tables nested in cells (merge_hwpx renumbers them).
        self.last_table_id = max(5000 + len(self.section), getattr(self, "last_table_id", 0) + 1)
        table.set("id",str(self.last_table_id))
        table.set("rowCnt",str(len(rows)))
        table.set("colCnt",str(max(c[0]+c[6] for row in rows for c in row)))
        table.set("repeatHeader","0")
        table.set("borderFillIDRef","1")
        table.set("pageBreak","CELL")
        self.get(table,"hp:sz").set("width",str(sum(c[1] for c in rows[0])))
        self.get(table,"hp:sz").set("height",str(sum(min(c[2] for c in row) for row in rows)))
        self.get(table,"hp:outMargin").set("bottom",str(gap))
        for ri, cells in enumerate(rows):
            row = self.sub(table,"hp:tr")
            for ci,width,height,contents,fill,span,colspan,*extra in cells:
                cell = deepcopy(self.old_cell)
                row.append(cell)
                cell.set("header","0")
                cell.set("borderFillIDRef",fill)
                cell.set("hasMargin","1")
                listing = self.get(cell,"hp:subList")
                listing[:] = contents
                addr = self.get(cell,"hp:cellAddr")
                addr.set("rowAddr",str(ri))
                addr.set("colAddr",str(ci))
                self.get(cell,"hp:cellSpan").set("rowSpan",str(span))
                self.get(cell,"hp:cellSpan").set("colSpan",str(colspan))
                sz = self.get(cell,"hp:cellSz")
                sz.set("width",str(width))
                sz.set("height",str(height))
                padding = dict(left=320,right=180,top=80,bottom=80)
                text = "".join(t for para in contents
                               for t in para.xpath(".//hp:t/text()", namespaces=self.ns)).strip()
                if text in CONNECTORS:
                    padding.update(left=0, right=0)
                if extra and extra[0]:
                    padding.update(extra[0])
                m=self.get(cell,"hp:cellMargin")
                for key,val in padding.items():
                    m.set(key,str(val))
        return table


    def add_table(self, rows, *, gap=0, floating=None):
        table = self.table(rows, gap=gap)
        if floating:
            table.set("textWrap","IN_FRONT_OF_TEXT")
            table.set("textFlow","BOTH_SIDES")
            pos = self.get(table,"hp:pos")
            pos.attrib.update(dict(treatAsChar="0",flowWithText="0",allowOverlap="1",
                                   vertRelTo="PAPER",horzRelTo="PAPER",
                                   vertOffset=str(floating[1]),horzOffset=str(floating[0])))
            self.anchor[-1].insert(0,table)
        else:
            holder = self.add_text(size=100,line=0)
            holder[0].insert(0,table)
        return table


    def nest(self, rows, *, align="CENTER"):
        """A cell paragraph holding a small table: a box inside a box, such as a label tag.

        The inner table sits like a character, so the paragraph alignment places it. The
        paragraph uses percent line spacing so its line grows to the inner table's height.
        """
        holder = self.p(size=100, line=0, align=align)
        holder[0].insert(0, self.table(rows))
        return holder


    def tagged(self, tag, text, width, height, tag_fill, *, tag_size=900, tag_color="#FFFFFF",
               size=1080, color="#161616", ratio=80, gap=200, align="CENTER", bold=True):
        """Cell contents with a small filled tag box followed by text, both centred vertically.

        A one-row nested table: the tag cell has the fill, the text cell has none. The pair is
        sized from text_width() and centred in the outer cell, never wider than `width`, the
        outer cell's inner width (cell width minus its left and right padding).
        """
        tag_w = text_width(tag, tag_size, ratio) + 300 + 200
        text_w = min(text_width(text, size, ratio) + gap + 300, width - tag_w)
        pad = dict(left=150, right=150, top=0, bottom=0)
        return [self.nest([[
            cell(0, tag_w, height, [self.p(tag, tag_size, True, tag_color, align="CENTER",
                                            line=tag_size + 200, ratio=ratio)], tag_fill, margin=pad),
            cell(1, text_w, height, [self.p(text, size, bold, color, line=size + 170, ratio=ratio)],
                 margin=dict(pad, left=gap, right=0)),
        ]], align=align)]


    def center(self, text,size=1090,bold=False,color="#161616"):
        return [self.p(text,size,bold,color,align="CENTER",line=max(1250,size+80))]


    def write(self, output):
        """Serialize the candidate. The target editor must verify actual pagination."""
        output = Path(output)
        if output.suffix.lower() != ".hwpx":
            raise ValueError("Output path must end in .hwpx")
        output.parent.mkdir(parents=True, exist_ok=True)
        for node in self.section.iter(self.q("hp:t")):
            if node.text and any(ch in node.text for ch in PUA_MAP):
                node.text = node.text.translate(str.maketrans(PUA_MAP))
        replacements = {"Contents/header.xml": self.header, "Contents/section0.xml": self.section}
        with ZipFile(SEED) as src, ZipFile(output, "w") as dst:
            for info in src.infolist():
                node = replacements.get(info.filename)
                blob = (E.tostring(node, encoding="UTF-8", xml_declaration=True)
                        if node is not None else src.read(info))
                if info.filename == "Preview/PrvText.txt":
                    lines = self.section.xpath(".//hp:t/text()", namespaces=self.ns)
                    blob = "\n".join(lines).encode("utf-8")
                dst.writestr(info, blob)
        return output


def text_width(text, size, ratio=100):
    """Generous one-line advance width in 1/100 pt, for sizing cells that must not wrap.

    Hangul, CJK and other non-ASCII glyphs count 1 em, ASCII 0.6 em and spaces 0.35 em,
    so the estimate is at or above the real width in KoPub-style fonts.
    """
    ems = sum(0.35 if ch == " " else 0.6 if ord(ch) < 0x80 else 1.0 for ch in text)
    return round(ems * size * ratio / 100)


def cell(index, width, height, contents, fill="1", span=1, colspan=1, margin=None):
    """Declare one cell. A merged cell carries its full width and height.

    margin: optional dict with any of left/right/top/bottom padding in 1/100 pt.
    """
    return (index, width, height, contents, fill, span, colspan, margin)
