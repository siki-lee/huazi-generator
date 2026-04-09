"""
风格5：花朵粉彩风 — StudyMingCN 仿明朝衬线体（简体）
透明底 + 粉橙渐变文字 + 白色厚外描边 + 绿色轮廓线 + 两侧雏菊花装饰
"""
from utils.renderer import embed_font, embed_font_by_name
import os
import math

FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'StudyMingCN-Regular.ttf')
FONT_FAMILY = 'StudyMingCN'


def _daisy(cx, cy, r, petals=8):
    """生成雏菊 SVG（黄色花瓣 + 白色边 + 绿色茎圆 + 黄色花心）"""
    petal_parts = []
    for i in range(petals):
        angle = 2 * math.pi / petals * i
        px = cx + r * 0.72 * math.cos(angle)
        py = cy + r * 0.72 * math.sin(angle)
        pr = r * 0.38
        petal_parts.append(
            f'<ellipse cx="{px:.2f}" cy="{py:.2f}" rx="{pr:.2f}" ry="{pr*0.68:.2f}" '
            f'fill="#FFFB6E" stroke="white" stroke-width="1.2" '
            f'transform="rotate({math.degrees(angle):.1f},{px:.2f},{py:.2f})"/>'
        )
    center = (
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.32:.2f}" fill="#FFE000" stroke="#FFAA00" stroke-width="1.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.16:.2f}" fill="#FF9900"/>'
    )
    return '\n  '.join(petal_parts) + '\n  ' + center


def build_svg(text: str, font_size: int = 72, letter_spacing: int = 6,
              grad_top: str = '#FFB3C6', grad_bottom: str = '#FF4D6D',
              outline_color: str = '#3DB85A', glow_color: str = '#FF6BAE',
              font_override: str = '', **kwargs) -> str:
    char_w = font_size * 0.98
    ls = letter_spacing
    text_w = len(text) * char_w + max(0, len(text) - 1) * ls

    flower_r = font_size * 0.42
    pad_x = int(flower_r * 2.6 + 28)   # 左右给花朵留空间
    pad_y = int(font_size * 0.28)

    w = int(text_w + pad_x * 2)
    h = int(font_size * 1.55 + pad_y * 2)
    cx = w / 2
    ty = pad_y + font_size * 1.1

    ff = FONT_FAMILY
    font_css = embed_font_by_name(font_override, ff) if font_override else embed_font(FONT_PATH, ff)

    # 花朵位置：左侧、右侧各一朵，偏上一点
    fl_x = flower_r * 1.1
    fl_y = h * 0.48
    fr_x = w - flower_r * 1.1
    fr_y = h * 0.48

    daisy_left  = _daisy(fl_x, fl_y, flower_r)
    daisy_right = _daisy(fr_x, fr_y, flower_r)

    # 绿色茎叶小圆（花托）
    stem_r = flower_r * 0.28

    def txt(fill, stroke_c, stroke_w, filt=''):
        f = f'filter="url(#{filt})"' if filt else ''
        return f"""<text x="{cx}" y="{ty}"
    font-family="{ff}" font-size="{font_size}" font-weight="900"
    text-anchor="middle" letter-spacing="{ls}"
    fill="{fill}" stroke="{stroke_c}" stroke-width="{stroke_w}"
    stroke-linejoin="round" style="paint-order:stroke fill" {f}>{text}</text>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}">
  <defs>
    <style>{font_css}</style>

    <!-- 粉橙渐变（文字主体） -->
    <linearGradient id="pink_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{grad_top}"/>
      <stop offset="40%"  stop-color="{grad_top}"/>
      <stop offset="100%" stop-color="{grad_bottom}"/>
    </linearGradient>

    <filter id="white_glow" x="-15%" y="-25%" width="130%" height="150%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feFlood flood-color="white" flood-opacity="0.9" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <filter id="pink_glow" x="-12%" y="-20%" width="124%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-color="{glow_color}" flood-opacity="0.6" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- 花朵：左 -->
  <!-- 花托绿圆 -->
  <circle cx="{fl_x:.1f}" cy="{fl_y:.1f}" r="{flower_r*0.52:.2f}"
    fill="#5BC85B" stroke="#3A9C3A" stroke-width="1.5"/>
  {daisy_left}

  <!-- 花朵：右 -->
  <circle cx="{fr_x:.1f}" cy="{fr_y:.1f}" r="{flower_r*0.52:.2f}"
    fill="#5BC85B" stroke="#3A9C3A" stroke-width="1.5"/>
  {daisy_right}

  <!-- 文字：白色厚底（产生白色光晕外描边） -->
  {txt('white', 'white', int(font_size * 0.32), 'white_glow')}

  <!-- 文字：绿色轮廓线 -->
  {txt('none', outline_color, int(font_size * 0.12))}

  <!-- 文字：粉橙渐变主体 + 白色描边 -->
  {txt('url(#pink_grad)', 'white', int(font_size * 0.07))}

  <!-- 文字：粉色发光层 -->
  {txt('url(#pink_grad)', 'none', 0, 'pink_glow')}
</svg>"""
