"""Rebuild KDN 2025 report physical PDF page 38 (printed page 23) as editable HWPX.

Usage: python3 work/kdn2025/p38.py <report.pdf> <out.hwpx> [--page N]

윤리경영 ②-③: 통제활동-② 계약관리 플랫폼 and 3. 청렴문화 확산 (even page: PART box head,
footer at the left). Built with the shared kit (one flat table per band, see kit.py / p19.py).
Image-only parts typed as editable cells (read from 4x renders):
  - the whole 다. 윤리소통 diagram (PDF y 600-802): labels, two numbered headers, bullets, the two
    employee quotes, the 'AI 활용 홍보' / 'KDN 튼튼설계' panels and their results;
  - the PART label, section number band, 신규 / 지적사항 개선 badges, the footer logo name.
The two photos become empty placeholder cells; the 청렴 emblem and mascot, the quote avatars
and the check-mark icons are omitted (check marks -> ◎, round arrow icons -> ▶, rings -> ○ ▷).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from kit import Layout, recipe_inputs  # noqa: E402

source, target = recipe_inputs(38, "청렴을 뿌리내리고 윤리경영의 꽃을 피우기 위한 청렴문화 확산 노력")
L = Layout(top=3100)
kit.setup(source, L)
from kit import *  # noqa: E402,F401,F403  helpers and presets bound to this page

GRAYL = "#E6E6E6"    # label tabs
DARKB = "#6A6A6A"    # dark badges
PANEL = "#EBEBEB"    # light gray panels
soft = "soft"
box = dict(top=soft, bottom=soft, left=soft, right=soft)


def margin(g, x0, r0, **pad):
    """Override the padding of the cell whose top-left slot is (r0, x0)."""
    c0 = g.xs.index(kit.to_x(x0))
    g.items[r0, c0] = g.items[r0, c0][:7] + (pad,)


def run(text, size=1090, bold=False, color=INK):
    return (text, size, bold, color)


def title_badge(name, line, edges, top):
    """'가. [pill] title': number | pill | title."""
    runs = runs_of(line)
    g = Grid(name, edges, [1650])
    g.put(edges[0], edges[1], 0, 1, [strip_runs(runs[:1])], align="LEFT", line=1450, fit=False)
    margin(g, edges[0], 0, left=0, right=0)
    g.put(edges[1], edges[2], 0, 1, [runs[1]], pill)
    g.put(edges[2], edges[3], 0, 1, [strip_runs(runs[2:])], align="LEFT", line=1450)
    block(g, top)


# ---------------------------------------------------------------------------
# Page chrome (even page): footer at the left, PART 01 box over a rule (as p22 / p40)
# ---------------------------------------------------------------------------
foot = [(line1(55, 60, 816, 820)["text"], 1090, False, INK), ("   ", 1090, False, INK),
        ("한전KDN㈜", 1090, True, INK)]   # the logo is an image; its name is typed
L.add_table([[cell(0, W, 1500, [para(foot, "LEFT", 1300)[0]])]], floating=(5660, 81550))

g = Grid("head", [X0, 102.6, 158.6, X1], [1600])
g.put(X0, 102.6, 0, 1, [[("PART ", 820, False, INK), ("01", 1450, True, "#505050")]], align="LEFT", line=1400,
      fit=False)
g.put(102.6, 158.6, 0, 1, "경영관리", frame("#333333"), size=1080, bold=True, color=WHITE)
g.put(158.6, X1, 0, 1, [], frame(bottom=soft))
block(g, 31.8)

# ---------------------------------------------------------------------------
# □ “함께하는 공정문화” … [통제활동-②]
# ---------------------------------------------------------------------------
head = line1(68, 72, 69, 73)
g = Grid("heading", [X0, 484.0, 540.0, X1], [1600])
g.put(X0, 484.0, 0, 1, [[("□ ", 1350, True, INK)] + runs_of(head, x1=484)], align="LEFT", line=1400)
g.put(484.0, 540.0, 0, 1, [runs_of(head, x0=484)], frame(WHITE, **box), line=1100)
block(g, 69.0)

xs = [X0, 102.2, 104.8, 110.0, 152.0, X1]
g = Grid("plan", xs, [2430, 350, 350, 1630, 1630, 1630, 1630, 350, 360, 2500])
label = frame(GRAYL, top=soft, bottom=soft)
g.put(X0, 102.2, 0, 1, [line1(58, 62, 97, 100)], label, bold=True)
g.put(104.8, X1, 0, 1, [line1(108, 112, 96, 99)], frame(**box), align="LEFT")
g.put(X0, 102.2, 2, 8, [line1(58, 62, 148, 152)], label, bold=True)
gbox = "#EDEDED"
g.put(104.8, 110.0, 2, 8, [], frame(gbox, top=soft, bottom=soft, left=soft))
g.put(110.0, X1, 2, 3, [], frame(gbox, top=soft, right=soft))
for r, line in enumerate(lines_in(115, 120, 120, 190), 3):
    g.put(110.0, 152.0, r, r + 1, [runs_of(line, WHITE, x1=152)], frame(DARKB), line=1050)
    margin(g, 110.0, r, left=0, right=0, top=150, bottom=150)
    g.put(152.0, X1, r, r + 1, [runs_of(line, x0=152)], frame(gbox, right=soft), align="LEFT")
g.put(110.0, X1, 7, 8, [], frame(gbox, bottom=soft, right=soft))
g.put(X0, 102.2, 9, 10, [line1(58, 62, 201, 204)], label, bold=True)
g.put(104.8, X1, 9, 10, [line1(108, 112, 199, 202)], frame(**box), align="LEFT")
block(g, 91.2)

# ---------------------------------------------------------------------------
# 3. 청렴문화 확산
# ---------------------------------------------------------------------------
g = Grid("section-3", [X0, 85.0, X1], [2300])
g.put(X0, 85.0, 0, 1, [line1(60, 80, 238, 241)], frame("#5E5E5E"), color=WHITE, line=1800)
g.put(85.0, X1, 0, 1, [line1(88, 95, 239, 242)], frame("#E4E4E4"), align="LEFT", line=1700)
block(g, 236.1)

title_badge("title-ga", line1(55, 60, 266, 270), [X0, 76.5, 151.5, X1], 265.2)

# Two cards: chips + lines, photos (left) and the emblem / mascot images (right, omitted).
xs = [X0, 62.0, 84.0, 243.5, 302.5, 304.8, 307.5, 313.0, 334.0, 337.0, 497.0, 527.0, 550.0, X1]
g = Grid("cards", xs, [1900, 700] + [1560] * 6 + [680])
hdr = frame("#D8D8D8", **box)
g.put(X0, 304.8, 0, 1, [line1(125, 130, 291, 294)], hdr, bold=True)
g.put(307.5, 337.0, 0, 1, [], frame("#D8D8D8", top=soft, bottom=soft, left=soft))
g.put(337.0, 497.0, 0, 1, [line1(335, 340, 291, 294)], frame("#D8D8D8", top=soft, bottom=soft), bold=True)
g.put(497.0, 527.0, 0, 1, "신규", frame("#3A3A3A"), size=800, bold=True, color=WHITE, line=950)   # badge image
g.put(527.0, X1, 0, 1, [], frame("#D8D8D8", top=soft, bottom=soft, right=soft))
chip = frame(WHITE, **box)
g.put(X0, 62.0, 1, 8, [], frame(left=soft))
g.put(302.5, 304.8, 1, 8, [], frame(right=soft))
g.put(X0, 304.8, 8, 9, [], frame(left=soft, right=soft, bottom=soft))
for r, y in enumerate((315.8, 331.5, 347.1, 362.6, 378.4, 394.0), 2):
    if y in (347.1, 394.0):      # '➡ …' continuation lines (arrow is an image)
        g.put(62.0, 243.5, r, r + 1, [[run("→ ", 900)] + runs_of(line1(75, 85, y - 1, y + 2))], align="LEFT")
        continue
    line = line1(64, 68, y - 1, y + 2)
    g.put(62.0, 84.0, r, r + 1, [runs_of(line, x1=84)], chip, line=1050)
    margin(g, 62.0, r, left=0, right=0, top=150, bottom=150)
    g.put(84.0, 243.5, r, r + 1, [runs_of(line, x0=84)], align="LEFT")
g.put(243.5, 302.5, 1, 5, [], photo)       # photo: 청렴목 식수
g.put(243.5, 302.5, 5, 8, [], photo)       # photo: 교육 현장
g.put(307.5, 313.0, 1, 8, [], frame(left=soft))
g.put(550.0, X1, 1, 8, [], frame(right=soft))
g.put(307.5, X1, 8, 9, [], frame(left=soft, right=soft, bottom=soft))
for r, y in enumerate((316.0, 331.5, 347.1, 362.6, 378.2, 393.8), 2):
    if r % 2 == 1:
        g.put(313.0, 497.0, r, r + 1, [[run("  → ", 900)] + runs_of(line1(328, 333, y - 1, y + 2))], align="LEFT")
        continue
    line = line1(315, 322, y - 1, y + 2)
    g.put(313.0, 334.0, r, r + 1, [runs_of(line, x1=334)], chip, line=1050)
    margin(g, 313.0, r, left=0, right=0, top=150, bottom=150)
    g.put(334.0, 497.0, r, r + 1, [runs_of(line, x0=334)], align="LEFT")
block(g, 287.8)

# ---------------------------------------------------------------------------
# 나. 윤리규범 정비: three hatched columns
# ---------------------------------------------------------------------------
title_badge("title-na", line1(55, 60, 427, 430), [X0, 76.5, 151.5, X1], 425.5)

xs = [X0, 220.6, 224.3, 388.3, 392.0, 466.5, 492.5, 502.5, X1]
g = Grid("norms", xs, [2250, 1700, 1540, 6450])
body = frame("#EFEFEF", hatch="#DADADA")
g.put(X0, 220.6, 0, 1, [line1(90, 95, 454, 457)], frame(top="mid"), bold=True)
g.put(224.3, 388.3, 0, 1, [line1(228, 232, 454, 457)], frame(top="mid"), bold=True)
g.put(392.0, 502.5, 0, 1, [line1(392, 394, 454, 457)], frame(top="mid"), align="LEFT", bold=True)
g.put(502.5, X1, 0, 1, "지적사항 개선", frame("#4A4A4A", top="mid"), size=780, bold=True, color=WHITE, line=950)


def bullets(found):
    """Bullet lines as they are; continuation lines indented under the bullet text."""
    return [l if l["text"].startswith("∙") else [run("  ")] + runs_of(l) for l in found]


g.put(X0, 220.6, 1, 4, bullets(lines_in(58, 70, 472, 566)), body, align="LEFT", line=1540)
g.put(224.3, 388.3, 1, 4, bullets(lines_in(226, 240, 472, 566)), body, align="LEFT", line=1540)
iso = lines_in(394, 405, 472, 566)
g.put(392.0, X1, 1, 2, [iso[0]], body, align="LEFT", line=1540)
g.put(392.0, 466.5, 2, 3, [[run("  ")] + runs_of(iso[1])], body, align="LEFT", line=1300)
g.put(466.5, 492.5, 2, 3, "신규", frame("#3A3A3A"), size=780, bold=True, color=WHITE, line=950)   # badge image
g.put(492.5, X1, 2, 3, [], body)
g.put(392.0, X1, 3, 4, bullets(iso[2:]), body, align="LEFT", line=1540)
block(g, 447.0)

# ---------------------------------------------------------------------------
# 다. 윤리소통 확대 (image in the PDF; every text below typed from a 4x render)
# ---------------------------------------------------------------------------
title_badge("title-da", line1(55, 60, 578, 582), [X0, 76.5, 151.5, X1], 577.3)

xs = [X0, 74.0, 95.0, 110.0, 116.5, 118.8, 135.4, 179.0, 328.0, 341.7, 343.8, 360.4, 400.0, 484.0, 506.0,
      552.0, X1]
g = Grid("channels", xs, [1700, 400, 5900, 600, 3600, 2100, 3200, 1800, 760])
hatched = frame("#E2E2E2", hatch="#CFCFCF")
g.put(X0, 110.0, 0, 3, ["유형별", "안심 신고", "채널 가동"], frame(**box), size=1200, bold=True, line=1450)
heads = [((118.8, 135.4, 179.0, 328.0), "1", "채널 운영", "목적별 맞춤형 신고채널 운영"),
         ((343.8, 360.4, 400.0, X1), "2", "활성화", "신고 활성화 및 안심 신고 환경 조성")]
for (a, b, c, e), num, tag, title in heads:
    g.put(a, b, 0, 1, num, frame(DARKB), size=1200, bold=True, color=WHITE)
    g.put(b, c, 0, 1, tag, frame("#D4D4D4"), size=1000)
    g.put(c, e, 0, 1, title, frame("#E8E8E8"), align="LEFT", size=1150, bold=True)
CHECK = run("◎ ", 1000, color="#555555")
g.put(116.5, 328.0, 2, 3, [[CHECK, run(t, 1050)] for t in (
    "[익명신고] 외부기관(K-휘슬) 운영",
    "[대리신고] ‘안심변호사’ 운영으로 신고자 보호",
    "[비위신고] 갑질신고센터, 예산부당사용신고 등",
    "[감사청원] 회사 홈페이지 내 대국민 청원채널 운영")], align="LEFT", line=1400)
g.put(341.7, X1, 2, 3, [[CHECK, run("[보호강화] 비밀준수, 불이익 금지, 보상금 지급 등", 1050)],
                        [run("                  신고자 보호 규정 실효성 제고", 1050)],
                        [CHECK, run("[인식개선] 모의신고 시행으로 신고채널 인지도 확대", 1050)],
                        [CHECK, run("[선제감시] 상시 모니터링을 통한 부패요인 사전 차단", 1050)]], align="LEFT", line=1400)
g.put(X0, 110.0, 4, 7, ["활성화", "및", "신뢰성", "향상"], hatched, size=1200, bold=True, line=1400)
g.put(X0, 74.0, 7, 8, [], hatched)
g.put(74.0, 95.0, 7, 8, "노력", frame(WHITE, **box), size=1000, line=1150)
g.put(95.0, 110.0, 7, 8, [], hatched)
for a, e in ((110.0, 116.5), (328.0, 341.7), (552.0, X1)):
    g.put(a, e, 4, 8, [], hatched)
g.put(X0, X1, 8, 9, [], hatched)
quote = frame(PANEL)
ICON = run("▶ ", 900, color="#333333")
RING = run("○ ", 900, color="#555555")
RESULT = run("▷ ", 900, color="#333333")
# Left panel: AI 활용 홍보
g.put(116.5, 328.0, 4, 5, ["“익명 신고채널의 익명성이 정말로", "보장되는지 의심됩니다”"], quote, size=1100,
      line=1500)
g.put(116.5, 328.0, 5, 6, [[ICON, run("AI 활용 홍보 컨텐츠 제작, 설명회 개최", 1150, True)]], frame("#CFCFCF"),
      align="LEFT", line=1350)
g.put(116.5, 328.0, 6, 7, [[RING, run("생성형 AI 활용 스토리북 · 웹툰 제작 및 배포", 1050), run("(9월)", 860)],
                           [RING, run("신고제도 필요성, 익명성 보장 수준 등 설명", 1050), run("(11월)", 860)]],
      quote, align="LEFT", line=1400)
g.put(116.5, 328.0, 7, 8, [[RESULT, run("익명신고 신뢰도 향상(79.9%", 1100, True), run("’24년", 600, True),
                            run(" → 83.4%", 1100, True), run("’25년", 600, True), run(")", 1100, True)]],
      frame("#D9D9D9"), align="LEFT", line=1300)
# Right panel: KDN 튼튼설계
g.put(341.7, 552.0, 4, 5, ["“우리 회사의 내부통제 허점은", "없는지 확인해야 한다고 생각합니다”"], quote, size=1100,
      line=1500)
g.put(341.7, 484.0, 5, 6, [[ICON, run("「KDN 튼튼설계」 프로젝트 추진", 1150, True)]], frame("#CFCFCF"),
      align="LEFT", line=1350)
g.put(484.0, 506.0, 5, 6, "신규", frame(WHITE, **box), size=850, line=1000)   # outlined badge
g.put(506.0, 552.0, 5, 6, [], frame("#CFCFCF"))
g.put(341.7, 552.0, 6, 7, [[RING, run("부정 유발 시나리오 공모전 개최", 1050), run("(11월)", 860)],
                           [run("    - 직원이 직접 잠재 리스크 발굴, 개선방안 제시", 1050)]],
      quote, align="LEFT", line=1400)
g.put(341.7, 552.0, 7, 8, [[RESULT, run("우수 아이디어 포상(6명, 140만원), 내부통제 반영", 1100, True)]],
      frame("#D9D9D9"), align="LEFT", line=1300)
block(g, 600.2)

kit.finish(target, end=801.6)
