"""
风格2：红色冲击风 — kuaikanshijieti 快看世界体
黑底 + 倾斜红色横幅 + 白字
"""
from utils.renderer import embed_font
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'kuaikanshijieti20231213.ttf')
FONT_FAMILY = 'KuaikanShijie'

PAD_X = 48
PAD_Y = 28


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6,
              rotate_angle: int = -2, **kwargs) -> str:  # noqa
    char_w = font_size * 0.95
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2)
    h = int(font_size * 1.6 + PAD_Y * 2)
    cx = w / 2
    cy = h / 2
    ty = cy + font_size * 0.36

    banner_h = int(font_size * 1.3)
    banner_y = int(cy - banner_h / 2)

    font_css = embed_font(FONT_PATH, FONT_FAMILY)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <filter id="grunge" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.065" numOctaves="3" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="3" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- 黑色底板 -->
  <rect width="{w}" height="{h}" rx="8" fill="#111111"/>

  <!-- 红色横幅（倾斜） -->
  <g transform="rotate({rotate_angle}, {cx}, {cy})">
    <rect x="-10" y="{banner_y}" width="{w+20}" height="{banner_h}"
      fill="#CC0000" filter="url(#grunge)"/>
    <!-- 内框细线 -->
    <rect x="4" y="{banner_y + 4}" width="{w - 8}" height="{banner_h - 8}"
      fill="none" stroke="#FF4444" stroke-width="1.5" stroke-opacity="0.5"/>
  </g>

  <!-- 白色文字 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="#FFFFFF"
    filter="url(#shadow)">{text}</text>
</svg>"""
