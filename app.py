"""
花字生成器 — Streamlit 主程序（9种风格）
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.renderer import svg_to_png
from utils.fonts import FONT_NAMES
from templates.style_orange import build_svg as svg_orange
from templates.style_red    import build_svg as svg_red
from templates.style_fresh  import build_svg as svg_fresh
from templates.style_ink    import build_svg as svg_ink
from templates.style_gold   import build_svg as svg_gold
from templates.style_scroll import build_svg as svg_scroll
from templates.style_note   import build_svg as svg_note
from templates.style_pink   import build_svg as svg_pink
from templates.style_neon   import build_svg as svg_neon

# ── 页面配置 ──────────────────────────────────────────────────
st.set_page_config(
    page_title='花字生成器',
    page_icon='🎨',
    layout='centered',
)

# ── 风格注册表 ────────────────────────────────────────────────
STYLES = {
    '橙黄活泼风': {
        'icon': '🟠', 'desc': '趣味互动 · 低年级',
        'font': 'KeinannMaruPOP 圆体',
        'builder': svg_orange,
        'default_spacing': 4,
        'color_params': {
            'grad_top':      ('#FFD44F', '渐变顶色'),
            'grad_bottom':   ('#FF8C00', '渐变底色'),
            'outline_color': ('#B85000', '轮廓颜色'),
        },
    },
    '红色冲击风': {
        'icon': '🔴', 'desc': '考试冲刺 · 重点强调',
        'font': '快看世界体',
        'builder': svg_red,
        'default_spacing': 6,
        'color_params': {
            'grad_top':  ('#CC0000', '横幅颜色'),
            'bg_color':  ('#111111', '背景颜色'),
        },
    },
    '清新自然风': {
        'icon': '🌿', 'desc': '作文 · 文学主题',
        'font': '昆明海鸥体',
        'builder': svg_fresh,
        'default_spacing': 8,
        'color_params': {
            'grad_top':      ('#FFD6E0', '背景渐变顶色'),
            'grad_bottom':   ('#DCEDC8', '背景渐变底色'),
            'outline_color': ('#2E7D32', '文字颜色'),
        },
    },
    '橙色厚重风': {
        'icon': '🟡', 'desc': '重点原则 · 规则强调',
        'font': '马善政毛笔楷书',
        'builder': svg_ink,
        'default_spacing': 6,
        'color_params': {
            'grad_top':      ('#FFE033', '渐变顶色'),
            'grad_bottom':   ('#FF9500', '渐变底色'),
            'bg_color':      ('#D46000', '外框颜色'),
            'outline_color': ('#7A2800', '文字颜色'),
        },
    },
    '花朵粉彩风': {
        'icon': '🌸', 'desc': '趣味 · 揭秘 · 互动主题',
        'font': '明朝仿宋（简体）',
        'builder': svg_gold,
        'default_spacing': 6,
        'color_params': {
            'grad_top':      ('#FFB3C6', '渐变顶色'),
            'grad_bottom':   ('#FF4D6D', '渐变底色'),
            'outline_color': ('#3DB85A', '轮廓颜色'),
            'glow_color':    ('#FF6BAE', '发光颜色'),
        },
    },
    '双色错落风': {
        'icon': '🌈', 'desc': '篇法 · 技巧 · 双重概念',
        'font': '明朝仿宋（繁体）',
        'builder': svg_scroll,
        'default_spacing': 6,
        'color_params': {
            'grad_top':      ('#3DD68C', '左半渐变顶色'),
            'grad_bottom':   ('#00B894', '左半渐变底色'),
            'outline_color': ('#FFAA00', '右半主色'),
        },
    },
    '活泼卡通风': {
        'icon': '⭐', 'desc': '互动环节 · 趣味标题',
        'font': 'Written 手写体',
        'builder': svg_note,
        'default_spacing': 6,
        'color_params': {
            'grad_top':      ('#FFE566', '文字渐变顶色'),
            'grad_bottom':   ('#FF7700', '文字渐变底色'),
            'bg_color':      ('#5DECD0', '背景颜色'),
            'outline_color': ('#CC4400', '轮廓颜色'),
        },
    },
    '粉彩少女风': {
        'icon': '✨', 'desc': '语文 · 作文 · 美育',
        'font': 'WrittenSC 手写简体',
        'builder': svg_pink,
        'default_spacing': 6,
        'color_params': {
            'grad_top':    ('#F48FB1', '渐变顶色'),
            'grad_bottom': ('#F06292', '渐变底色'),
            'bg_color':    ('#CE93D8', '渐变中间色'),
        },
    },
    '霓虹发光风': {
        'icon': '💜', 'desc': '科技 · 创意 · 趣味',
        'font': '春秋书法体',
        'builder': svg_neon,
        'default_spacing': 6,
        'color_params': {
            'grad_top':   ('#00FFFF', '主光色'),
            'grad_bottom': ('#00FFAA', '渐变底色'),
            'bg_color':   ('#0D0D1A', '背景颜色'),
            'glow_color': ('#BF5FFF', '发光颜色'),
        },
    },
}

STYLE_NAMES = list(STYLES.keys())

# ── 主标题 ────────────────────────────────────────────────────
st.title('🎨 花字生成器')
st.caption('输入文字，选择风格，一键生成课件花字图片')
st.divider()

# ── 输入区 ────────────────────────────────────────────────────
text_input = st.text_input(
    '输入文字',
    value='猜猜他是谁',
    max_chars=12,
    placeholder='建议 2-8 个字符',
)

st.markdown('#### 选择风格')

if 'selected_style' not in st.session_state:
    st.session_state['selected_style'] = STYLE_NAMES[0]

selected_style = st.session_state['selected_style']

for row in range(3):
    cols = st.columns(3)
    for col_i in range(3):
        idx = row * 3 + col_i
        name = STYLE_NAMES[idx]
        info = STYLES[name]
        is_selected = selected_style == name
        border_color = '#FF8C00' if is_selected else '#DDDDDD'
        card_bg = '#FFF8EE' if is_selected else '#FAFAFA'
        with cols[col_i]:
            st.markdown(
                f"""<div style="
                    border: 2.5px solid {border_color};
                    border-radius: 12px;
                    padding: 12px 6px 6px;
                    text-align: center;
                    background: {card_bg};
                    min-height: 88px;
                ">
                    <div style="font-size:26px">{info['icon']}</div>
                    <div style="font-weight:bold;font-size:12px;margin-top:3px">{name}</div>
                    <div style="color:#888;font-size:10px;margin-top:1px">{info['desc']}</div>
                    <div style="color:#aaa;font-size:9px;margin-top:1px">{info['font']}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button('选择', key=f'btn_{name}', use_container_width=True,
                         type='primary' if is_selected else 'secondary'):
                st.session_state['selected_style'] = name
                st.rerun()

selected_style = st.session_state['selected_style']
st.markdown(f'当前选择：**{selected_style}**　　默认字体：*{STYLES[selected_style]["font"]}*')

# ── 高级选项 ──────────────────────────────────────────────────
font_size = 72
letter_spacing = STYLES[selected_style]['default_spacing']
rotate_angle = -2
font_override = ''
color_values = {}

with st.expander('高级选项', expanded=False):
    font_size = st.slider('字号大小', 36, 120, 72, 4)
    letter_spacing = st.slider('字间距', 0, 20, STYLES[selected_style]['default_spacing'], 1)

    # 字体选择
    font_options = ['默认（跟随风格）'] + FONT_NAMES
    selected_font = st.selectbox('字体', font_options, index=0)
    if selected_font != '默认（跟随风格）':
        font_override = selected_font

    if selected_style == '红色冲击风':
        rotate_angle = st.slider('横幅倾斜角度', -8, 0, -2, 1)

    # 颜色选项
    color_params = STYLES[selected_style].get('color_params', {})
    if color_params:
        st.markdown('**颜色设置**')
        param_keys = list(color_params.keys())
        for i in range(0, len(param_keys), 2):
            cols = st.columns(2)
            for j, key in enumerate(param_keys[i:i+2]):
                default, label = color_params[key]
                with cols[j]:
                    color_values[key] = st.color_picker(label, default, key=f'color_{selected_style}_{key}')

st.divider()

# ── 生成 + 预览 ───────────────────────────────────────────────
st.markdown('#### 预览')

CHECKERBOARD = """
<div style="
    background-image:
        linear-gradient(45deg,#ccc 25%,transparent 25%),
        linear-gradient(-45deg,#ccc 25%,transparent 25%),
        linear-gradient(45deg,transparent 75%,#ccc 75%),
        linear-gradient(-45deg,transparent 75%,#ccc 75%);
    background-size:16px 16px;
    background-position:0 0,0 8px,8px -8px,-8px 0;
    background-color:#fff;
    border-radius:12px;
    padding:24px;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:120px;
">
"""

png_bytes = None

if not text_input.strip():
    st.info('请先输入文字内容')
else:
    try:
        builder = STYLES[selected_style]['builder']
        svg = builder(
            text=text_input,
            font_size=font_size,
            letter_spacing=letter_spacing,
            rotate_angle=rotate_angle,
            font_override=font_override,
            **color_values,
        )
        png_bytes = svg_to_png(svg, scale=2.0)

        import base64
        b64 = base64.b64encode(png_bytes).decode()
        st.markdown(
            CHECKERBOARD +
            f'<img src="data:image/png;base64,{b64}" style="max-width:100%;border-radius:6px"/>'
            + '</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f'生成失败：{e}')

st.divider()

# ── 下载 ──────────────────────────────────────────────────────
dl_col, _ = st.columns([1, 2])
with dl_col:
    if png_bytes:
        safe_text = text_input.replace('/', '').replace('\\', '').replace(':', '')
        st.download_button(
            label='📥 下载 PNG',
            data=png_bytes,
            file_name=f'花字_{selected_style}_{safe_text}.png',
            mime='image/png',
            use_container_width=True,
        )
    else:
        st.download_button(
            label='📥 下载 PNG',
            data=b'',
            file_name='花字.png',
            mime='image/png',
            use_container_width=True,
            disabled=True,
        )
