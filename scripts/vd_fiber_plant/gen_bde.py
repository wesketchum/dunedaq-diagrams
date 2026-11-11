#!/usr/bin/env python3
"""Generate the VD BDE fiber plant draw.io diagram. Usage: gen_bde.py <out.drawio>"""
import sys
import xml.etree.ElementTree as ET

mxfile = ET.Element("mxfile", host="Electron")
diagram = ET.SubElement(mxfile, "diagram", id="vd-bde-fiber-plant", name="VD Fiber Plant BDE")
model = ET.SubElement(
    diagram, "mxGraphModel", dx="1463", dy="966", grid="1", gridSize="10", guides="1",
    tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
    pageWidth="2120", pageHeight="1700", math="0", shadow="0")
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
# Colour by who purchases: BDE purple, DAQ blue, FDC I&I pink
BDE, BDE_FILL, BDE_LINE = "fillColor=#E1D5E7;strokeColor=#9673A6;", "fillColor=#C3ABD0;", "strokeColor=#9673A6;"
DAQ, DAQ_FILL, DAQ_LINE = "fillColor=#DAE8FC;strokeColor=#6C8EBF;", "fillColor=#7EA6E0;", "strokeColor=#2F5FB3;"
INI, INI_FILL, INI_LINE = "fillColor=#FFD6E7;strokeColor=#D6336C;", "fillColor=#FF99CC;", "strokeColor=#D6336C;"
COAX = "dashed=1;"

DY = 100  # the drawing sits below the title and legend


def v(cid, value, style, x, y, w, h, parent="1"):
    return vertex(cid, value, style, x, y + DY, w, h, parent)


DEV = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=12;"
THINFLEX = FLEX.replace("width=22", "width=14")

# Headings
vertex("title", "VD BDE", TEXT + "fontStyle=1;fontSize=24;", 40, 20, 130, 30)
vertex("bde-count", "80 WIECs total, 2 to each 27U rack (12 WIBs + 2 PTCs per rack). The WIECs sit on the BDE flange.<br>"
       "DAQ fiber and network connections only.",
       TEXT + "fontStyle=1;fontSize=14;align=left;", 40, 64, 900, 44)

# WIECs on the flange, each split into its 6 WIBs and its PTC; the lower one is mirrored
# so that timing faces the splitter between them
def wiec(w, top, wib_y, ptc_y, wib_ports, ptc_ports):
    v(w, "WIEC on BDE flange", DEV + BDE, 270, top, 300, 320)
    v(f"{w}-wib", "6x WIB", DEV + BDE, 285, wib_y, 270, 140, parent=w)
    v(f"{w}-ptc", "PTC", DEV + BDE, 285, ptc_y, 270, 125, parent=w)
    labels = {"data": "12x10G Data<br>(2x LC duplex per WIB)", "wctrl": "6x1G Ctrl, 1 per WIB (RJ45 Cu)",
              "pctrl": "1x1G Ctrl (RJ45 Cu)", "tim": "DTS timing (1x SM fiber)"}
    for dev, ports in ((f"{w}-wib", wib_ports), (f"{w}-ptc", ptc_ports)):
        for port, y, h in ports:
            v(f"{w}-{port}", labels[port], BOX + BDE, 300, y, 240, h, parent=dev)


wiec("w1", 120, 150, 300, (("data", 178, 55), ("wctrl", 238, 42)), (("pctrl", 328, 40), ("tim", 373, 42)))
wiec("w2", 510, 675, 540, (("wctrl", 703, 42), ("data", 750, 55)), (("tim", 567, 42), ("pctrl", 614, 40)))

# 27U detector top rack
v("rack", "27U Detector Top rack (40X: DR_2bbN / DR_2bbS)", "swimlane;startSize=26;" + INI, 640, 110, 510, 740)
v("split", "Timing splitter 1:6<br><br>shared with PDS<br>(DAPHNE, LCM)", BOX + DAQ, 680, 370, 110, 240, parent="rack")
v("aggsw", "1G Ctrl<br>agg.<br>switch", TRI + INI, 850, 400, 100, 180, parent="rack")
v("aggsw-note", "28+ port 1G Detector Top<br>Aggregating switch<br>(14 ports used by BDE)",
  TEXT + "fontSize=11;", 850, 590, 200, 50, parent="rack")
v("pp27", "Patch Panel (27U)", PANEL + INI, 1100, 150, 32, 680, parent="rack")

# WIECs -> 27U rack
edge("d1", "12x10G Data: 2x MTP12 pigtail 10G MM OM4 (24f) to 27U", FLEX + BDE_FILL + pin(1, 0.5, 0, 0.0816), "w1-data", "pp27")
edge("d2", "12x10G Data: 2x MTP12 pigtail 10G MM OM4 (24f) to 27U", FLEX + BDE_FILL + pin(1, 0.5, 0, 0.9228), "w2-data", "pp27")
for cid, label, src_port, sy, cx, ey in (("k1w", "6x RJ45 Cu", "w1-wctrl", 259, 830, 0.12), ("k1p", "1x RJ45 Cu", "w1-pctrl", 348, 810, 0.27),
                                         ("k2p", "1x RJ45 Cu", "w2-pctrl", 634, 810, 0.73), ("k2w", "6x RJ45 Cu", "w2-wctrl", 724, 830, 0.88)):
    edge(cid, label, THIN + BIDIR + BDE_LINE + pin(1, 0.5, 0, ey), src_port, "aggsw",
         points=((cx, sy + DY), (cx, 400 + 180 * ey + DY)), label_x=-0.7)
edge("up", "2x LC duplex<br>(2x10G)", THIN + BIDIR + INI_LINE + pin(1, 0.5, 0, 0.5), "aggsw", "pp27")
edge("t1f", "SM", THIN + BIDIR + BDE_LINE + pin(0, 0.1, 1, 0.5), "split", "w1-tim")
edge("t2f", "SM", THIN + BIDIR + BDE_LINE + pin(0, 0.9083, 1, 0.5), "split", "w2-tim")

# Trunks to the DAQ barracks
v("ppdaq", "Patch Panel (DAQ Barracks)", PANEL + DAQ, 1420, 150, 32, 680)
for n, hy in (("1", 100), ("2", 672)):
    v(f"h{n}", "BDE TPC Data", TEXT + "fontSize=16;", 1216, hy, 120, 30)
    v(f"s{n}", "12 active fibers (6x10G) in each", TEXT, 1176, hy + 28, 200, 20)
for n, ey in (("1", 0.0485), ("2", 0.1147), ("3", 0.8897), ("4", 0.9559)):
    edge(f"t{n}", "MTP12 10G MM OM4 (12f) to DAQ", FLEX + INI_FILL + pin(1, ey, 0, ey), "pp27", "ppdaq")
v("hc", "Ctrl Data", TEXT + "fontSize=16;", 1216, 416, 120, 30)
v("sc", "4 active fibers (2x10G uplinks),<br>shared by all subsystems in the rack", TEXT, 1166, 442, 220, 32)
edge("tc", "MTP12 10G MM OM4 (12f) to DAQ", FLEX + INI_FILL + "startArrow=block;" + pin(1, 0.5, 0, 0.5), "pp27", "ppdaq")

# DAQ barracks
v("ctrlsw", "", TRI + INI, 1510, 445, 60, 90)
v("ctrlsw-note", "Ctrl network switch in DAQ Barracks", TEXT, 1475, 540, 130, 36)
edge("u1", "2xLC", THIN + BIDIR + DAQ_LINE + pin(1, 0.5, 0, 0.5), "ppdaq", "ctrlsw")
v("rosw", "Readout<br>Switch in<br>DAQ<br>Barracks", TRI + DAQ, 1650, 360, 100, 260)
v("rosw-note", "9 switches for all VD BDE:<br>12x10G (3 QSFP+ 4x10G breakout<br>ports) per 100G uplink",
  TEXT + "fontSize=11;", 1680, 640, 220, 50)
edge("r1", "12x10G", THIN + DAQ_LINE + pin(1, 0.0816, 0, 0.2), "ppdaq", "rosw",
     points=((1620, 205.5 + DY), (1620, 412 + DY)))
edge("r2", "12x10G", THIN + DAQ_LINE + pin(1, 0.9228, 0, 0.8), "ppdaq", "rosw",
     points=((1620, 777.5 + DY), (1620, 568 + DY)))
v("server", "BDE TPC<br>Readout Server<br>4x100G inputs<br><br>(reads out 2x 27U racks =<br>4x WIEC, 24x WIB)",
  "rounded=0;whiteSpace=wrap;html=1;" + DAQ, 1900, 390, 170, 200)
edge("q1", "QSFP28 100G AOC", FLEX + DAQ_FILL + pin(0.75, 0.375, 0, 0.3375), "rosw", "server")
edge("q2", "QSFP28 100G AOC", FLEX + DAQ_FILL + pin(0.75, 0.625, 0, 0.6625), "rosw", "server")

# DTS timing: fanout rack on the cryostat roof, master in the DAQ barracks
v("fanout", "DTS fanout<br>(dedicated rack on the cryostat roof,<br>serves all 40 racks)", BOX + DAQ, 40, 430, 180, 85)
edge("feed", "2x SM LC/APC fiber per 27U rack (1 active, 1 spare; 80 total),<br>direct from fanout rack, not via 27U patch panel",
     THINFLEX + "startArrow=block;" + DAQ_FILL + pin(1, 0.5, 0, 0.427), "fanout", "split")
v("hbar", "DAQ Barracks", TEXT + "fontStyle=1;fontSize=14;", 1500, 920, 180, 30)
v("dts", "DTS master<br>(2x DTS uTCA crate)", BOX + DAQ, 1500, 960, 180, 70)
edge("dtsfib", "SM fiber, DTS master to roof fanout rack (count TBD)",
     THINFLEX + "startArrow=block;" + DAQ_FILL + pin(0, 0.5, 0.5, 1), "dts", "fanout", points=((130, 995 + DY),))

# Legend
legend = ('<table cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
          '<tr><th colspan="2" align="left">Colour = who purchases</th></tr>'
          '<tr><td style="background:#E1D5E7;border:1px solid #9673A6;width:40px;"></td><td>BDE</td></tr>'
          '<tr><td style="background:#DAE8FC;border:1px solid #6C8EBF;"></td><td>DAQ</td></tr>'
          '<tr><td style="background:#FFD6E7;border:1px solid #D6336C;"></td><td>FDC I&amp;I</td></tr>'
          '<tr><td colspan="2">Thick arrows: fiber trunks. Thin solid: patch / copper.</td></tr>'
          '</table>')
vertex("legend", legend, "text;html=1;whiteSpace=wrap;overflow=fill;strokeColor=#000000;fillColor=none;align=left;verticalAlign=top;",
       1740, 20, 330, 170)

# Notes and totals
rows = [
    ("WIECs (6 WIB + 1 PTC each)", "2", "80"),
    ("PTCs", "2", "80"),
    ("WIBs", "12", "480"),
    ("10G data links (2 per WIB)", "24", "960"),
    ("Active data fibers", "48", "1920"),
    ("MTP12 pigtails, WIEC to 27U panel", "4", "160"),
    ("MTP12 data trunks to DAQ barracks (12 active)", "4", "160"),
    ("1G Ctrl ports on aggregating switch (12 WIB + 2 PTC)", "14", "560"),
    ("Timing splitter outputs used by BDE (1 per PTC)", "2", "80"),
    ("SM timing fibers, splitter to PTC", "2", "80"),
    ("100G uplinks, readout switch to server", "2", "80"),
    ("BDE readout switches", "-", "9"),
    ("BDE TPC readout servers (4x100G inputs, 2 racks each)", "1 per 2", "20"),
]
table = ('<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
         '<tr><th align="left">BDE totals</th><th>Per 27U rack</th><th>40 racks</th></tr>'
         + "".join(f'<tr><td>{a}</td><td align="center">{b}</td><td align="center">{c}</td></tr>' for a, b, c in rows)
         + "</table>")
v("totals", table, "text;html=1;overflow=fill;strokeColor=none;fillColor=none;align=left;verticalAlign=top;",
  40, 1070, 660, 355)

v("notes",
  "<b>Draft 2026-11-11</b><br>"
  "Sources: DAQ VD Fiber Plant v3; &quot;VD onDetector Rack View of Cabling&quot; (TMS, stamped 16SEPT2026); "
  "&quot;VD Cryostat 27U Detector Racks&quot; naming drawing (20 N + 20 S racks); "
  "&quot;DAQ Readout Network&quot; PRR specification (EDMS 3463072, v1.0, 21 May 2026).<br><br>"
  "<b>Open items</b><br>"
  "1. Purchase ownership assumed by analogy with TDE and PDS, not confirmed: BDE buys the WIEC electronics, the MTP12 pigtails "
  "to the 27U patch panel, the RJ45 Cu cables and the timing fibers from the PTCs to the splitter; "
  "racks and the patch cord from the 1G switch to the 27U patch panel are FDC I&amp;I.<br>"
  "2. The patching between the trunk patch panel and the readout switches (top-of-rack patch panels, MTP-12 into 4-way breakout transceivers, per EDMS 3463072) is not drawn in detail.<br>"
  "3. DTS fanout rack on the cryostat roof: rack name and location, fanout hardware, number of fibers from the DTS master "
  "and its Ctrl network connection are not defined here.<br>"
  "4. The 1G ports for the CRP level meter and the DPS PDU on the TMS sheet (&quot;2x1G DPS&quot; in the VD overview) are not drawn here.<br>"
  "5. Two 10G Ctrl uplinks per 27U rack are assumed.<br>"
  "6. Follow-up: who purchases the 2xLC patch cord from the DAQ barracks patch panel to the Ctrl network switch (drawn as DAQ).",
  "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=8;", 740, 1070, 1330, 355)

ET.indent(mxfile, space="  ")
ET.ElementTree(mxfile).write(sys.argv[1], encoding="unicode")
