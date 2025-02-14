import json

import AIHelper
import Config

LANG = 0
# 0: Chinese Simplified, 1: Chinese Traditional, 2: English, 3: Japanese（翻译由 ChatGPT 提供）

STRINGS = {}
LANG_DICT = {
    0: 'zh_cn',
    1: 'zh_tr',
    2: 'en_us',
    3: 'jp_jp'
}
LANG_NAME_DICT = {
    0: '简体中文',
    1: '繁體中文',
    2: 'English',
    3: '日本語'
}


def set_language(lang: int):
    global LANG
    LANG = lang
    load_strings()
    AIHelper.add_response('player has set language to ' + LANG_NAME_DICT[LANG])


def load_strings():
    with open('./assets/lang/' + LANG_DICT[LANG] + '.json', 'r', encoding='utf-8') as file:
        global STRINGS
        STRINGS = json.load(file)


def text(string: str):
    return TranslatableText(string)


def literal(string: str):
    return Text(string)


def ai_text(name: str, string: str):
    return AIResponseText(name + ': ' + string)


class Text:

    def __init__(self, string: str):
        self.string = string

    def format(self, *args):
        return self.string.format(*args)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()

    def get(self):
        return self.__str__()


class TranslatableText(Text):

    def __init__(self, key: str):
        super().__init__(key)

    def format(self, *args):
        return STRINGS[self.string].format(*args) if self.string in STRINGS else self.string

    def __str__(self):
        return STRINGS[self.string] if self.string in STRINGS else self.string

    def __repr__(self):
        return self.__str__()

    def get(self):
        return self.__str__()


class AIResponseText(Text):

    def __init__(self, string: str):
        super().__init__(string)
        self.st = 0
        self.cnt = len(string)

    def count(self, limit=Config.SCREEN_WIDTH // 2):
        self.cnt = min(self.cnt + 1, len(self.string) - 1)
        return ((0 <= self.cnt < len(self.string) and self.string[self.cnt] == '\n') or
                Config.FONT.size(self.__str__())[0] > limit)

    def is_end(self):
        return self.cnt == len(self.string) - 1

    def __str__(self):
        return self.string[self.st:self.cnt + 1]

    def __repr__(self):
        return self.__str__()

    def get(self):
        return self.__str__()


load_strings()
