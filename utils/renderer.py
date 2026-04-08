"""
SVG → PNG 渲染工具（使用 Playwright Chromium）
启动本地 HTTP 服务器提供字体文件，避免 base64 嵌入或 file:// 限制。
"""
import base64
import os
import re
import subprocess
import sys
import threading
import http.server
import socketserver

_browser_ready = False
_font_server = None
_font_server_port = 17321
_font_root = os.path.join(os.path.dirname(__file__), '..', 'fonts')


def _start_font_server():
    """启动本地字体 HTTP 服务器（只启动一次）。"""
    global _font_server
    if _font_server is not None:
        return

    font_dir = os.path.abspath(_font_root)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=font_dir, **kwargs)
        def log_message(self, *args):
            pass  # 静默日志

    _font_server = socketserver.TCPServer(('127.0.0.1', _font_server_port), Handler)
    t = threading.Thread(target=_font_server.serve_forever, daemon=True)
    t.start()


def embed_font(font_path: str, font_family: str) -> str:
    """生成 @font-face CSS，通过本地 HTTP 服务器加载字体。"""
    filename = os.path.basename(font_path)
    import urllib.parse
    encoded = urllib.parse.quote(filename)
    uri = f"http://127.0.0.1:{_font_server_port}/{encoded}"
    return f"""
    @font-face {{
        font-family: '{font_family}';
        src: url('{uri}') format('truetype');
    }}
    """


def _ensure_browser():
    """确保 Chromium 已安装。"""
    subprocess.run(
        [sys.executable, '-m', 'playwright', 'install', 'chromium'],
        check=True,
        capture_output=True,
    )


def svg_to_png(svg_string: str, scale: float = 2.0) -> bytes:
    """通过 Playwright Chromium 将 SVG 渲染为透明背景 PNG。"""
    global _browser_ready
    if not _browser_ready:
        _ensure_browser()
        _start_font_server()
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
<script>
document.fonts.ready.then(function() {{
  document.title = 'FONTS_READY';
}});
</script>
</body></html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': vw, 'height': vh})
        page.set_content(html, wait_until='networkidle')
        page.wait_for_function("document.title === 'FONTS_READY'", timeout=15000)
        png = page.screenshot(type='png', omit_background=True,
                              clip={'x': 0, 'y': 0, 'width': vw, 'height': vh})
        browser.close()
    return png
