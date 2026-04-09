"""
风格1：橙黄活泼风 — KeinannMaruPOP 圆体
渐变文字 + 多层描边
"""
from utils.renderer import embed_font, embed_font_by_name
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'KeinannMaruPOP.ttf')
FONT_FAMILY = 'KeinannMaruPOP'

PAD_X = 40
PAD_Y = 20


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 4,
              grad_top: str = '#FFD44F', grad_bottom: str = '#FF8C00',
              outline_color: str = '#B85000', font_override: str = '', **kwargs) -> str:
    char_w = font_size * 0.95
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2)
    h = int(font_size * 1.5 + PAD_Y * 2)
    cx = w / 2
    cy = h / 2 + font_size * 0.35

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{grad_top}"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>
    <filter id="outline_dark" x="-15%" y="-15%" width="130%" height="130%">
      <feMorphology operator="dilate" radius="5" in="SourceAlpha" result="expanded"/>
      <feFlood flood-color="{outline_color}" result="color"/>
      <feComposite in="color" in2="expanded" operator="in" result="outline"/>
      <feMerge><feMergeNode in="outline"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="outline_white" x="-15%" y="-15%" width="130%" height="130%">
      <feMorphology operator="dilate" radius="3" in="SourceAlpha" result="expanded"/>
      <feFlood flood-color="#FFFFFF" result="color"/>
      <feComposite in="color" in2="expanded" operator="in" result="outline"/>
      <feMerge><feMergeNode in="outline"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <text x="{cx}" y="{cy}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="{outline_color}"
    filter="url(#outline_dark)"
    style="paint-order: stroke fill;"
    stroke="{outline_color}" stroke-width="9">{text}</text>

  <text x="{cx}" y="{cy}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="url(#grad1)"
    style="paint-order: stroke fill;"
    stroke="white" stroke-width="6">{text}</text>

  <text x="{cx}" y="{cy}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="url(#grad1)">{text}</text>
</svg>"""
