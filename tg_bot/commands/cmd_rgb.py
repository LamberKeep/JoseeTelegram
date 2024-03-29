import os
from time import time

from aiogram import bot, types
from PIL import Image as IMG
from aiogram.types import Message


async def cmd_rgb(msg: types.Message) -> Message | None:
    arg = msg.text.split()[1:]

    if not arg:
        return await msg.reply("Usage: /rgb <r> <g> <b>")

    r = int(arg[0])
    g = int(arg[1])
    b = int(arg[2])

    if 0 < r > 255 or 0 < g > 255 or 0 < b > 255:
        return await msg.reply("")

    try:
        file_name = int(time())
        IMG.new("RGB", (128, 128), (r, g, b)).save(f"tg_bot/cache/{file_name}.png", bitmap_format="png")
        file = open(f"tg_bot/cache/{file_name}.png", "rb")
    except Exception as e:
        print(e)
        await msg.reply("Error, usage: /rgb <r> <g> <b>")
        return

    await bot.send_photo(msg.chat.id, file,
                         f"*RGB:* {r}, {g}, {b}\n"
                         f"*HEX:* #{''.join(str(i) for i in rgb2hex(r, g, b))}\n"
                         f"*HSV:* {', '.join(str(round(i)) for i in rgb2hsv(r, g, b))}\n"
                         f"*CMYK:* {', '.join(str(round(i)) for i in rgb2cmyk(r, g, b))}\n",
                         parse_mode="Markdown")

    os.remove(f"tg_bot/cache/{file_name}.png")
    return file.close()


def rgb2hex(r: int, g: int, b: int):
    return "%02x" % r, "%02x" % g, "%02x" % b


def rgb2hsv(r: int, g: int, b: int):
    if 0 < r > 255 or 0 < g > 255 or 0 < b > 255:
        return False

    r /= 255
    g /= 255
    b /= 255

    M = max(r, g, b)
    m = min(r, g, b)

    diff = M - m

    h = -1
    if M == m:
        h = 0
    elif M == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif M == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif M == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0
    if M != 0:
        s = (diff / M) * 100

    v = M * 100

    return h, s, v


def rgb2cmyk(r: int, g: int, b: int):
    r /= 255
    g /= 255
    b /= 255

    k = 1 - max(r, g, b)

    return (1 - r - k) / (1 - k) * 100, (1 - g - k) / (1 - k) * 100, (1 - b - k) / (1 - k) * 100, k * 100
