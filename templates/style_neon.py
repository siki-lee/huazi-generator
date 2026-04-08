"""
风格9：霓虹发光风 — ChillCalligraphyChunQiu 春秋书法体
深色底 + 青紫霓虹发光描边 + 荧光渐变文字
"""
from utils.renderer import embed_font
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'ChillCalligraphyChunQiu_QiuHong.ttf')
FONT_FAMILY = 'ChillCalligraphy'

PAD_X = 44
PAD_Y = 24


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6, **kwargs) -> str:
    char_w = font_size * 1.0
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    w = int(text_w + PAD_X * 2)
    h = int(font_size * 1.6 + PAD_Y * 2)
    cx = w / 2
    ty = h / 2 + font_size * 0.38

    font_css = embed_font(FONT_PATH, FONT_FAMILY)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="neon_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00FFFF"/>
      <stop offset="50%" stop-color="#BF5FFF"/>
      <stop offset="100%" stop-color="#00FFAA"/>
    </linearGradient>
    <!-- 青色外发光 -->
    <filter id="cyan_glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur1"/>
      <feFlood flood-color="#00FFFF" flood-opacity="0.7" result="cyan"/>
      <feComposite in="cyan" in2="blur1" operator="in" result="glow1"/>
      <feMerge><feMergeNode in="glow1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <!-- 紫色外发光（范围更大） -->
    <filter id="purple_glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur2"/>
      <feFlood flood-color="#BF5FFF" flood-opacity="0.4" result="purple"/>
      <feComposite in="purple" in2="blur2" operator="in" result="glow2"/>
      <feMerge><feMergeNode in="glow2"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- 深色底板 -->
  <rect width="{w}" height="{h}" rx="8" fill="#0D0D1A"/>
  <!-- 底部扫光条 -->
  <rect x="0" y="{h-4}" width="{w}" height="4" rx="2" fill="#BF5FFF" opacity="0.4"/>
  <rect x="0" y="0" width="{w}" height="4" rx="2" fill="#00FFFF" opacity="0.3"/>

  <!-- 紫色大光晕层 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="#BF5FFF" opacity="0.5"
    filter="url(#purple_glow)">{text}</text>

  <!-- 青色描边发光层 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="none"
    stroke="#00FFFF" stroke-width="2.5"
    filter="url(#cyan_glow)">{text}</text>

  <!-- 荧光渐变主文字 -->
  <text x="{cx}" y="{ty}"
    font-family="{FONT_FAMILY}" font-size="{font_size}"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="url(#neon_grad)">{text}</text>
</svg>"""
