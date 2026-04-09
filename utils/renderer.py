"""
SVG → PNG 渲染工具
- 优先：Playwright Chromium 子进程（效果完整，本地使用）
- 降级：cairosvg 直接渲染（无需浏览器，云端兼容）
"""
import base64
import os
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


def _svg_to_png_playwright(svg_string: str, scale: float) -> bytes:
    """用 Playwright 子进程渲染（本地高质量）。"""
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


def _svg_to_png_cairo(svg_string: str, scale: float) -> bytes:
    """用 cairosvg 渲染（云端兼容，无需浏览器）。"""
    import cairosvg
    return cairosvg.svg2png(
        bytestring=svg_string.encode('utf-8'),
        scale=scale,
        background_color=None,
    )


def svg_to_png(svg_string: str, scale: float = 2.0) -> bytes:
    """将 SVG 渲染为透明背景 PNG，自动选择最佳引擎。"""
    # 先尝试 Playwright（本地效果完整）
    try:
        result = _svg_to_png_playwright(svg_string, scale)
        # 如果渲染结果太小（空图），认为失败
        if len(result) > 1000:
            return result
    except Exception:
        pass

    # 降级到 cairosvg（云端）
    return _svg_to_png_cairo(svg_string, scale)
