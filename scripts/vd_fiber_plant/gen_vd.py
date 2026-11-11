#!/usr/bin/env python3
"""Generate the VD overview fiber plant draw.io diagram. Usage: gen_vd.py <out.drawio>"""
import sys
import xml.etree.ElementTree as ET

mxfile = ET.Element("mxfile", host="Electron")
diagram = ET.SubElement(mxfile, "diagram", id="mL0A8LK-hVtzoJInjnnh", name="VD Fiber Plant")
model = ET.SubElement(
    diagram, "mxGraphModel", dx="1463", dy="966", grid="1", gridSize="10", guides="1",
    tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
    pageWidth="2270", pageHeight="1500", math="0", shadow="0")
root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")

ABS = {"1": (0, 0)}  # absolute origin of each vertex, for parent-relative geometry


def vertex(cid, value, style, x, y, w, h, parent="1"):
    px, py = ABS[parent]
    cell = ET.SubElement(root, "mxCell", id=cid, parent=parent, style=style, value=value, vertex="1")
    geo = ET.SubElement(cell, "mxGeometry", x=str(x - px), y=str(y - py), width=str(w), height=str(h))
    geo.set("as", "geometry")
    ABS[cid] = (x, y)
    return cid


def edge(cid, value, style, source, target, points=(), label_x=None):
    cell = ET.SubElement(root, "mxCell", id=cid, parent="1", style=style, value=value,
                         edge="1", source=source, target=target)
    geo = ET.SubElement(cell, "mxGeometry", relative="1")
    if label_x is not None:
        geo.set("x", str(label_x))
    geo.set("as", "geometry")
    if points:
        arr = ET.SubElement(geo, "Array")
        arr.set("as", "points")
        for x, y in points:
            ET.SubElement(arr, "mxPoint", x=str(x), y=str(y))
    return cid


def pin(ex, ey, nx, ny):
    return (f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;exitPerimeter=0;"
            f"entryX={nx};entryY={ny};entryDx=0;entryDy=0;entryPerimeter=0;")


TEXT = "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;"
BOX = "rounded=1;whiteSpace=wrap;html=1;fontSize=11;"
SWIM = "swimlane;horizontal=0;strokeColor=#000000;fontSize=12;fillColor=#FFFFFF;"
PANEL = "rounded=0;whiteSpace=wrap;html=1;fontSize=20;horizontal=0;"
TRI = "triangle;whiteSpace=wrap;html=1;align=left;"
THIN = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;strokeColor=#000000;strokeWidth=1;"
BIDIR = "startArrow=classic;startFill=1;"
FLEX = "shape=flexArrow;endArrow=classic;html=1;rounded=0;strokeColor=#000000;strokeWidth=1;fontSize=10;width=22;endSize=8.66;"
TRUNK = FLEX + "fillColor=#FF00FF;"
QSFP = FLEX + "fillColor=#33FFFF;"
# Colour by who purchases: TDE green, BDE purple, PDS orange, DAQ blue, FDC I&I pink
TDE, TDE_FILL, TDE_LINE = "fillColor=#D5E8D4;strokeColor=#82B366;", "fillColor=#97D077;", "strokeColor=#4D9900;"
DAQ, DAQ_FILL, DAQ_LINE = "fillColor=#DAE8FC;strokeColor=#6C8EBF;", "fillColor=#7EA6E0;", "strokeColor=#2F5FB3;"
INI, INI_FILL, INI_LINE = "fillColor=#FFD6E7;strokeColor=#D6336C;", "fillColor=#FF99CC;", "strokeColor=#D6336C;"
COAX = "dashed=1;"

BDE, BDE_FILL, BDE_LINE = "fillColor=#E1D5E7;strokeColor=#9673A6;", "fillColor=#C3ABD0;", "strokeColor=#9673A6;"
PDS, PDS_FILL, PDS_LINE = "fillColor=#FFE6CC;strokeColor=#D79B00;", "fillColor=#FFB570;", "strokeColor=#D79B00;"
DEV = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=12;"
THINFLEX = FLEX.replace("width=22", "width=14")
BOTH = "startArrow=block;"
DX, DY = 30, 130  # the drawing sits right of the timing return route and below the title


def v(cid, value, style, x, y, w, h, parent="1"):
    return vertex(cid, value, style, x + DX, y + DY, w, h, parent)


def pts(*points):
    return tuple((x + DX, y + DY) for x, y in points)


# Headings
vertex("title", "VD", TEXT + "fontStyle=1;fontSize=24;", 40, 20, 60, 30)
vertex("sub", "DAQ fiber and network connections for one 27U detector-top rack (40X) and the shared timing and readout hardware.<br>"
       "Details are in the per-subsystem diagrams: VD Fiber Plant TDE, BDE and PDS.",
       TEXT + "fontStyle=1;fontSize=14;align=left;", 40, 64, 1000, 44)

# Detector electronics outside the rack
v("tde", "TDE: 2x Horizontal Container (8x uTCA crate)", DEV + TDE, 320, 130, 300, 190)
v("tde-data", "8x25G Data (LC duplex)", BOX + TDE, 340, 165, 260, 50, parent="tde")
v("tde-ctrl", "8x1G Ctrl (RJ45 Cu)", BOX + TDE, 340, 222, 260, 42, parent="tde")
v("tde-wr", "WR timing (8x SM fiber)", BOX + TDE, 340, 270, 260, 42, parent="tde")
v("bde", "BDE: 2x WIEC on flange (12x WIB + 2x PTC)", DEV + BDE, 320, 520, 300, 190)
v("bde-tim", "DTS timing, 1 per PTC (2x SM fiber)", BOX + BDE, 340, 555, 260, 42, parent="bde")
v("bde-ctrl", "14x1G Ctrl (RJ45 Cu)", BOX + BDE, 340, 603, 260, 42, parent="bde")
v("bde-data", "24x10G Data (LC duplex)", BOX + BDE, 340, 652, 260, 50, parent="bde")

# 27U detector top rack
v("rack", "27U Detector Top rack (40X: DR_2bbN / DR_2bbS)", "swimlane;startSize=26;" + INI, 700, 110, 690, 640)
v("split", "Timing<br>splitter 1:6", BOX + DAQ, 740, 340, 110, 170, parent="rack")
v("aggsw", "1G Ctrl<br>agg.<br>switch", TRI + INI, 930, 340, 100, 180, parent="rack")
v("aggsw-note", "28+ port 1G Aggregating switch:<br>TDE 8, BDE 14, PDS 4,<br>CRP level meter 1, DPS PDU 1",
  TEXT + "fontSize=11;", 910, 262, 200, 56, parent="rack")
v("pds", "PDS: DAPHNE, LCM,<br>2x PoF", DEV + PDS, 950, 560, 200, 90, parent="rack")
v("pds-note", "4x10G patched,<br>1 active", TEXT + "fontSize=11;fontStyle=0;", 990, 605, 120, 36, parent="pds")
v("pp27", "Patch Panel (27U)", PANEL + INI, 1330, 150, 32, 580, parent="rack")

# Into the rack
edge("d-tde", "TDE Data: 2x MTP8 breakout 25G MM OM4 to 27U", FLEX + TDE_FILL + pin(1, 0.5, 0, 0.069), "tde-data", "pp27")
edge("d-bde", "BDE Data: 4x MTP12 pigtail 10G MM OM4 to 27U", FLEX + BDE_FILL + pin(1, 0.5, 0, 0.9086), "bde-data", "pp27")
edge("d-pds", "4x LC duplex", FLEX + PDS_FILL + pin(1, 0.5, 0, 0.7845), "pds", "pp27")
edge("k-tde", "8x RJ45 Cu", THIN + BIDIR + TDE_LINE + pin(1, 0.5, 0, 0.2), "tde-ctrl", "aggsw",
     points=pts((890, 243), (890, 376)), label_x=-0.6)
edge("k-bde", "14x RJ45 Cu", THIN + BIDIR + BDE_LINE + pin(1, 0.5, 0, 0.8), "bde-ctrl", "aggsw",
     points=pts((890, 624), (890, 484)), label_x=-0.6)
edge("k-pds", "4x RJ45 Cu", THIN + BIDIR + PDS_LINE + pin(0.15, 0, 0.5, 0.75), "pds", "aggsw")
edge("up", "2x LC duplex (2x10G)", THIN + BIDIR + INI_LINE + pin(1, 0.5, 0, 0.4828), "aggsw", "pp27")
edge("t-bde", "2x SM", THIN + BIDIR + BDE_LINE + pin(1, 0.5, 0.27, 1), "bde-tim", "split", points=pts((770, 576),), label_x=-0.3)
edge("t-pds", "2x SM", THIN + BIDIR + PDS_LINE + pin(0, 0.5, 0.5, 1), "pds", "split", points=pts((795, 605),), label_x=0.3)

# Trunks to the DAQ barracks
v("ppdaq", "Patch Panel (DAQ Barracks)", PANEL + DAQ, 1640, 150, 32, 580)
for n, name, sub, lab, ey in (
        ("tde", "TDE Data", "2 trunks, 8 active fibers each", "2x MTP12 25G MM OM4 (12f) to DAQ", 0.069),
        ("ctrl", "Ctrl Data", "1 trunk, 4 active fibers (2x10G)", "MTP12 10G MM OM4 (12f) to DAQ", 0.362),
        ("pds", "PDS Data", "1 trunk, 2 active fibers + 6 debug", "MTP12 10G MM OM4 (12f) to DAQ", 0.638),
        ("bde", "BDE Data", "4 trunks, 12 active fibers each", "4x MTP12 10G MM OM4 (12f) to DAQ", 0.9086)):
    y = 150 + 580 * ey
    top = y - 62 if n != "tde" else y - 68
    v(f"h-{n}", name, TEXT + "fontSize=15;", 1441, top, 120, 24)
    v(f"s-{n}", sub, TEXT + "fontSize=11;", 1391, top + 22, 220, 18)
    edge(f"tr-{n}", lab, FLEX + INI_FILL + (BOTH if n == "ctrl" else "") + pin(1, ey, 0, ey), "pp27", "ppdaq")

# DAQ barracks: readout switches and servers
for n, sw, srv, link, aoc, ey, h in (
        ("tde", "5x TDE readout switch", "TDE readout servers<br>20 (4x100G inputs each,<br>1 per 2 racks)", "8x25G", "2x 100G AOC", 0.069, 110),
        ("pds", "1x PDS readout switch", "PDS readout servers<br>2 (4x100G inputs each,<br>1 uplink per 10 racks)", "1x10G active", "100G AOC", 0.638, 90),
        ("bde", "9x BDE readout switch", "BDE TPC readout servers<br>20 (4x100G inputs each,<br>1 per 2 racks)", "24x10G", "2x 100G AOC", 0.9086, 110)):
    y = 150 + 580 * ey
    v(f"sw-{n}", "", TRI + DAQ, 1800, y - h / 2, 90, h)
    v(f"swl-{n}", sw, TEXT + "fontSize=11;", 1760, y - h / 2 - 22, 170, 20)
    edge(f"r-{n}", link, THIN + DAQ_LINE + pin(1, ey, 0, 0.5), "ppdaq", f"sw-{n}")
    v(f"srv-{n}", srv, "rounded=0;whiteSpace=wrap;html=1;fontSize=11;" + DAQ, 2040, y - 40, 170, 80)
    edge(f"q-{n}", aoc, THINFLEX + DAQ_FILL + pin(1, 0.5, 0, 0.5), f"sw-{n}", f"srv-{n}")
v("ctrlsw", "", TRI + INI, 1800, 320, 60, 80)
v("ctrlsw-note", "Ctrl network switch in DAQ Barracks", TEXT + "fontSize=11;", 1870, 342, 130, 36)
edge("u1", "2x10G", THIN + BIDIR + DAQ_LINE + pin(1, 0.362, 0, 0.5), "ppdaq", "ctrlsw")

# Timing: White Rabbit on the mezzanine for TDE, DTS fanout on the cryostat roof for BDE and PDS
v("mezz", "Detector Mezzanine", "swimlane;startSize=26;" + INI, 30, 150, 230, 180)
v("intf", "2x DTS-WR interface unit<br>+ optical splitter", BOX + DAQ, 45, 185, 200, 50, parent="mezz")
v("wr", "White Rabbit network:<br>2 GM + 2 L2 + 20 L1 switches", BOX + TDE, 45, 265, 200, 52, parent="mezz")
edge("coax", "10 MHz, 1PPS (coax)", THIN + COAX + DAQ_LINE + pin(0.5, 1, 0.5, 0), "intf", "wr")
edge("wrfib", "8x SM", THIN + BIDIR + TDE_LINE + "strokeWidth=2;" + pin(1, 0.5, 0, 0.5), "wr", "tde-wr")
v("fanout", "DTS fanout<br>(dedicated rack on the cryostat roof,<br>serves all 40 racks)", BOX + DAQ, 40, 385, 200, 80)
edge("feed", "2x SM LC/APC per rack (1 active, 1 spare),<br>direct, not via the 27U patch panel",
     THINFLEX + BOTH + DAQ_FILL + pin(1, 0.5, 0, 0.5), "fanout", "split")
v("hbar", "DAQ Barracks", TEXT + "fontStyle=1;fontSize=14;", 1700, 770, 180, 26)
v("dts", "DTS master<br>(2x DTS uTCA crate)", BOX + DAQ, 1700, 800, 180, 70)
edge("dts-fan", "SM fiber, DTS master to roof fanout rack (count TBD)",
     THINFLEX + BOTH + DAQ_FILL + pin(0, 0.5, 0.5, 1), "dts", "fanout", points=pts((140, 835),))
edge("fan-wr", "2x SM fiber<br>(1000Base-BX)",
     THINFLEX + BOTH + DAQ_FILL + pin(0, 0.5, 0, 0.5), "fanout", "intf", points=pts((-10, 425), (-10, 210)))

# Legend
swatches = (("#D5E8D4", "#82B366", "TDE"), ("#E1D5E7", "#9673A6", "BDE"), ("#FFE6CC", "#D79B00", "PDS"),
            ("#DAE8FC", "#6C8EBF", "DAQ"), ("#FFD6E7", "#D6336C", "FDC I&amp;I"))
legend = ('<table cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
          '<tr><th colspan="2" align="left">Colour = who purchases</th></tr>'
          + "".join(f'<tr><td style="background:{f};border:1px solid {s};width:40px;"></td><td>{t}</td></tr>' for f, s, t in swatches)
          + '<tr><td colspan="2">Thick arrows: fiber trunks. Thin solid: patch / copper. Thin dashed: coax.</td></tr>'
          '</table>')
vertex("legend", legend, "text;html=1;whiteSpace=wrap;overflow=fill;strokeColor=#000000;fillColor=none;align=left;verticalAlign=top;",
       1910, 10, 330, 215)

# Notes and totals
rows = [
    ("TDE: uTCA crates / 25G data links", "8", "320"),
    ("BDE: WIBs / 10G data links", "12 / 24", "480 / 960"),
    ("PDS: DAPHNE / active 10G data links", "1 / 1", "40 / 40"),
    ("MTP12 trunks to DAQ barracks (TDE 2, BDE 4, PDS 1, Ctrl 1)", "8", "320"),
    ("1G Ctrl ports on aggregating switch", "28", "1120"),
    ("Timing splitters 1:6 (BDE PTCs, DAPHNE, LCM)", "1", "40"),
    ("SM timing fibers, roof fanout rack to 27U rack", "2", "80"),
    ("WR timing fibers, mezzanine to TDE crates", "8", "320"),
    ("Readout switches (TDE 5, BDE 9, PDS 1)", "-", "15"),
    ("100G uplinks to servers (TDE 80, BDE 80, PDS 4)", "-", "164"),
    ("Readout servers (TDE 20, BDE 20, PDS 2)", "-", "42"),
]
table = ('<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
         '<tr><th align="left">VD totals</th><th>Per 27U rack</th><th>40 racks</th></tr>'
         + "".join(f'<tr><td>{a}</td><td align="center">{b}</td><td align="center">{c}</td></tr>' for a, b, c in rows)
         + "</table>")
v("totals", table, "text;html=1;overflow=fill;strokeColor=none;fillColor=none;align=left;verticalAlign=top;",
  10, 920, 700, 330)

v("notes",
  "<b>Draft 2026-11-11</b><br>"
  "Sources: &quot;VD onDetector Rack View of Cabling&quot; (TMS, stamped 16SEPT2026); "
  "&quot;VD Cryostat 27U Detector Racks&quot; naming drawing (20 N + 20 S racks); "
  "&quot;DTS to TDE White Rabbit Synchronisation Interface&quot; (EDMS 3482906, draft v7.0); "
  "&quot;DAQ Readout Network&quot; PRR specification (EDMS 3463072, v1.0).<br><br>"
  "<b>Notes and open items</b> (more in the per-subsystem diagrams)<br>"
  "1. All readout switches and servers are in the DAQ barracks; the detector-top rack holds only the patch panel, "
  "the 1G Ctrl aggregating switch and the timing splitter, plus the PDS warm electronics.<br>"
  "2. The readout network specification counts 42 VD DAPHNE (5 uplinks); 40 are drawn, one per rack.<br>"
  "3. The patching between the trunk patch panel and the readout switches (top-of-rack patch panels, MTP-12 into "
  "4-way breakout transceivers) is not drawn in detail.<br>"
  "4. The CRP level meter and DPS PDU Ctrl ports are taken from the TMS sheet. The sheet lists 44 on-detector switches for 40 racks.<br>"
  "5. Two 10G Ctrl uplinks per 27U rack are assumed. The mezzanine Ctrl switch for the WR hardware is shown in the TDE diagram only.<br>"
  "6. DTS fanout rack on the cryostat roof (feeds the 27U rack splitters and the DTS-WR interface on the mezzanine): "
  "location, hardware and fiber count from the DTS master are not defined here.",
  "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=8;", 750, 920, 1460, 330)

ET.indent(mxfile, space="  ")
ET.ElementTree(mxfile).write(sys.argv[1], encoding="unicode")
