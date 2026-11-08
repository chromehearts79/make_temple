"""Rebuild KDN's physical PDF page 13 (printed page 1): Ⅰ. 지표관리 방향.

usage: python3 work/kdn2025/p13.py report.pdf out.hwpx [--page N]

The upper table is extracted from the PDF text layer. The PART header, side tab, the
section number bands and the whole SWOT grid are images in the source PDF; their text
is transcribed from the rendered page and kept as editable cells. Decorative graphics
(rounded frames, the SWOT diagonal and dotted arrows, check-mark bullets) are replaced
by table fills, borders and plain glyphs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/pdf-hwpx-layout/scripts"))

from hwpx_layout import Layout, cell  # noqa: E402
from pdf_coords import recipe_inputs  # noqa: E402

source, target = recipe_inputs(13, "대내외 경영 여건 및 관련 정부 정책")
layout = Layout(top=3180)
add_text, add_table, border = layout.add_text, layout.add_table, layout.border
p = layout.p
reg, only = source.region, source.only
INK = "#161616"


def vis(text):
    """Conservative em-width estimate (Hangul and symbols full width) at 100% ratio."""
    width = 0.0
    for ch in text:
        if ch == " ":
            width += .33
        elif ord(ch) < 128:
            width += .62 if (ch.isupper() or ch.isdigit()) else .55 if ch.islower() else .4
        elif ch in "･":
            width += .5
        else:
            width += 1.0
    return width


def fit(lines, width, size, cap=90, floor=60):
    """Largest 장평 (ratio) that keeps every line on one line inside a cell of this width."""
    need = max(vis(t) for t in lines) * size
    return max(floor, min(cap, int((width - 500) * 0.97 * 100 / need)))


def ps(values, size=1090, bold=False, align="LEFT", ratio=90, color=INK, line=1250, before=0):
    if isinstance(values, str):
        values = [values]
    return [p(t, size, bold, color, align=align, line=line, ratio=ratio, before=before if i == 0 else 0)
            for i, t in enumerate(values)]


def c(i, w, h, v, fill="1", *, bold=False, align="LEFT", size=1090, ratio=90, color=INK,
      span=1, cols=1, line=1250):
    return cell(i, w, h, ps(v, size, bold, align, ratio, color, line), fill, span, cols)


def label(i, w, h, v, fill=None, **kwargs):
    return c(i, w, h, v, fill or gray, bold=True, align="CENTER", **kwargs)


def tab(rows, gap=0):
    return add_table(rows, gap=gap)


# Shared presets (same as the validated p49/p50 recipes).
gray = border("#E9E9E9", top="soft", bottom="soft")
gray2 = border("#D8D8D8", top="strong", bottom="soft", sides="soft")
white = border(top="soft", bottom="soft", sides="soft")
dark = border("#686868", top="strong", bottom="soft")
outline = border(top="strong", bottom="soft", sides="soft")
grid = border(bottom="soft", sides="soft")
striped = border("#E9E9E9", top="strong", bottom="soft", sides="soft", pattern=True)
# Page-specific presets.
mid_head = border("#808080", top="strong", bottom="soft", sides="soft")
hatch = border("#E4E4E4", bottom="dot", sides="soft", pattern=True)
hatch_end = border("#E4E4E4", bottom="strong", sides="soft", pattern=True)
dotted = border(bottom="dot", sides="soft")
closed = border(bottom="strong", sides="soft")
NONE = "1"

# --- side tab and running header (tab and PART label are images in the source) ---
add_table([
    [cell(0, 3350, 1680, layout.center("01", 1380, True, "#FFFFFF"), border("#606060", top="strong"))],
    [cell(0, 3350, 5960, [p(ch, 950, True, align="CENTER", line=1160) for ch in "경영관리"], border("#D7D7D7"))],
], floating=(57800, 15000))
tab([[
    c(0, 4600, 1600, "PART 01", border("#EFEFEF", top="strong"), bold=True, align="CENTER", size=1000),
    c(1, 5700, 1600, "경영관리", border("#333333"), bold=True, align="CENTER", size=1080, color="#FFFFFF"),
    c(2, 19100, 1600, "", border(bottom="soft"), size=100, line=100),
    c(3, 20500, 1600, only(460, 480, 30, 45), align="RIGHT", ratio=88),
]])
add_text(only(230, 250, 65, 75), 1800, True, align="CENTER", line=2400, before=1700, after=1500, ratio=97)


def section_heading(y, gap):
    tab([[label(0, 2850, 2200, only(60, 80, y - 3, y + 3), dark, color="#FFFFFF", size=1720, line=1850),
          c(1, 47050, 2200, only(85, 100, y - 3, y + 3), gray, bold=True, size=1500, ratio=92, line=1800)]], gap)


def fitted(i, w, h, lines, fill, size=1090, cap=82):
    """Like the source, which shrinks long lines, give each line its own 장평 so it fills the cell."""
    return cell(i, w, h, [p(t, size, line=1760, ratio=fit([t], w, size, cap=cap)) for t in lines], fill)


# --- 1. 대내외 경영 여건 및 관련 정부 정책 ---
section_heading(109, 650)
W = [3000, 2800, 21000, 1500, 21600]  # 경영 | 외부/내부 | 주요 이슈 | arrow gutter | 시사점
assert sum(W) == 49900
HEAD, ROW = 2000, 5200
bands = [(160, 200), (210, 255), (265, 310), (318, 360)]
issues = [reg(115, 330, lo, hi) for lo, hi in bands]
implications = [reg(340, 560, lo, hi) for lo, hi in bands]
assert all(len(v) == 2 for v in issues + implications)
rows = [[
    label(0, W[0] + W[1], HEAD, only(70, 80, 135, 145), gray2, cols=2),
    label(2, W[2], HEAD, only(195, 210, 135, 145), gray2),
    c(3, W[3], HEAD, ""),
    label(4, W[4], HEAD, only(430, 440, 135, 145), mid_head, color="#FFFFFF"),
]]
for j, (issue, implication) in enumerate(zip(issues, implications)):
    last = j == 3
    row = []
    if j == 0:
        row.append(label(0, W[0], ROW * 2, reg(60, 70, 190, 215), hatch, span=2))
        row.append(label(1, W[1], ROW, only(85, 95, 170, 180), hatch))
    elif j == 1:
        row.append(label(1, W[1], ROW, only(85, 95, 220, 230), hatch))
    else:
        name = only(60, 70, 275, 285) if j == 2 else only(60, 70, 325, 335)
        row.append(label(0, W[0] + W[1], ROW, name, hatch_end if last else hatch, cols=2))
    row.append(fitted(2, W[2], ROW, issue, closed if last else dotted))
    if j == 0:
        row.append(c(3, W[3], ROW * 4, "▶", NONE, align="CENTER", size=1200, color="#9A9A9A", span=4))
    row.append(fitted(4, W[4], ROW, implication, closed if last else dotted))
    rows.append(row)
tab(rows, 2700)

# --- 2. SWOT 분석 및 전략과제 도출 (image in the source; text transcribed) ---
section_heading(394, 600)

# Column grid: L1 L2 | gap | M1 M2 M3 | gap | R1 R2 R3
G = [3600, 11600, 450, 3600, 4800, 8500, 450, 3600, 4800, 8500]
assert sum(G) == 49900
L, M = G[0] + G[1], G[3] + G[4] + G[5]
band_light = "#E6E6E6"
chip_fill = border("#CFCFCF", top="soft")
band_fill = border(band_light, top="soft")
box_body = border(bottom="soft", sides="soft")
strat_label = border("#3F3F3F", top="strong")
strat_title = border("#D5D5D5", top="soft")
strat_body = border("#EDEDED")
strat_chip = border("#8C8C8C")
BULLET = "✓ "


def gap(i, h, grid_widths=G):
    return c(i, grid_widths[i], h, "", NONE, size=100, line=100)


def bullets(items, width):
    lines = [BULLET + t for t in items]
    return lines, fit(lines, width, 1060, cap=88)


def swot_head(i, w1, w2, name, english):
    return [label(i, w1, 1900, name, chip_fill, size=1150),
            c(i + 1, w2, 1900, english, band_fill, align="RIGHT", size=1050, ratio=92)]


def strategy_head(i, code, title):
    return [label(i, G[i], 1900, code, strat_label, color="#FFFFFF", size=1400, line=1500),
            label(i + 1, G[i + 1] + G[i + 2], 1900, title, strat_title, size=1150, cols=2)]


def strategy_rows(i, pairs, chip_h, text_h):
    """Three (chip, text) pairs as alternating sub-rows inside a strategy column."""
    texts = [t for _, t in pairs]
    ratio = fit(texts, G[i] + G[i + 1] + G[i + 2], 1090, cap=90)
    chip_ratio = fit([k for k, _ in pairs], G[i] + G[i + 1], 1000, cap=88)
    out = []
    for chip, text in pairs:
        out.append([c(i, G[i] + G[i + 1], chip_h, chip, strat_chip, align="CENTER", size=1000,
                      color="#FFFFFF", ratio=chip_ratio, cols=2),
                    c(i + 2, G[i + 2], chip_h, "", strat_body, size=100, line=100)])
        out.append([c(i, G[i] + G[i + 1] + G[i + 2], text_h, text, strat_body, size=1090,
                      ratio=ratio, cols=3)])
    return out


strengths = ["전력계통 全주기 ICT사업 운영 노하우 보유", "한전 및 그룹사 특화 ICT솔루션 보유",
             "업계 최고 수준의 보안기술 및 역량보유", "수소 및 해상풍력ICT 등 민간대비 시장 선점",
             "안정적 재무건전성 확보 및 투자여력 보유"]
weaknesses = ["한전 및 그룹사 중심의 의존적 사업구조", "AI, 분산E 등 미래분야 전문인력 부족",
              "신사업 추진 자체자산 및 인프라 미흡", "해외 투자사업 경험부족으로 소극적 추진",
              "공공기관 사업관련 규제 및 프로세스 복잡·다양"]
opportunities = ["새정부 주요정책에 ICT 역할 부각", "분산E 시장 본격화 및 투자기회 증가",
                 "한전 및 그룹사 IT투자 확대 기조 유지", "체코원전, 데이터센터 등 그룹사 협업 지속",
                 "산업전반 사이버보안 강화 및 확대"]
threats = ["한전 및 그룹사 자체 AX·DX 투자 확대", "ICT영역의 민간경쟁 지속적 증가",
           "전통적 기저사업 역무 축소 가능성", "탄소중립 등 기후대응 규제 강화",
           "ESG, 혁신 등 공공가치 요구수준 강화"]
so = [("DX기반 차세대 전력망", "디지털 혁신 기술 기반 전력망 지능화 선도"),
      ("AI융합 플랫폼 서비스", "AI융합 E플랫폼 중심 사업 패러다임 전환"),
      ("분산E 서비스 다각화", "新 수요시장 대응 분산E 서비스 다각화")]
wo = [("투자기반 에너지신사업", "에너지신사업 자생력 강화를 위한 투자확대"),
      ("전문역량", "고객과 산업을 리드하는 직무중심 전문가 육성"),
      ("경영혁신", "지속가능성과 창출 경영시스템  혁신")]
st = [("New ICT O&M", "AI적용 New ICT O&M 서비스 혁신"),
      ("환경경영", "탄소중립 선도 친환경 디지털 경영 강화"),
      ("상생경영", "사회적가치 창출로 상생협력경영 차별화")]
wt = [("ICT운영 서비스", "ICT운영 서비스 디지털 경쟁력 강화"),
      ("신뢰경영", "투명한 거버넌스 기반 국민 신뢰 경영"),
      ("경영자원", "시너지 효율 극대화 지향 자원배분 최적화")]

# Band A has its own 7-column grid so every column boundary is defined by some cell:
# corner box | gap | 강점 chip, Strength | gap | 약점 chip, Weakness.
HA, BA = 1900, 5200
A = [L, G[2], G[3], G[4] + G[5], G[6], G[7], G[8] + G[9]]
assert sum(A) == 49900
s_lines, s_ratio = bullets(strengths, M)
w_lines, w_ratio = bullets(weaknesses, M)
tab([
    [c(0, L, HA + BA, "내부역량 →", border("#D9D9D9", top="strong", sides="soft"), bold=True,
       align="RIGHT", size=1400, ratio=92, line=1600, span=2),
     gap(1, HA, A), *swot_head(2, A[2], A[3], "강점", "Strength"),
     gap(4, HA, A), *swot_head(5, A[5], A[6], "약점", "Weakness")],
    [gap(1, BA, A),
     c(2, M, BA * 2, s_lines, box_body, size=1060, ratio=s_ratio, line=1880, span=2, cols=2),
     gap(4, BA, A),
     c(5, M, BA * 2, w_lines, box_body, size=1060, ratio=w_ratio, line=1880, span=2, cols=2)],
    [c(0, L, BA, "↓ 외부환경", box_body, bold=True, size=1400, ratio=92, line=1600),
     gap(1, BA, A), gap(4, BA, A)],
], 650)


def strategy_band(name, english, items, left_pair, right_pair, gap_after):
    (code_m, title_m, pairs_m), (code_r, title_r, pairs_r) = left_pair, right_pair
    chip_h, text_h = 1500, 2000
    lines, ratio = bullets(items, L)
    mids = strategy_rows(3, pairs_m, chip_h, text_h)
    rights = strategy_rows(7, pairs_r, chip_h, text_h)
    rows = [[*swot_head(0, G[0], G[1], name, english), gap(2, 1900), *strategy_head(3, code_m, title_m),
             gap(6, 1900), *strategy_head(7, code_r, title_r)]]
    for k, (m_row, r_row) in enumerate(zip(mids, rights)):
        h = chip_h if k % 2 == 0 else text_h
        row = []
        if k == 0:
            row.append(c(0, L, 3 * (chip_h + text_h), lines, box_body, size=1060, ratio=ratio,
                         line=1880, span=6, cols=2))
        row += [gap(2, h), *m_row, gap(6, h), *r_row]
        rows.append(row)
    tab(rows, gap_after)


strategy_band("기회", "Opportunity", opportunities, ("SO", "역량 확대", so), ("WO", "기회 포착", wo), 600)
strategy_band("위협", "Threat", threats, ("ST", "선택 집중", st), ("WT", "약점 보완", wt), 0)

# --- footer: two runs keep the source sizes (7.9pt title, 10.9pt page number) ---
footer = add_text(only(440, 540, 815, 830) + "   ", 800, align="RIGHT", line=1300, before=900)
footer.append(p(only(545, 560, 815, 832), 1090)[0])

print(layout.write(target))
