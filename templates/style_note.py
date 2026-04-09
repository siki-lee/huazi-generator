"""
风格7：活泼卡通风 — Written-Regular
圆角矩形绿青渐变底板 + 青蓝发光描边 + 橙黄渐变文字 + 白色粗描边 + 左右星星
"""
from utils.renderer import embed_font, embed_font_by_name
import os
import math

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Written-Regular.ttf')
FONT_FAMILY = 'Written'

PAD_X = 52
PAD_Y = 22


def _star_path(cx, cy, r_outer, r_inner, points=5):
    """生成五角星 SVG path"""
    path = []
    for i in range(points * 2):
        angle = math.pi / points * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        path.append(f"{'M' if i == 0 else 'L'}{x:.2f},{y:.2f}")
    path.append('Z')
    return ' '.join(path)


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6,
              grad_top: str = '#FFE566', grad_bottom: str = '#FF7700',
              bg_color: str = '#5DECD0', outline_color: str = '#CC4400',
              font_override: str = '', **kwargs) -> str:
    char_w = font_size * 0.92
    text_w = len(text) * char_w + max(0, len(text) - 1) * letter_spacing
    star_space = 52          # 左右各留给星星的空间
    w = int(text_w + PAD_X * 2 + star_space * 2)
    h = int(font_size * 1.45 + PAD_Y * 2)
    cx = w / 2
    ty = h / 2 + font_size * 0.36
    rx = h * 0.45            # 圆角半径
    border = 5               # 底板边框厚度

    # 星星位置
    sl_x, sl_y = star_space * 0.5, h / 2
    sr_x, sr_y = w - star_space * 0.5, h / 2
    star_r_out = h * 0.22
    star_r_in  = star_r_out * 0.42

    star_left  = _star_path(sl_x, sl_y, star_r_out, star_r_in)
    star_right = _star_path(sr_x, sr_y, star_r_out, star_r_in)

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>

    <!-- 底板绿青渐变 -->
    <linearGradient id="bg_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#B8F05A"/>
      <stop offset="50%"  stop-color="{bg_color}"/>
      <stop offset="100%" stop-color="#4DD8F0"/>
    </linearGradient>

    <linearGradient id="txt_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{grad_top}"/>
      <stop offset="55%"  stop-color="{grad_top}"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>

    <!-- 青蓝外发光（底板边框辉光） -->
    <filter id="border_glow" x="-8%" y="-15%" width="116%" height="130%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feFlood flood-color="#00E5FF" flood-opacity="0.85" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <!-- 文字发光 -->
    <filter id="txt_glow" x="-10%" y="-20%" width="120%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feFlood flood-color="#FF8800" flood-opacity="0.5" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <!-- 星星发光 -->
    <filter id="star_glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-color="#FFD700" flood-opacity="0.7" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- 青蓝发光外框（比底板略大） -->
  <rect x="-3" y="-3" width="{w+6}" height="{h+6}" rx="{rx+3}"
    fill="none" stroke="#00E5FF" stroke-width="{border+4}"
    filter="url(#border_glow)" opacity="0.9"/>

  <!-- 底板圆角矩形 -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="{rx}"
    fill="url(#bg_grad)"/>

  <!-- 底板内层高光（顶部白色半透明弧） -->
  <ellipse cx="{cx}" cy="{h*0.28}" rx="{w*0.38}" ry="{h*0.18}"
    fill="white" opacity="0.18"/>

  <!-- 青蓝边框线 -->
  <rect x="{border}" y="{border}" width="{w - border*2}" height="{h - border*2}"
    rx="{rx - border}" fill="none"
    stroke="#00D4FF" stroke-width="{border}"/>

  <!-- 左侧星星 -->
  <path d="{star_left}" fill="#FFE500" stroke="#FF9900" stroke-width="1.5"
    filter="url(#star_glow)"/>

  <!-- 右侧星星 -->
  <path d="{star_right}" fill="#FFE500" stroke="#FF9900" stroke-width="1.5"
    filter="url(#star_glow)"/>

  <!-- 文字：深橙外轮廓 -->
  <text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="{outline_color}" stroke="{outline_color}" stroke-width="10"
    stroke-linejoin="round" style="paint-order:stroke fill">{text}</text>

  <text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="url(#txt_grad)" stroke="white" stroke-width="6"
    stroke-linejoin="round" style="paint-order:stroke fill">{text}</text>

  <text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{letter_spacing}"
    fill="url(#txt_grad)" filter="url(#txt_glow)">{text}</text>
</svg>"""
