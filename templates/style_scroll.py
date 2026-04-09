"""
风格6：双色错落风 — StudyMingTW 繁体明朝体
透明底 + 单行文字左半绿右半橙 + 闪光星 + 底部波浪色块
"""
from utils.renderer import embed_font, embed_font_by_name
import os
import math

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'StudyMingTW-Regular.ttf')
FONT_FAMILY = 'StudyMingTW'


def _star4(cx, cy, r):
    pts = []
    for i in range(8):
        angle = math.pi / 4 * i - math.pi / 4
        radius = r if i % 2 == 0 else r * 0.2
        pts.append(f"{cx + radius*math.cos(angle):.2f},{cy + radius*math.sin(angle):.2f}")
    return '<polygon points="' + ' '.join(pts) + '" fill="white" opacity="0.95"/>'


def build_svg(text: str, font_size: int = 80, letter_spacing: int = 6,
              grad_top: str = '#3DD68C', grad_bottom: str = '#00B894',
              outline_color: str = '#FFAA00', font_override: str = '', **kwargs) -> str:
    mid = math.ceil(len(text) / 2)
    line1 = text[:mid]   # 左半：绿色
    line2 = text[mid:]   # 右半：橙色

    char_w = font_size * 1.02
    ls = letter_spacing

    w1 = len(line1) * char_w + max(0, len(line1) - 1) * ls
    w2 = len(line2) * char_w + max(0, len(line2) - 1) * ls

    pad = 40
    total_text_w = w1 + w2 + ls  # 两段之间保留一个字间距
    canvas_w = int(total_text_w + pad * 2)
    wave_h = int(font_size * 0.38)
    canvas_h = int(font_size * 1.45 + pad * 1.2 + wave_h)

    ty = int(pad * 0.6 + font_size * 1.0)
    x1 = pad                      # 左半起始 x
    x2 = int(pad + w1 + ls)       # 右半起始 x

    wy = canvas_h - wave_h

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    stars = '\n  '.join([
        _star4(x1 + w1 * 0.08,  ty - font_size * 0.72, font_size * 0.13),
        _star4(x1 + w1 * 0.85,  ty - font_size * 0.55, font_size * 0.10),
        _star4(x2 + w2 * 0.90,  ty - font_size * 0.65, font_size * 0.14),
        _star4(x2 + w2 * 0.5,   ty - font_size * 0.88, font_size * 0.07),
        _star4(canvas_w - pad*0.4, ty - font_size * 0.30, font_size * 0.08),
    ])

    wave_pts = (
        f"0,{canvas_h} "
        f"0,{wy + wave_h*0.4} "
        f"{canvas_w*0.12},{wy} "
        f"{canvas_w*0.28},{wy + wave_h*0.25} "
        f"{canvas_w*0.45},{wy - wave_h*0.1} "
        f"{canvas_w*0.62},{wy + wave_h*0.3} "
        f"{canvas_w*0.78},{wy} "
        f"{canvas_w*0.92},{wy + wave_h*0.2} "
        f"{canvas_w},{wy + wave_h*0.45} "
        f"{canvas_w},{canvas_h}"
    )

    def txt_layer(x, text, fill, stroke_color, stroke_w, filt=''):
        f = f'filter="url(#{filt})"' if filt else ''
        return f"""<text x="{x}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="start" letter-spacing="{ls}"
    fill="{fill}" stroke="{stroke_color}" stroke-width="{stroke_w}"
    stroke-linejoin="round" style="paint-order:stroke fill" {f}>{text}</text>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}"
     viewBox="0 0 {canvas_w} {canvas_h}">
  <defs>
    <style>{font_css}</style>
    <linearGradient id="green_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#AAFFA0"/>
      <stop offset="45%"  stop-color="{grad_top}"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>
    <linearGradient id="orange_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#FFE566"/>
      <stop offset="50%"  stop-color="{outline_color}"/>
      <stop offset="100%" stop-color="#FF7700"/>
    </linearGradient>
    <linearGradient id="wave_grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#C6F135"/>
      <stop offset="50%"  stop-color="#FFE033"/>
      <stop offset="100%" stop-color="#FFB300"/>
    </linearGradient>
    <filter id="green_glow" x="-12%" y="-20%" width="124%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feFlood flood-color="#00E676" flood-opacity="0.55" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="orange_glow" x="-12%" y="-20%" width="124%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feFlood flood-color="#FF9100" flood-opacity="0.55" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- 底部波浪 -->
  <polygon points="{wave_pts}" fill="url(#wave_grad)" opacity="0.92"/>

  <!-- 左半（绿色）：深绿轮廓 → 白色描边 → 绿色主体 -->
  {txt_layer(x1, line1, '#006644', '#006644', 13)}
  {txt_layer(x1, line1, 'url(#green_grad)', 'white', 6)}
  {txt_layer(x1, line1, 'url(#green_grad)', 'none', 0, 'green_glow')}

  <!-- 右半（橙色）：深橙轮廓 → 白色描边 → 橙色主体 -->
  {txt_layer(x2, line2, '#B84500', '#B84500', 13)}
  {txt_layer(x2, line2, 'url(#orange_grad)', 'white', 6)}
  {txt_layer(x2, line2, 'url(#orange_grad)', 'none', 0, 'orange_glow')}

  <!-- 闪光星 -->
  {stars}
</svg>"""
