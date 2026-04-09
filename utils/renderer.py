"""
SVG → PNG 渲染工具（使用 Playwright Chromium）
base64 嵌入字体，子进程渲染避免超时和模块缓存问题。
"""
import base64
import os
import re
import subprocess
import sys
import tempfile

_chromium_installed = False


def embed_font(font_path: str, font_family: str) -> str:
    """生成 @font-face CSS，base64 嵌入字体。"""
    with open(font_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"""
    @font-face {{
        font-family: '{font_family}';
        src: url('data:font/truetype;base64,{b64}') format('truetype');
    }}
    """


def embed_font_by_name(font_name: str, font_family: str) -> str:
    """按字体显示名称嵌入字体（用于 font_override）。"""
    from utils.fonts import get_font_path
    return embed_font(get_font_path(font_name), font_family)


def _ensure_browser():
    global _chromium_installed
    if _chromium_installed:
        return
    subprocess.run(
        [sys.executable, '-m', 'playwright', 'install', 'chromium'],
        check=True, capture_output=True,
    )
    _chromium_installed = True


# 子进程渲染脚本
_RENDER_SCRIPT = """
import sys, re
from playwright.sync_api import sync_playwright

svg_file = sys.argv[1]
out_file = sys.argv[2]
scale = float(sys.argv[3])

with open(svg_file, 'r', encoding='utf-8') as f:
    svg_string = f.read()

w = h = 400
m = re.search(r'<svg[^>]*\\swidth="(\\d+)"[^>]*\\sheight="(\\d+)"', svg_string)
if m:
    w, h = int(m.group(1)), int(m.group(2))
vw, vh = int(w * scale), int(h * scale)

html = f\"\"\"<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:transparent;width:{vw}px;height:{vh}px;overflow:hidden}}</style>
</head>
<body>
<div style="transform:scale({scale});transform-origin:top left;width:{w}px;height:{h}px">
{svg_string}
</div>
</body></html>\"\"\"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={{'width': vw, 'height': vh}})
    page.set_content(html, wait_until='networkidle')
    page.wait_for_timeout(800)
    png = page.screenshot(type='png', omit_background=True,
                          clip={{'x': 0, 'y': 0, 'width': vw, 'height': vh}})
    browser.close()

with open(out_file, 'wb') as f:
    f.write(png)
"""


def svg_to_png(svg_string: str, scale: float = 2.0) -> bytes:
    """通过子进程 Playwright Chromium 将 SVG 渲染为透明背景 PNG。"""
    _ensure_browser()

    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False, mode='w', encoding='utf-8') as sf:
        sf.write(svg_string)
        svg_path = sf.name

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as pf:
        png_path = pf.name

    script_path = os.path.join(os.path.dirname(__file__), '_render_worker.py')

    try:
        subprocess.run(
            [sys.executable, script_path, svg_path, png_path, str(scale)],
            check=True, timeout=60,
        )
        with open(png_path, 'rb') as f:
            return f.read()
    finally:
        os.unlink(svg_path)
        try:
            os.unlink(png_path)
        except FileNotFoundError:
            pass
