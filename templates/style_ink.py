"""
风格4：橙色厚重风 — MaShanZheng 马善政毛笔楷书
橙黄渐变圆角底板 + 深橙粗描边外框 + 白色文字 + 深橙文字描边
"""
from utils.renderer import embed_font, embed_font_by_name
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'MaShanZheng-Regular.ttf')
FONT_FAMILY = 'MaShanZheng'

PAD_X = 36
PAD_Y = 18


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6,
              grad_top: str = '#FFE033', grad_bottom: str = '#FF9500',
              bg_color: str = '#D46000', outline_color: str = '#7A2800',
              font_override: str = '', **kwargs) -> str:
    char_w = font_size * 1.0
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2)
    h = int(font_size * 1.4 + PAD_Y * 2)
    cx = w / 2
    ty = h / 2 + font_size * 0.36
    rx = h * 0.48          # 圆角半径，足够圆润
    border_w = 5           # 外框描边厚度

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="bg_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{grad_top}"/>
      <stop offset="55%"  stop-color="{grad_top}"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>
    <filter id="inner_shadow" x="0" y="0" width="100%" height="100%">
      <feGaussianBlur stdDeviation="3" in="SourceAlpha" result="blur"/>
      <feOffset dx="0" dy="3" result="offset"/>
      <feFlood flood-color="#CC6600" flood-opacity="0.3" result="color"/>
      <feComposite in="color" in2="offset" operator="in" result="shadow"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shadow"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="{w}" height="{h}" rx="{rx}" fill="{bg_color}"/>

  <rect x="{border_w}" y="{border_w}"
    width="{w - border_w*2}" height="{h - border_w*2}"
    rx="{rx - border_w}"
    fill="url(#bg_grad)"/>

  <ellipse cx="{cx}" cy="{h * 0.3}" rx="{w * 0.36}" ry="{h * 0.16}"
    fill="white" opacity="0.22"/>

  <text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="white" stroke="white" stroke-width="14"
    stroke-linejoin="round" style="paint-order:stroke fill">{text}</text>

  <text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="{outline_color}" stroke="{outline_color}" stroke-width="2"
    stroke-linejoin="round" style="paint-order:stroke fill">{text}</text>
</svg>"""
