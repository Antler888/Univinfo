import re
import tgapi
import Bot_db
from tgapi import tools

uploader = tgapi.bot(Bot_db.uploader_id)


def telegram_style(text):
    do_italics = re.sub(r'__(.+)__', r'_\1_', text)
    do_at = re.sub(r'@([a-zA-Z0-9_]+)', r'[@\1]', do_italics)
    del_strike = re.sub(r'~~(.+)~~', r'\1 (这里手动下划线)', do_at)
    return (del_strike, False) if del_strike == do_at else (del_strike, True)


def publish(text, markdown=True):
    if markdown:
        parse = 'Markdown'
    else:
        parse = None
    return uploader.send(Bot_db.channel_id).text(text, parse=parse, no_preview=True)


if __name__ == '__main__':
    tools.set_proxy()
    with open('Univinfo.md', 'r', encoding='utf-8') as file:
        index = file.read()
    tg_style_index, strike = telegram_style(index)
    res_1 = publish(tg_style_index)
    print('Success: ', res_1['ok'], '\nNeed manually do strikethrough: ', strike)
    with open('Changelog.md', 'r', encoding='utf-8') as file:
        cl = file.read()
    tg_style_cl, strike = telegram_style(cl)
    res_2 = publish(tg_style_cl)
    print('Success: ', res_2['ok'], '\nNeed manually do strikethrough: ', strike)
