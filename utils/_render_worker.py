
import sys, re
from playwright.sync_api import sync_playwright

svg_file = sys.argv[1]
out_file = sys.argv[2]
scale = float(sys.argv[3])

with open(svg_file, 'r', encoding='utf-8') as f:
    svg_string = f.read()

w = h = 400
m = re.search(r'<svg[^>]*\swidth="(\d+)"[^>]*\sheight="(\d+)"', svg_string)
if m:
    w, h = int(m.group(1)), int(m.group(2))
vw, vh = int(w * scale), int(h * scale)

html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:transparent;width:{vw}px;height:{vh}px;overflow:hidden}}</style>
</head>
<body>
<div style="transform:scale({scale});transform-origin:top left;width:{w}px;height:{h}px">
{svg_string}
</div>
</body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': vw, 'height': vh})
    page.set_content(html, wait_until='networkidle')
    page.wait_for_timeout(800)
    png = page.screenshot(type='png', omit_background=True,
                          clip={'x': 0, 'y': 0, 'width': vw, 'height': vh})
    browser.close()

with open(out_file, 'wb') as f:
    f.write(png)
