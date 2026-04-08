"""
风格8：粉彩少女风 — WrittenSC 手写简体中文
粉色渐变底 + 白色文字 + 星星装饰
"""
from utils.renderer import embed_font
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'WrittenSC-Regular.ttf')
FONT_FAMILY = 'WrittenSC'

PAD_X = 44
PAD_Y = 22


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6, **kwargs) -> str:
    char_w = font_size * 0.95
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2)
    h = int(font_size * 1.5 + PAD_Y * 2)
    cx = w / 2
    ty = h / 2 + font_size * 0.36

    font_css = embed_font(FONT_PATH, FONT_FAMILY)

    def star(x, y, r, color, opacity=1.0):
        """生成五角星 SVG path"""
        import math
        pts = []
        for i in range(10):
            angle = math.pi / 5 * i - math.pi / 2
            radius = r if i % 2 == 0 else r * 0.4
            pts.append(f"{x + radius * math.cos(angle):.1f},{y + radius * math.sin(angle):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{color}" opacity="{opacity}"/>'

    stars = '\n  '.join([
        star(18, 18, 9, '#FFD700', 0.9),
        star(w - 22, 14, 7, '#FFD700', 0.8),
        star(w - 14, h - 18, 6, '#FFFFFF', 0.7),
        star(20, h - 16, 5, '#FFE0F0', 0.8),
        star(w * 0.3, 12, 4, '#FFFFFF', 0.6),
        star(w * 0.72, h - 12, 4, '#FFD700', 0.6),
    ])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="pink_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F48FB1"/>
      <stop offset="50%" stop-color="#CE93D8"/>
      <stop offset="100%" stop-color="#F06292"/>
    </linearGradient>
    <filter id="white_glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feFlood flood-color="#FFFFFF" flood-opacity="0.5" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- 粉色渐变底板（圆角） -->
  <rect width="{w}" height="{h}" rx="20" fill="url(#pink_grad)"/>

  <!-- 星星装饰 -->
  {stars}

  <!-- 白色文字 + 发光 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="#FFFFFF"
    filter="url(#white_glow)">{text}</text>
</svg>"""
