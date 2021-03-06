import requests
from aiogram import types
from josee import data
from libs.round import RoundTo


async def cmd_crypto(msg: types.Message) -> None:
  answer = await msg.reply('Please wait...')
  res = "*Popular cryptocurrencies*\n"
  for i in data['crypto']:
    # print("Requesting:", i) # debug
    req = requests.get(f'https://data.messari.io/api/v1/assets/{i}/metrics').json()['data']['market_data']
    res += f"*{data['crypto'][i]['name']} ({data['crypto'][i]['short-name']})* - ${RoundTo(req['price_usd'])}"
    if req['percent_change_usd_last_1_hour']:   res += f" (1h: {RoundTo(req['percent_change_usd_last_1_hour'])}%"
    if req['percent_change_usd_last_24_hours']: res += f" 24h: {RoundTo(req['percent_change_usd_last_24_hours'])}%)"
    else: 
      if req['percent_change_usd_last_1_hour']: res += ")"
    res += "\n"
  await msg.bot.edit_message_text(res, msg.chat.id, answer.message_id, parse_mode = 'Markdown')
  return
