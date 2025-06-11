# LanguageSwitcher.py

import language_switch.language as language
# import language?

class LanguageSwitcher:
    def __init__(self, lang='en'):
        self.lang = lang

    def set_language(self, lang):
        self.lang = lang

    def get_text(self, key):
        if key in language.language:
            return language.language[key][self.lang]
        else:
            return ''

def get_text(key):
    # 创建语言切换实例，默认使用英文
    switcher = LanguageSwitcher()
    # 切换到中文
    # switcher.set_language('zh')
    # 切换到英文
    switcher.set_language('en')
    return switcher.get_text(key)

