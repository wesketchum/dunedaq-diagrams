#!/usr/bin/env python3
"""Generate the VD PDS fiber plant draw.io diagram.

Writes DUNE_Detector_Fiber_Plant-v<version>-VD_Fiber_Plant_PDS.drawio next to this script
unless --output is given.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--version", default="4", help="version number for the file name and the diagram stamp (default: 4)")
parser.add_argument("--output", type=Path, help="output .drawio path (default: versioned name next to this script)")
args = parser.parse_args()
OUT = args.output or Path(__file__).parent / f"DUNE_Detector_Fiber_Plant-v{args.version}-VD_Fiber_Plant_PDS.drawio"

mxfile = ET.Element("mxfile", host="Electron")
diagram = ET.SubElement(mxfile, "diagram", id="vd-pds-fiber-plant", name="VD Fiber Plant PDS")
model = ET.SubElement(
    diagram, "mxGraphModel", dx="1463", dy="966", grid="1", gridSize="10", guides="1",
    tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
    pageWidth="1900", pageHeight="1600", math="0", shadow="0")
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
# Colour by who purchases: PDS orange, DAQ blue, FDC I&I pink
PDS, PDS_FILL, PDS_LINE = "fillColor=#FFE6CC;strokeColor=#D79B00;", "fillColor=#FFB570;", "strokeColor=#D79B00;"
DAQ, DAQ_FILL, DAQ_LINE = "fillColor=#DAE8FC;strokeColor=#6C8EBF;", "fillColor=#7EA6E0;", "strokeColor=#2F5FB3;"
INI, INI_FILL, INI_LINE = "fillColor=#FFD6E7;strokeColor=#D6336C;", "fillColor=#FF99CC;", "strokeColor=#D6336C;"
COAX = "dashed=1;"

DY = 100  # the drawing sits below the title and legend


def v(cid, value, style, x, y, w, h, parent="1"):
    return vertex(cid, value, style, x, y + DY, w, h, parent)


DEV = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=12;"
THINFLEX = FLEX.replace("width=22", "width=14")

# Headings
vertex("title", "VD PDS", TEXT + "fontStyle=1;fontSize=24;", 90, 20, 130, 30)
vertex("pds-count", "40 DAPHNE drawn, 1 per 27U rack. The PDS warm electronics sit in the detector-top rack.<br>"
       "DAQ fiber and network connections only (signal, laser and power-over-fiber fibers to the cryostat are not drawn).",
       TEXT + "fontStyle=1;fontSize=14;align=left;", 90, 64, 900, 44)

# 27U detector top rack
v("rack", "27U Detector Top rack (40X: DR_2bbN / DR_2bbS)", "swimlane;startSize=26;" + INI, 90, 110, 810, 640)
v("split", "Timing splitter 1:6<br><br>shared with BDE<br>(2 outputs,<br>1 per PTC)", BOX + DAQ, 115, 310, 100, 230, parent="rack")

v("daphne", "DAPHNE", DEV + PDS, 270, 150, 230, 230, parent="rack")
v("d-data", "4x 10G Data (LC duplex)<br>1 active, 3 patched for debug", BOX + PDS, 300, 180, 180, 65, parent="daphne")
v("d-ctrl", "1x1G Ctrl<br>(RJ45 Cu)", BOX + PDS, 300, 255, 180, 50, parent="daphne")
v("d-tim", "DTS timing<br>(1x SM fiber)", BOX + PDS, 300, 315, 180, 50, parent="daphne")

v("lcm", "Light Calibration Module (LCM)", DEV + PDS, 270, 400, 230, 150, parent="rack")
v("l-ctrl", "1x1G Ctrl<br>(RJ45 Cu)", BOX + PDS, 300, 430, 180, 45, parent="lcm")
v("l-tim", "DTS timing<br>(1x SM fiber)", BOX + PDS, 300, 485, 180, 45, parent="lcm")

v("pof", "Power over Fiber (PoF) x2", DEV + PDS, 270, 570, 230, 90, parent="rack")
v("p-ctrl", "1x1G Ctrl each<br>(RJ45 Cu)", BOX + PDS, 300, 600, 180, 45, parent="pof")

v("aggsw", "1G Ctrl<br>agg.<br>switch", TRI + INI, 640, 350, 100, 180, parent="rack")
v("aggsw-note", "28+ port 1G Detector Top<br>Aggregating switch<br>(4 ports used by PDS)",
  TEXT + "fontSize=11;", 600, 290, 190, 50, parent="rack")
v("pp27", "Patch Panel (27U)", PANEL + INI, 850, 150, 32, 580, parent="rack")

# Inside the rack
edge("d1", "4x LC duplex 10G MM OM4 (8f) to 27U patch panel", FLEX + PDS_FILL + pin(1, 0.5, 0, 0.1078), "d-data", "pp27")
edge("k1", "1x RJ45 Cu", THIN + BIDIR + PDS_LINE + pin(1, 0.5, 0, 0.2), "d-ctrl", "aggsw",
     points=((560, 280 + DY), (560, 386 + DY)), label_x=-0.5)
edge("k2", "1x RJ45 Cu", THIN + BIDIR + PDS_LINE + pin(1, 0.5, 0, 0.5694), "l-ctrl", "aggsw")
edge("k3", "2x RJ45 Cu", THIN + BIDIR + PDS_LINE + pin(1, 0.5, 0, 0.85), "p-ctrl", "aggsw",
     points=((590, 622.5 + DY), (590, 503 + DY)), label_x=-0.5)
edge("up", "2x LC duplex<br>(2x10G)", THIN + BIDIR + INI_LINE + pin(1, 0.5, 0, 0.5), "aggsw", "pp27")
edge("t-d", "SM", THIN + BIDIR + PDS_LINE + pin(1, 0.1304, 0, 0.5), "split", "d-tim")
edge("t-l", "SM", THIN + BIDIR + PDS_LINE + pin(1, 0.8587, 0, 0.5), "split", "l-tim")

# Trunks to the DAQ barracks
v("ppdaq", "Patch Panel (DAQ Barracks)", PANEL + DAQ, 1170, 150, 32, 580)
v("h1", "PDS Data", TEXT + "fontSize=16;", 976, 140, 120, 30)
v("s1", "2 active fibers (1x10G),<br>6 patched for debug, 4 dark", TEXT, 926, 166, 220, 32)
edge("t1", "MTP12 10G MM OM4 (12f) to DAQ", FLEX + INI_FILL + pin(1, 0.1078, 0, 0.1078), "pp27", "ppdaq")
v("hc", "Ctrl Data", TEXT + "fontSize=16;", 976, 366, 120, 30)
v("sc", "4 active fibers (2x10G uplinks),<br>shared by all subsystems in the rack", TEXT, 926, 396, 220, 32)
edge("tc", "MTP12 10G MM OM4 (12f) to DAQ", FLEX + INI_FILL + "startArrow=block;" + pin(1, 0.5, 0, 0.5), "pp27", "ppdaq")

# DAQ barracks
v("ctrlsw", "", TRI + INI, 1260, 395, 60, 90)
v("ctrlsw-note", "Ctrl network switch in DAQ Barracks", TEXT, 1225, 490, 130, 36)
edge("u1", "2xLC", THIN + BIDIR + DAQ_LINE + pin(1, 0.5, 0, 0.5), "ppdaq", "ctrlsw")
v("rosw", "Readout<br>Switch in<br>DAQ<br>Barracks", TRI + DAQ, 1400, 100, 100, 225)
v("rosw-note", "1 switch for all VD PDS:<br>4 DAPHNE per 40GBASE-SR4 QSFP+<br>breakout port (4x10G),<br>10 DAPHNE per 100G uplink",
  TEXT + "fontSize=11;", 1350, 330, 220, 64)
edge("r1", "1x10G active", THIN + DAQ_LINE + pin(1, 0.1078, 0, 0.5), "ppdaq", "rosw")
v("server", "PDS<br>Readout Servers<br>4x100G inputs each<br><br>40 DAPHNE = 4 uplinks<br>(spec: 42 DAPHNE, 5 uplinks<br>over 2 servers)",
  "rounded=0;whiteSpace=wrap;html=1;" + DAQ, 1700, 137.5, 170, 150)
edge("q1", "QSFP28 100G AOC", FLEX + DAQ_FILL + pin(1, 0.5, 0, 0.5), "rosw", "server")

# DTS timing: fanout rack on the cryostat roof, master in the DAQ barracks
v("fanout", "DTS fanout<br>(dedicated rack on the cryostat roof,<br>serves all 40 racks)", BOX + DAQ, 90, 880, 250, 70)
edge("feed", "2x SM LC/APC fiber per 27U rack<br>(1 active, 1 spare; 80 total),<br>direct from fanout rack,<br>not via 27U patch panel",
     THINFLEX + "startArrow=block;" + DAQ_FILL + pin(0.3, 0, 0.5, 1), "fanout", "split", label_x=-0.53)
v("hbar", "DAQ Barracks", TEXT + "fontStyle=1;fontSize=14;", 1250, 840, 180, 30)
v("dts", "DTS master<br>(2x DTS uTCA crate)", BOX + DAQ, 1250, 880, 180, 70)
edge("dtsfib", "SM fiber, DTS master to roof fanout rack (count TBD)", THINFLEX + "startArrow=block;" + DAQ_FILL + pin(0, 0.5, 1, 0.5), "dts", "fanout")

# Legend
legend = ('<table cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
          '<tr><th colspan="2" align="left">Colour = who purchases</th></tr>'
          '<tr><td style="background:#FFE6CC;border:1px solid #D79B00;width:40px;"></td><td>PDS</td></tr>'
          '<tr><td style="background:#DAE8FC;border:1px solid #6C8EBF;"></td><td>DAQ</td></tr>'
          '<tr><td style="background:#FFD6E7;border:1px solid #D6336C;"></td><td>FDC I&amp;I</td></tr>'
          '<tr><td colspan="2">Thick arrows: fiber trunks. Thin solid: patch / copper.</td></tr>'
          '</table>')
vertex("legend", legend, "text;html=1;whiteSpace=wrap;overflow=fill;strokeColor=#000000;fillColor=none;align=left;verticalAlign=top;",
       1540, 20, 330, 170)

# Notes and totals
rows = [
    ("DAPHNE", "1", "40 (spec: 42)"),
    ("10G data links patched to 27U panel (LC duplex)", "4", "160"),
    ("Active 10G data links", "1", "40"),
    ("Active data fibers", "2", "80"),
    ("MTP12 data trunks to DAQ barracks (2 active + 6 debug + 4 dark)", "1", "40"),
    ("1G Ctrl ports on aggregating switch (DAPHNE, LCM, 2x PoF)", "4", "160"),
    ("Timing splitters 1:6 (shared with BDE; 2 outputs used by PDS)", "1", "40"),
    ("SM timing fibers, roof fanout rack to 27U rack (1 active + 1 spare)", "2", "80"),
    ("SM timing fibers, splitter to DAPHNE / LCM", "2", "80"),
    ("QSFP+ 4x10G breakout ports on readout switch", "1 per 4", "10 (spec: 11)"),
    ("100G uplinks, readout switch to servers", "1 per 10", "4 (spec: 5)"),
    ("PDS readout switches", "-", "1"),
    ("PDS readout servers (4x100G inputs)", "-", "2"),
]
table = ('<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
         '<tr><th align="left">PDS totals</th><th>Per 27U rack</th><th>40 racks</th></tr>'
         + "".join(f'<tr><td>{a}</td><td align="center">{b}</td><td align="center">{c}</td></tr>' for a, b, c in rows)
         + "</table>")
v("totals", table, "text;html=1;overflow=fill;strokeColor=none;fillColor=none;align=left;verticalAlign=top;",
  90, 990, 660, 380)

v("notes",
  f"<b>v{args.version}, draft 2026-11-11</b><br>"
  "Sources: DAQ VD Fiber Plant v3; &quot;VD onDetector Rack View of Cabling&quot; (TMS, stamped 16SEPT2026); "
  "&quot;VD Cryostat 27U Detector Racks&quot; naming drawing (20 N + 20 S racks); "
  "&quot;DAQ Readout Network&quot; PRR specification (EDMS 3463072, v1.0, 21 May 2026).<br><br>"
  "<b>Open items</b><br>"
  "1. The readout network specification counts 42 VD DAPHNE (11 breakout ports, 5 uplinks, 2 servers); 40 are drawn, one per 27U rack. "
  "Where the other two sit is not known (the TMS sheet mentions an extra PDS membrane flange).<br>"
  "2. The TMS cabling sheet gives 1-4 10GbE LC links per DAPHNE. Drawn here: 4 patched, 1 active.<br>"
  "3. Ctrl ports per rack (DAPHNE 1, LCM 1, PoF 2) are read from the TMS sheet; the PoF count needs confirming.<br>"
  "4. DTS fanout rack on the cryostat roof: rack name and location, fanout hardware, number of fibers from the DTS master "
  "and its Ctrl network connection are not defined here.<br>"
  "5. The patching between the trunk patch panel and the readout switches (top-of-rack patch panels, MTP-12 into 4-way breakout transceivers, per EDMS 3463072) is not drawn in detail.<br>"
  "6. Two 10G Ctrl uplinks per 27U rack are assumed.<br>"
  "7. Purchase ownership assumed, not confirmed: racks (FDC I&amp;I); patch cord from the 1G switch to the 27U patch panel (FDC I&amp;I).<br>"
  "8. Follow-up: who purchases the 2xLC patch cord from the DAQ barracks patch panel to the Ctrl network switch (drawn as DAQ).",
  "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=8;", 790, 990, 1080, 380)

ET.indent(mxfile, space="  ")
ET.ElementTree(mxfile).write(OUT, encoding="unicode")
print(f"Wrote {OUT}")
