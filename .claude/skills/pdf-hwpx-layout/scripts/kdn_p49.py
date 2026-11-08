"""Rebuild KDN's physical PDF page 49 from the user's original PDF."""

from hwpx_layout import Layout, cell
from pdf_coords import recipe_inputs

source, target = recipe_inputs(49, '외부 지적사항 조치실적')
layout = Layout(top=3180)
add_text, add_table, border = layout.add_text, layout.add_table, layout.border
p, center = layout.p, layout.center
reg, only = source.region, source.only

def body(lines, *, bold=False, size=1090,ratio=90, spacing=1210):
    return [p(t,size,bold,line=spacing,ratio=ratio(t) if callable(ratio) else ratio) for t in lines]

def compact_ratio(text):
    visual_length = sum(1 if ord(c) >= 0x3000 else 0.52 for c in text)
    return max(65, min(84, int(1580 / max(1,visual_length))))


add_table([
    [cell(0,3350,1680,center("01",1380,True,"#FFFFFF"),border("#606060",top="strong"))],
    [cell(0,3350,5960,[p(c,950,True,align="CENTER",line=1160) for c in "경영관리"],border("#D7D7D7"))]
],floating=(57800,15000))
add_table([[
    cell(0,4600,1600,center("PART 01",1000,True),border("#EFEFEF",top="strong")),
    cell(1,5700,1600,center("경영관리",1080,True,"#FFFFFF"),border("#333333")),
    cell(2,19100,1600,[p("",100,line=100)],border(bottom="soft")),
    cell(3,20500,1600,[p(reg(380,390,30,45)[0],1090,align="RIGHT",line=1250,ratio=83)])
]])
add_text(reg(200,220,70,80)[0],1800,True,align="CENTER",line=2400,before=1800,after=350,ratio=97)

widths=(11200,34900,3800)
headings=reg(0,560,98,103)
rows=[[cell(i,w,2070,center(t,1160,True,"#FFFFFF" if i==1 else "#161616"),
            border("#808080" if i==1 else "#D7D7D7",top="strong",sides="soft"))
       for i,(w,t) in enumerate(zip(widths,headings))]]
for i,(lo,hi,h1,h2) in enumerate([(116,163,2590,2120),(163,226,2640,3600),(226,273,2540,2130),(273,348,2630,4800),(348,396,2550,2120)]):
    issue=reg(50,165,lo,hi)
    details=reg(165,510,lo,hi)
    reference=reg(510,560,lo,hi)
    assert len(reference)==1 and len(details)>=3
    end=border(bottom="dot")
    rows.append([
        cell(0,widths[0],h1+h2,body([" ".join(issue)],ratio=85),end,2),
        cell(1,widths[1],h1,body(details[:2],size=1090,ratio=73),border("#EBEBEB",sides="soft")),
        cell(2,widths[2],h1+h2,center(reference[0],1090),end,2),
    ])
    rows.append([cell(1,widths[1],h2,body(["☑ "+t for t in details[2:]],bold=True,size=1050,ratio=lambda t: 65 if t.startswith("☑ 지역전문사원") else 73,spacing=1340),
                      border("#D1D1D1",bottom="dot",sides="soft"))])
# Rowspan cells store total height. The middle cells define the component row heights.
add_table(rows)
add_text(reg(50,100,397,406)[0],940,line=1250,before=240)
add_text(reg(205,215,422,430)[0],1800,True,align="CENTER",line=2400,before=1200,after=280,ratio=97)
for i,band in enumerate((453,543,633,723),1):
    title=reg(120,135,band,band+3)[0]
    add_table([[
        cell(0,6950,2650,[p(f"✓ 평가내용 {i:02}",970,True,"#FFFFFF",align="CENTER",line=1150,ratio=74)],border("#565656",top="strong",bottom="soft")),
        cell(1,42950,2650,[p(title,1120,align="LEFT",line=1400,ratio=70)],border("#E9E9E9",top="strong",bottom="soft",pattern=True))
    ]],gap=340)
    heads=reg(50,560,band+25,band+33)
    assert len(heads)==3
    widths=(13700,18000,18200)
    heading=[cell(j,w,1990,center(t,1120,True,"#FFFFFF" if j==1 else "#161616"),
                  border("#808080" if j==1 else "#D7D7D7",top="strong",sides="soft"))
             for j,(w,t) in enumerate(zip(widths,heads))]
    content=[cell(j,w,3200,body(reg(l,r,band+42,band+69),size=1050,ratio=compact_ratio,spacing=1180),
                  border("#EBEBEB" if j==1 else None,bottom="soft",sides="soft" if j==1 else None))
             for j,(w,l,r) in enumerate(zip(widths,(50,190,370),(190,370,560)))]
    assert all(c[3] for c in content)
    add_table([heading,content],gap=820 if i<4 else 0)
add_text("2025년도 경영실적보고서   29",920,align="RIGHT",line=1300,before=1100)

print(layout.write(target))
