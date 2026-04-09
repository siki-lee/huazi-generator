"""
风格3：清新自然风 — 昆明海鸥体
粉绿渐变多边形底板 + 深绿文字 + 小花装饰
"""
from utils.renderer import embed_font, embed_font_by_name
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'KunmingHaiyou.ttf')
FONT_FAMILY = 'KunmingHaiOu'

PAD_X = 48
PAD_Y = 24


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 8,
              grad_top: str = '#FFD6E0', grad_bottom: str = '#DCEDC8',
              outline_color: str = '#2E7D32', font_override: str = '', **kwargs) -> str:
    char_w = font_size * 0.95
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2 + 40)  # 右侧留小花空间
    h = int(font_size * 1.5 + PAD_Y * 2)
    cx = w / 2 - 10
    ty = h / 2 + font_size * 0.35

    # 不规则多边形底板
    p1 = f"0,{h*0.15}"
    p2 = f"{w*0.05},0"
    p3 = f"{w},0"
    p4 = f"{w},{h}"
    p5 = f"0,{h}"
    polygon_pts = f"{p1} {p2} {p3} {p4} {p5}"

    # 小花位置（右上角）
    fx = w - 26
    fy = 26

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="bg_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{grad_top}"/>
      <stop offset="50%" stop-color="#FFF3E0"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>
    <filter id="txt_shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="2" flood-color="{outline_color}" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- 底板多边形 -->
  <polygon points="{polygon_pts}" fill="url(#bg_grad)"/>

  <!-- 小花装饰 -->
  <g transform="translate({fx},{fy})">
    <!-- 花瓣 -->
    <ellipse cx="0" cy="-11" rx="5" ry="9" fill="#FFD700" opacity="0.9"/>
    <ellipse cx="0" cy="11" rx="5" ry="9" fill="#FFD700" opacity="0.9"/>
    <ellipse cx="-11" cy="0" rx="9" ry="5" fill="#FFD700" opacity="0.9"/>
    <ellipse cx="11" cy="0" rx="9" ry="5" fill="#FFD700" opacity="0.9"/>
    <ellipse cx="-8" cy="-8" rx="5" ry="9" fill="#FFC107" opacity="0.8" transform="rotate(45,{-8},{-8})"/>
    <ellipse cx="8" cy="-8" rx="5" ry="9" fill="#FFC107" opacity="0.8" transform="rotate(-45,{8},{-8})"/>
    <ellipse cx="-8" cy="8" rx="5" ry="9" fill="#FFC107" opacity="0.8" transform="rotate(-45,{-8},{8})"/>
    <ellipse cx="8" cy="8" rx="5" ry="9" fill="#FFC107" opacity="0.8" transform="rotate(45,{8},{8})"/>
    <!-- 花心 -->
    <circle cx="0" cy="0" r="6" fill="#FF8F00"/>
    <!-- 叶片 -->
    <ellipse cx="-18" cy="10" rx="7" ry="4" fill="#66BB6A" opacity="0.9" transform="rotate(-30,{-18},{10})"/>
  </g>

  <!-- 文字 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="{outline_color}"
    filter="url(#txt_shadow)">{text}</text>
</svg>"""
