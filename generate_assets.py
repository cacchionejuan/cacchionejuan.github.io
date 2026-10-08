from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
W, H = 1120, 760
PAPER = "#f8fbf8"
INK = "#192d2a"
MUTED = "#526662"
LINE = "#bdcbc5"
GREEN = "#176b55"
LIME = "#c5ef70"
CORAL = "#e17658"
WHITE = "#ffffff"


def font(size, bold=False, mono=False):
    names = []
    if mono:
        names.extend(["consola.ttf", "cour.ttf"])
    elif bold:
        names.extend(["arialbd.ttf", "segoeuib.ttf"])
    else:
        names.extend(["arial.ttf", "segoeui.ttf"])
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def canvas(kicker, title):
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 22, W - 22, H - 22), radius=10, outline=LINE, width=2)
    draw.text((58, 56), kicker, font=font(19, mono=True), fill=GREEN)
    draw.text((58, 103), title, font=font(37, bold=True), fill=INK)
    return image, draw


def box(draw, bounds, title, lines, fill=WHITE, title_color=INK):
    draw.rounded_rectangle(bounds, radius=8, fill=fill, outline=LINE, width=2)
    x1, y1, _, _ = bounds
    draw.text((x1 + 22, y1 + 18), title, font=font(20, bold=True), fill=title_color)
    for i, line in enumerate(lines):
        draw.text((x1 + 22, y1 + 56 + i * 30), line, font=font(16, mono=True), fill=MUTED)


def arrow(draw, start, end, color=GREEN):
    draw.line((start, end), fill=color, width=5)
    x1, y1 = start
    x2, y2 = end
    if x2 >= x1:
        points = [(x2, y2), (x2 - 15, y2 - 10), (x2 - 15, y2 + 10)]
    else:
        points = [(x2, y2), (x2 + 15, y2 - 10), (x2 + 15, y2 + 10)]
    draw.polygon(points, fill=color)


def dashboard_preview():
    image = Image.new("RGB", (W, H), "#dce9e2")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((28, 26, W - 28, H - 26), radius=18, fill=WHITE, outline=LINE, width=2)

    draw.rounded_rectangle((28, 26, W - 28, 112), radius=18, fill=INK)
    draw.rectangle((28, 84, W - 28, 112), fill=INK)
    draw.text((58, 52), "FIELDNOTE  /  OPERATIONS", font=font(21, bold=True), fill=WHITE)
    draw.rounded_rectangle((870, 48, 1045, 84), radius=5, fill="#c5ef70")
    draw.text((887, 57), "SYNTHETIC DEMO", font=font(14, bold=True, mono=True), fill=INK)

    draw.rectangle((28, 112, 246, H - 26), fill="#213c36")
    nav_items = [("OVERVIEW", 166), ("AVAILABILITY", 230), ("INVENTORY", 294), ("TRANSFERS", 358)]
    for label, y in nav_items:
        if label == "OVERVIEW":
            draw.rounded_rectangle((48, y - 8, 226, y + 35), radius=5, fill="#176b55")
        draw.text((66, y), label, font=font(14, bold=True, mono=True), fill=WHITE if label == "OVERVIEW" else "#bfd0c8")
    draw.line((54, 427, 218, 427), fill="#56736a", width=2)
    draw.text((64, 452), "SAMPLE WORKSPACE", font=font(12, mono=True), fill="#bfd0c8")

    draw.text((280, 141), "Inventory overview", font=font(30, bold=True), fill=INK)
    draw.text((281, 181), "A clearer view of what needs attention", font=font(15), fill=MUTED)

    kpis = [("AVAILABILITY", "94.8%", GREEN), ("TRANSFER CANDIDATES", "286", CORAL), ("REVIEW QUEUE", "42", "#416c7a")]
    kpi_x = [280, 540, 800]
    for x, (label, value, accent) in zip(kpi_x, kpis):
        draw.rounded_rectangle((x, 220, x + 236, 330), radius=8, fill="#f4f8f5", outline=LINE, width=2)
        draw.rounded_rectangle((x, 220, x + 7, 330), radius=3, fill=accent)
        draw.text((x + 22, 240), label, font=font(12, mono=True), fill=MUTED)
        draw.text((x + 22, 268), value, font=font(29, bold=True), fill=INK)

    draw.rounded_rectangle((280, 355, 719, 641), radius=8, fill=WHITE, outline=LINE, width=2)
    draw.text((305, 375), "Availability trend", font=font(18, bold=True), fill=INK)
    draw.text((305, 402), "Illustrative monthly series", font=font(13, mono=True), fill=MUTED)
    chart = (326, 445, 685, 594)
    for fraction in (0, .33, .66, 1):
        y = int(chart[1] + fraction * (chart[3] - chart[1]))
        draw.line((chart[0], y, chart[2], y), fill="#e5ece8", width=2)
    values = [0.34, 0.48, 0.43, 0.61, 0.56, 0.76, 0.72, 0.88]
    points = []
    for i, value in enumerate(values):
        x = int(chart[0] + i * (chart[2] - chart[0]) / (len(values) - 1))
        y = int(chart[3] - value * (chart[3] - chart[1]))
        points.append((x, y))
    draw.line(points, fill=GREEN, width=5, joint="curve")
    for point in points:
        x, y = point
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=LIME, outline=GREEN, width=2)
    for i, label in enumerate(("W1", "W2", "W3", "W4")):
        draw.text((chart[0] + i * 116, 605), label, font=font(11, mono=True), fill=MUTED)

    draw.rounded_rectangle((741, 355, 1058, 641), radius=8, fill="#f4f8f5", outline=LINE, width=2)
    draw.text((764, 375), "Action queue", font=font(18, bold=True), fill=INK)
    draw.text((764, 402), "SAMPLE ITEMS", font=font(12, mono=True), fill=MUTED)
    queue = [("ITEM-0472", "Review"), ("ITEM-1120", "Balance"), ("ITEM-2054", "Review")]
    for i, (item, action) in enumerate(queue):
        y = 447 + i * 57
        draw.line((764, y - 8, 1036, y - 8), fill=LINE, width=1)
        draw.text((764, y + 3), item, font=font(13, mono=True), fill=INK)
        draw.text((764, y + 25), action.upper(), font=font(10, mono=True), fill=GREEN if action == "Balance" else CORAL)
        draw.text((982, y + 8), "OPEN", font=font(10, mono=True), fill=MUTED)

    draw.text((280, 674), "CONCEPT UI  /  ALL VALUES AND LABELS ARE SYNTHETIC", font=font(13, mono=True), fill=MUTED)
    image.save(OUT / "dashboard-preview.png", optimize=True)


def report_pipeline():
    image, draw = canvas("03 / REPORTING WORKFLOW", "From refresh to review")
    stages = [
        ((55, 292, 290, 465), "Refresh sources", ["BI + SQL", "validated inputs"]),
        ((331, 292, 565, 465), "Shared cache", ["reusable", "data snapshot"]),
        ((606, 292, 839, 465), "Build analysis", ["health metrics", "visual summary"]),
        ((879, 292, 1065, 465), "Tailored deck", ["account +", "division"]),
    ]
    for bounds, title, lines in stages:
        fill = "#c5ef70" if title == "Build analysis" else "#e6eee9"
        box(draw, bounds, title, lines, fill=fill)
    arrow(draw, (294, 378), (326, 378))
    arrow(draw, (569, 378), (601, 378))
    arrow(draw, (843, 378), (874, 378))
    draw.text((58, 556), "REPEATABLE INPUTS", font=font(13, mono=True), fill=GREEN)
    draw.text((58, 590), "REUSABLE CALCULATIONS", font=font(13, mono=True), fill=CORAL)
    draw.text((58, 660), "CONCEPTUAL PROCESS  /  NO CUSTOMER DATA OR SOURCE NAMES", font=font(14, mono=True), fill=MUTED)
    image.save(OUT / "report-pipeline.png", optimize=True)


def regional_model():
    image, draw = canvas("04 / DATA ARCHITECTURE", "Partition before consolidating")
    region_boxes = [
        ((55, 245, 255, 350), "Region A", ["source slice"]),
        ((55, 385, 255, 490), "Region B", ["source slice"]),
        ((55, 525, 255, 630), "Region C", ["source slice"]),
    ]
    for bounds, title, lines in region_boxes:
        box(draw, bounds, title, lines, fill="#e6eee9")
    box(draw, (365, 355, 665, 515), "Deduplicate + stage", ["materialized bridge", "join-ready keys"], fill="#c5ef70")
    box(draw, (780, 245, 1055, 390), "Aggregate model", ["reusable metrics", "smaller payload"])
    box(draw, (780, 455, 1055, 600), "BI reporting", ["interactive view", "governed access"])
    for y in (298, 438, 578):
        arrow(draw, (260, y), (355, 420))
    arrow(draw, (669, 405), (773, 318))
    arrow(draw, (915, 394), (915, 449))
    draw.text((58, 680), "ILLUSTRATIVE REGIONS  /  PROCESSING BOUNDARIES ARE THE DESIGN", font=font(13, mono=True), fill=MUTED)
    image.save(OUT / "regional-model.png", optimize=True)


def architecture():
    image, draw = canvas("01 / SYSTEMS MAP", "Local workflow integration")
    box(draw, (58, 280, 315, 465), "Assistant", ["MCP client", "tool request"], fill="#e6eee9")
    box(draw, (425, 250, 710, 495), "MCP server", ["Node.js / stdio", "Zod validation", "workflow rules"], fill="#c5ef70")
    box(draw, (822, 192, 1058, 345), "Microsoft Graph", ["Outlook", "Planner / Teams"])
    box(draw, (822, 405, 1058, 558), "Browser tasks", ["DPM workflows", "local session"])
    arrow(draw, (318, 372), (420, 372))
    arrow(draw, (713, 310), (815, 270))
    arrow(draw, (713, 430), (815, 480))
    draw.text((58, 660), "CONCEPTUAL ONLY  /  NO INTERNAL ENDPOINTS OR COMPANY DATA", font=font(15, mono=True), fill=MUTED)
    image.save(OUT / "architecture.png", optimize=True)


def sql_flow():
    image, draw = canvas("02 / QUERY DESIGN", "Normalize filters once")
    labels = [
        ((55, 278, 292, 465), "Input list", ["PN-001, PN-002", "PN-003, ..."]),
        ((330, 278, 552, 465), "Split + trim", ["one value", "per row"]),
        ((590, 278, 812, 465), "Semi-join", ["match keys", "without fan-out"]),
        ((850, 278, 1065, 465), "Result", ["filtered rows", "synthetic data"]),
    ]
    for bounds, title, lines in labels:
        box(draw, bounds, title, lines, fill="#e6eee9" if title != "Semi-join" else "#c5ef70")
    arrow(draw, (296, 372), (324, 372))
    arrow(draw, (556, 372), (584, 372))
    arrow(draw, (816, 372), (844, 372))
    draw.text((58, 660), "PATTERN: PARSE INPUT ONCE  ->  JOIN AGAINST SOURCE", font=font(15, mono=True), fill=MUTED)
    image.save(OUT / "sql-filtering.png", optimize=True)


def inventory():
    image, draw = canvas("03 / ILLUSTRATIVE DATA", "Inventory health snapshot")
    draw.text((58, 172), "Synthetic categories for layout demonstration only", font=font(18), fill=MUTED)
    rows = [("Active", 58, GREEN), ("Excess", 23, CORAL), ("New stock", 12, "#718b80"), ("Zero sales", 7, INK)]
    x_label, x_bar, bar_w = 58, 285, 675
    for i, (label, value, color) in enumerate(rows):
        y = 250 + i * 92
        draw.text((x_label, y + 5), label, font=font(22, bold=True), fill=INK)
        draw.rounded_rectangle((x_bar, y, x_bar + bar_w, y + 38), radius=5, fill="#e6eee9")
        draw.rounded_rectangle((x_bar, y, x_bar + int(bar_w * value / 100), y + 38), radius=5, fill=color)
        draw.text((x_bar + bar_w + 24, y + 3), f"{value}%", font=font(21, mono=True), fill=INK)
    draw.text((58, 660), "MOCK VALUES  /  NOT A JOHN DEERE REPORT", font=font(15, mono=True), fill=MUTED)
    image.save(OUT / "inventory-sample.png", optimize=True)


dashboard_preview()
report_pipeline()
regional_model()
architecture()
sql_flow()
inventory()
print(f"Generated {len(list(OUT.glob('*.png')))} synthetic portfolio images in {OUT}")