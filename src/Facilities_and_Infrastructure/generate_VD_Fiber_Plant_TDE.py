#!/usr/bin/env python3
"""Generate the VD TDE fiber plant draw.io diagram.

Writes DUNE_Detector_Fiber_Plant-v<version>-VD_Fiber_Plant_TDE.drawio next to this script
unless --output is given.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--version", default="4", help="version number for the file name and the diagram stamp (default: 4)")
parser.add_argument("--output", type=Path, help="output .drawio path (default: versioned name next to this script)")
args = parser.parse_args()
OUT = args.output or Path(__file__).parent / f"DUNE_Detector_Fiber_Plant-v{args.version}-VD_Fiber_Plant_TDE.drawio"

mxfile = ET.Element("mxfile", host="Electron")
diagram = ET.SubElement(mxfile, "diagram", id="vd-tde-fiber-plant", name="VD Fiber Plant TDE")
model = ET.SubElement(
    diagram, "mxGraphModel", dx="1463", dy="966", grid="1", gridSize="10", guides="1",
    tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
    pageWidth="1800", pageHeight="1900", math="0", shadow="0")
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
# Colour by who purchases: TDE green, DAQ blue, FDC I&I pink
TDE, TDE_FILL, TDE_LINE = "fillColor=#D5E8D4;strokeColor=#82B366;", "fillColor=#97D077;", "strokeColor=#4D9900;"
DAQ, DAQ_FILL, DAQ_LINE = "fillColor=#DAE8FC;strokeColor=#6C8EBF;", "fillColor=#7EA6E0;", "strokeColor=#2F5FB3;"
INI, INI_FILL, INI_LINE = "fillColor=#FFD6E7;strokeColor=#D6336C;", "fillColor=#FF99CC;", "strokeColor=#D6336C;"
COAX = "dashed=1;"

# Headings
vertex("title", "VD TDE", TEXT + "fontStyle=1;fontSize=24;", 90, 20, 130, 30)
vertex("tde-count", "80 Horizontal Containers total, 2 to each 27U rack (8 uTCA crates per rack)",
       TEXT + "fontStyle=1;fontSize=14;align=left;", 90, 64, 440, 40)

# TDE horizontal containers, 4 uTCA crates each
for c, cy in (("c1", 110), ("c2", 520)):
    vertex(c, "Horizontal Container", SWIM + TDE, 90, cy, 353, 380)
    for k, (dx, dy) in enumerate(((33, 10), (193, 10), (33, 195), (193, 195))):
        crate = vertex(f"{c}-crate{k}", "uTCA Crate", SWIM + TDE, 90 + dx, cy + dy, 150, 175, parent=c)
        vertex(f"{crate}-data", "1x25G Data<br>(LC duplex)", BOX + TDE, 90 + dx + 30, cy + dy + 10, 110, 45, parent=crate)
        vertex(f"{crate}-ctrl", "1x1G Ctrl<br>(RJ45 Cu)", BOX + TDE, 90 + dx + 30, cy + dy + 65, 110, 45, parent=crate)
        vertex(f"{crate}-wr", "WR timing<br>(1x SM fiber)", BOX + TDE, 90 + dx + 30, cy + dy + 120, 110, 45, parent=crate)

# 27U detector top rack
vertex("rack", "27U Detector Top rack (40X: DR_2bbN / DR_2bbS)", "swimlane;startSize=26;" + INI, 540, 84, 300, 816)
vertex("pp27", "Patch Panel (27U)", PANEL + INI, 790, 130, 32, 750, parent="rack")
vertex("aggsw", "1G Ctrl<br>agg.<br>switch", TRI + INI, 580, 420, 100, 180, parent="rack")
vertex("aggsw-note", "28+ port 1G Detector Top<br>Aggregating switch<br>(8 ports used by TDE)",
       TEXT + "fontSize=11;", 570, 360, 190, 50, parent="rack")

# Containers -> 27U rack
edge("d1", "4x25G Data: 8xLC to MTP8 25G MM OM4 (8f) to 27U", FLEX + TDE_FILL + pin(1, 0.316, 0, 0.133), "c1", "pp27")
edge("d2", "4x25G Data: 8xLC to MTP8 25G MM OM4 (8f) to 27U", FLEX + TDE_FILL + pin(1, 0.632, 0, 0.84), "c2", "pp27")
edge("k1", "4x RJ45 Cu<br>(4x1G Ctrl)", THIN + BIDIR + TDE_LINE + pin(1, 0.934, 0, 0.25), "c1", "aggsw", label_x=-0.3)
edge("k2", "4x RJ45 Cu<br>(4x1G Ctrl)", THIN + BIDIR + TDE_LINE + pin(1, 0.092, 0, 0.75), "c2", "aggsw", label_x=-0.3)
edge("up", "2x LC duplex<br>(2x10G)", THIN + BIDIR + INI_LINE + pin(1, 0.5, 0, 0.507), "aggsw", "pp27")

# Trunks to the DAQ barracks
vertex("ppdaq", "Patch Panel (DAQ Barracks)", PANEL + DAQ, 1110, 130, 32, 750)
for n, y, ey in (("1", 230, 0.133), ("2", 760, 0.84)):
    vertex(f"h{n}", "TDE Data", TEXT + "fontSize=16;", 916, y - 72, 120, 30)
    vertex(f"s{n}", "8 active fibers (4x25G), 4 dark", TEXT, 876, y - 44, 200, 20)
    edge(f"t{n}", "MTP12 25G MM OM4 (12f) to DAQ", FLEX + INI_FILL + pin(1, ey, 0, ey), "pp27", "ppdaq")
vertex("hc", "Ctrl Data", TEXT + "fontSize=16;", 916, 426, 120, 30)
vertex("sc", "4 active fibers (2x10G uplinks),<br>shared by all subsystems in the rack", TEXT, 866, 456, 220, 32)
edge("tc", "MTP12 10G MM OM4 (12f) to DAQ", FLEX + INI_FILL + "startArrow=block;" + pin(1, 0.507, 0, 0.507), "pp27", "ppdaq")

# DAQ barracks
vertex("ctrlsw", "", TRI + INI, 1200, 465, 60, 90)
vertex("ctrlsw-note", "Ctrl network switch in DAQ Barracks", TEXT, 1160, 560, 130, 36)
edge("u1", "2xLC", THIN + BIDIR + DAQ_LINE + pin(1, 0.507, 0, 0.5), "ppdaq", "ctrlsw")
vertex("rosw", "Readout<br>Switch in<br>DAQ<br>Barracks", TRI + DAQ, 1340, 380, 100, 260)
edge("r1", "4x25G", THIN + DAQ_LINE + pin(1, 0.133, 0, 0.2), "ppdaq", "rosw", points=((1310, 230), (1310, 432)))
edge("r2", "4x25G", THIN + DAQ_LINE + pin(1, 0.84, 0, 0.8), "ppdaq", "rosw", points=((1310, 760), (1310, 588)))
vertex("server", "TDE<br>Readout Server<br>4x100G inputs<br><br>(reads out 2x 27U racks =<br>4x Horizontal Containers)",
       "rounded=0;whiteSpace=wrap;html=1;" + DAQ, 1590, 410, 160, 200)
edge("q1", "QSFP28 100G MM Patch", FLEX + DAQ_FILL + pin(0.75, 0.375, 0, 0.3375), "rosw", "server")
edge("q2", "QSFP28 100G MM Patch", FLEX + DAQ_FILL + pin(0.75, 0.625, 0, 0.6625), "rosw", "server")

# Detector mezzanine: DTS to TDE White Rabbit timing chain (EDMS 3482906)
vertex("mezz", "Detector Mezzanine: DTS to TDE White Rabbit (WR) timing, one set for the whole detector",
       "swimlane;startSize=26;" + INI, 90, 1010, 1010, 420)
vertex("l1", "L1 WR switch (1 of 20)<br>18 ports: 2 uplinks (1 active),<br>16 downlinks = 2x 27U racks<br>(8 to this rack's crates)",
       BOX + TDE, 190, 1127, 190, 100, parent="mezz")
for s, y, n in (("a", 1060, "1"), ("b", 1240, "2")):
    vertex(f"l2m{s}", f"WR switch L2-{n}-2 M<br>(extra ports)", BOX + TDE, 440, y, 120, 55, parent="mezz")
    vertex(f"gm{s}", f"WR Grand Master L2-{n}", BOX + TDE, 620, y, 130, 55, parent="mezz")
    vertex(f"intf{s}", "DTS-WR interface unit<br>(incl. DTS TDC)", BOX + DAQ, 810, y, 130, 55, parent="mezz")
    edge(f"coax{s}", "10 MHz<br>1PPS", THIN + COAX + DAQ_LINE + pin(0, 0.5, 1, 0.5), f"intf{s}", f"gm{s}")
    edge(f"wrl2{s}", "WR", THIN + BIDIR + TDE_LINE + pin(0, 0.5, 1, 0.5), f"gm{s}", f"l2m{s}")
vertex("split", "Passive optical<br>splitter / combiner", BOX + DAQ, 980, 1147, 100, 60, parent="mezz")
edge("spa", "DTS", THIN + BIDIR + DAQ_LINE + pin(0.5, 0, 1, 0.5), "split", "intfa")
edge("spb", "DTS", THIN + BIDIR + DAQ_LINE + pin(0.5, 1, 1, 0.5), "split", "intfb")
edge("upa", "WR", THIN + BIDIR + TDE_LINE + pin(0, 0.5, 1, 0.25), "l2ma", "l1")
edge("upb", "WR", THIN + BIDIR + TDE_LINE + pin(0, 0.5, 1, 0.75), "l2mb", "l1")

# Synchronisation check hardware, between the two redundant chains
vertex("pulse", "Pulse generators x2<br>(network controlled)", BOX + DAQ, 810, 1150, 130, 55, parent="mezz")
vertex("wrtdc", "WR TDC x2<br>(PC, SPEC + FMC-DIO)", BOX + TDE, 620, 1150, 130, 55, parent="mezz")
edge("p-dtsa", "sync pulse", THIN + COAX + DAQ_LINE + pin(0.5, 0, 0.5, 1), "pulse", "intfa")
edge("p-dtsb", "sync pulse", THIN + COAX + DAQ_LINE + pin(0.5, 1, 0.5, 0), "pulse", "intfb")
edge("p-wr", "sync<br>pulse", THIN + COAX + DAQ_LINE + pin(0, 0.5, 1, 0.5), "pulse", "wrtdc")
edge("gma-tdc", "WR", THIN + BIDIR + TDE_LINE + pin(0.5, 1, 0.5, 0), "gma", "wrtdc")
edge("gmb-tdc", "WR", THIN + BIDIR + TDE_LINE + pin(0.5, 0, 0.5, 1), "gmb", "wrtdc")
vertex("sync-note", "Sync check: each pulse generator feeds both DTS TDCs and both WR TDCs (3.3V LVTTL)",
       TEXT + "fontSize=11;", 425, 1140, 180, 75, parent="mezz")

# Management on the DAQ control network
vertex("mezzsw", "1G Ctrl<br>switch<br>(mezz.)", TRI + INI, 980, 1290, 90, 120, parent="mezz")
edge("mgmt", "1G Cu management to DAQ Ctrl network: 24 WR switches, 2 WR TDC PCs, pulse generators",
     THIN + BIDIR + TDE_LINE + pin(0.5, 1, 0, 0.833), "l1", "mezzsw", points=((285, 1390),))

# WR fibers to the crates, and links to the DAQ barracks
THINFLEX = FLEX.replace("width=22", "width=14")
edge("wrfib", "8x SM fiber, 1000Base-BX, 1 per uTCA crate<br>(4 to each Horizontal Container)<br>direct to chimneys, not via the 27U rack",
     THINFLEX + "startArrow=block;" + TDE_FILL + pin(0.5, 0, 0.552, 1), "l1", "c2", label_x=0.5)
vertex("hroof", "Cryostat roof", TEXT + "fontStyle=1;fontSize=14;", 1250, 1095, 180, 30)
vertex("fanout", "DTS fanout<br>(dedicated rack, also feeds<br>the 27U rack timing splitters)", BOX + DAQ, 1250, 1142, 180, 70)
edge("dtsfib", "2x SM fiber (1000Base-BX)", THINFLEX + "startArrow=block;" + DAQ_FILL + pin(0, 0.5, 1, 0.5), "fanout", "split")
vertex("hbar", "DAQ Barracks", TEXT + "fontStyle=1;fontSize=14;", 1570, 1095, 180, 30)
vertex("dts", "DTS master<br>(2x DTS uTCA crate)", BOX + DAQ, 1570, 1142, 180, 70)
edge("dtsmaster", "SM fiber<br>(count TBD)", THINFLEX + "startArrow=block;" + DAQ_FILL + pin(0, 0.5, 1, 0.5), "dts", "fanout")
vertex("ctrlnet", "Ctrl network switches in DAQ Barracks<br>(also carry NTP to the WR GMs)", "rounded=0;whiteSpace=wrap;html=1;fontSize=11;" + INI,
       1250, 1315, 180, 70)
edge("mezzup", "Ctrl uplink", THIN + BIDIR + INI_LINE + pin(1, 0.5, 0, 0.5), "mezzsw", "ctrlnet")

# Legend
legend = ('<table cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
          '<tr><th colspan="2" align="left">Colour = who purchases</th></tr>'
          '<tr><td style="background:#D5E8D4;border:1px solid #82B366;width:40px;"></td><td>TDE</td></tr>'
          '<tr><td style="background:#DAE8FC;border:1px solid #6C8EBF;"></td><td>DAQ</td></tr>'
          '<tr><td style="background:#FFD6E7;border:1px solid #D6336C;"></td><td>FDC I&amp;I</td></tr>'
          '<tr><td colspan="2">Thick arrows: fiber trunks. Thin solid: patch / copper. Thin dashed: coax.</td></tr>'
          '</table>')
vertex("legend", legend, "text;html=1;whiteSpace=wrap;overflow=fill;strokeColor=#000000;fillColor=none;align=left;verticalAlign=top;",
       1420, 20, 330, 170)

# Notes and totals
rows = [
    ("uTCA crates", "8", "320"),
    ("25G data links (LC duplex)", "8", "320"),
    ("Active data fibers", "16", "640"),
    ("MTP8 breakouts, container to 27U panel", "2", "80"),
    ("MTP12 data trunks to DAQ barracks (8 active + 4 dark)", "2", "80"),
    ("1G Ctrl ports on aggregating switch (RJ45 Cu)", "8", "320"),
    ("100G links, readout switch to server", "2", "80"),
    ("TDE readout servers (4x100G inputs, 2 racks each)", "1 per 2", "20"),
    ("WR timing fibers, mezzanine to crates (SM, TDE-owned)", "8", "320"),
    ("WR switches on mezzanine (2 GM + 2 L2 + 20 L1)", "-", "24"),
    ("DTS-WR interface units / pulse generators / WR TDCs", "-", "2 each"),
    ("SM timing fibers, DTS fanout rack (cryostat roof) to mezzanine", "-", "2"),
    ("1G Ctrl ports on mezzanine for WR (24 switches + 2 TDC PCs)", "-", "26+"),
]
table = ('<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%;height:100%;font-size:12px;">'
         '<tr><th align="left">TDE totals</th><th>Per 27U rack</th><th>40 racks</th></tr>'
         + "".join(f'<tr><td>{a}</td><td align="center">{b}</td><td align="center">{c}</td></tr>' for a, b, c in rows)
         + "</table>")
vertex("totals", table, "text;html=1;overflow=fill;strokeColor=none;fillColor=none;align=left;verticalAlign=top;",
       90, 1460, 660, 380)

vertex("notes",
       f"<b>v{args.version}, draft 2026-11-11</b><br>"
       "Sources: DAQ VD Fiber Plant v3; &quot;VD onDetector Rack View of Cabling&quot; (TMS, stamped 16SEPT2026); "
       "&quot;VD Cryostat 27U Detector Racks&quot; naming drawing (20 N + 20 S racks); "
       "&quot;DTS to TDE White Rabbit Synchronisation Interface&quot; (EDMS 3482906, draft v7.0, 26 Oct 2026).<br><br>"
       "<b>Open items</b><br>"
       "1. The TMS cabling sheet shows 40GbE MTP-12F per crate (64 active fibers, 6-8 MTP12 per rack). "
       "The DAQ baseline drawn here is 25G on an LC pair per crate (16 active fibers, 2 MTP12 per rack); "
       "the sheet needs updating to match.<br>"
       "2. The WR interface document leaves the WR Grand Master / DTS interface location open (cryostat area or CUC). "
       "Drawn here on the detector mezzanine, fed from the DTS fanout rack on the cryostat roof, with the DTS master in the DAQ barracks.<br>"
       "3. Which mezzanine racks host the WR switches, Grand Masters, DTS interface units and sync-check hardware.<br>"
       "4. L1 uplinks land on a Grand Master or its L2 M extension; the exact port map is not drawn.<br>"
       "5. Two 10G Ctrl uplinks per 27U rack are assumed.<br>"
       "6. Purchase ownership assumed, not confirmed: racks (FDC I&amp;I); patch cord from the 1G switch to the 27U patch panel "
       "and the mezzanine Ctrl uplink (FDC I&amp;I); 1G Cu management cables from WR hardware (TDE).<br>"
       "7. Follow-up: who purchases the 2xLC patch cord from the DAQ barracks patch panel to the Ctrl network switch (drawn as DAQ).<br>"
       "8. The patching between the trunk patch panel and the readout switches (top-of-rack patch panels, MTP-12 into 4-way breakout transceivers, per EDMS 3463072) is not drawn in detail.",
       "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=8;", 790, 1460, 960, 380)

ET.indent(mxfile, space="  ")
ET.ElementTree(mxfile).write(OUT, encoding="unicode")
print(f"Wrote {OUT}")
