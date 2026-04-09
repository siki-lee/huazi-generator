"""
字体注册表：名称 → 文件路径映射
"""
import os

_FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts')

FONTS = {
    'KeinannMaruPOP 圆体':    'KeinannMaruPOP.ttf',
    '快看世界体':              'kuaikanshijieti20231213.ttf',
    '昆明海鸥体':              'KunmingHaiyou.ttf',
    '马善政毛笔楷书':          'MaShanZheng-Regular.ttf',
    '明朝仿宋（简体）':        'StudyMingCN-Regular.ttf',
    '明朝仿宋（繁体）':        'StudyMingTW-Regular.ttf',
    'Written 手写体':          'Written-Regular.ttf',
    'WrittenSC 手写简体':      'WrittenSC-Regular.ttf',
    '春秋书法体':              'ChillCalligraphyChunQiu_QiuHong.ttf',
}

FONT_NAMES = list(FONTS.keys())


def get_font_path(name: str) -> str:
    return os.path.join(_FONT_DIR, FONTS[name])
