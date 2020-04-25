import re
import os
import base64
from telegram import Bot


uploader_id = 781791363
channel_id = -1001457689364


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def query_token(token_id):
    return read_file(f'token_{token_id}', True)


def set_proxy(ip='127.0.0.1', port=1080, protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = os.environ['HTTP_PROXY'] = os.environ['https_proxy'] = os.environ['HTTPS_PROXY'] = proxy
    return proxy


def telegram_style(text):
    do_bold = re.sub(r'\*\*(.+)\*\*', r'*\1*', text)
    do_italics = re.sub(r'__(.+)__', r'_\1_', do_bold)
    do_at = re.sub(r'@([a-zA-Z0-9_]+)', r'[@\1]', do_italics)
    del_strike = re.sub(r'~~(.+)~~', r'\1 (Edit here with underline)', do_at)
    return (del_strike, False) if del_strike == do_at else (del_strike, True)


def publish(text, markdown=True):
    if markdown:
        parse = 'Markdown'
    else:
        parse = None
    return uploader.send_message(channel_id, text, parse, True)


if __name__ == '__main__':
    set_proxy()
    uploader = Bot(query_token(uploader_id))
    with open('../Univinfo.md', 'r', encoding='utf-8') as file:
        index = file.read()
    tg_style_index, strike = telegram_style(index)
    res_1 = publish(tg_style_index)
    print('Sent index at: ', res_1.date, '\nNeed manually do strikethrough: ' if strike else '')
    with open('../Changelog.md', 'r', encoding='utf-8') as file:
        cl = file.read()
    tg_style_cl, strike = telegram_style(cl)
    tg_style_cl = tg_style_cl.replace('* ', '\\* ')
    res_2 = publish(tg_style_cl)
    print('Sent changelog at: ', res_2.date, '\nNeed manually do strikethrough: ' if strike else '')
