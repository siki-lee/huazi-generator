"""
SVG → PNG 渲染工具（使用 Playwright Chromium）
云端自动安装浏览器，本地直接使用已安装的浏览器。
"""
import base64
import re
import subprocess
import sys

_browser_ready = False


def embed_font(font_path: str, font_family: str) -> str:
    with open(font_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"""
    @font-face {{
        font-family: '{font_family}';
        src: url('data:font/truetype;base64,{b64}') format('truetype');
    }}
    """


def _ensure_browser():
    """确保 Chromium 已安装。首次调用时运行 playwright install。"""
    subprocess.run(
        [sys.executable, '-m', 'playwright', 'install', 'chromium', '--with-deps'],
        check=True,
        capture_output=True,
    )


def svg_to_png(svg_string: str, scale: float = 2.0) -> bytes:
    """通过 Playwright Chromium 将 SVG 渲染为透明背景 PNG。"""
    global _browser_ready
    if not _browser_ready:
        _ensure_browser()
        _browser_ready = True

    from playwright.sync_api import sync_playwright

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
        png = page.screenshot(type='png', omit_background=True,
                              clip={'x': 0, 'y': 0, 'width': vw, 'height': vh})
        browser.close()
    return png
