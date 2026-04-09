# 花字生成器

输入文字，选择风格，一键生成课件花字图片。

**在线使用：** https://huazi-generator.streamlit.app

---

## 功能

- 9 种花字风格（橙黄活泼、红色冲击、清新自然、橙色厚重、花朵粉彩、双色错落、活泼卡通、粉彩少女、霓虹发光）
- 高级选项：调整字号、字间距、字体（9种可选）、各风格专属颜色
- 一键导出透明背景 PNG，直接插入 PPT

## 本地运行

```bash
git clone https://github.com/siki-lee/huazi-generator.git
cd huazi-generator
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
streamlit run app.py
```

## 项目结构

```
app.py              主程序
templates/          9种风格 SVG 模板
utils/
  fonts.py          字体注册表
  renderer.py       SVG → PNG 渲染（Playwright）
  _render_worker.py 子进程渲染脚本
fonts/              字体文件
```

## 技术栈

- [Streamlit](https://streamlit.io) — Web UI
- [Playwright](https://playwright.dev/python/) — SVG 渲染为 PNG
- SVG `@font-face` base64 内嵌字体，确保本地与云端字体一致
