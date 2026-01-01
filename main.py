from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
import surah_and_ayah as helper
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import asyncio
import json
bot = Bot('8564471713:AAGytjx1ueh4nlH-r1g421U_LLMJ8sseKbU') # 8564471713:AAGytjx1ueh4nlH-r1g421U_LLMJ8sseKbU
router = Router()
dp = Dispatcher()
dp.include_router(router)
async def data1():
    with open('data.txt', 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
        return {int(k): v for k, v in data.items()}
async def data2(my_dict):
    with open('data.txt', 'w', encoding="utf-8") as f:
        json.dump(my_dict, f, indent=4, ensure_ascii=False)
my_dict = asyncio.run(data1())
@router.message(Command('start'))
async def start(msg):
    if msg.chat.id not in my_dict:
        my_dict[msg.chat.id] = False
        await data2(my_dict)
    await data2(my_dict)
    await bot.send_message(msg.chat.id, "Assalomu alekum!\nSend me the Surah and Ayah number in this format: 94:5")
@router.message(Command('switch'))
async def more_info(msg: Message):
    try:
        my_dict[msg.chat.id] = False if (not msg.chat.id in my_dict or my_dict[msg.chat.id]) else True
        await data2(my_dict)
        await msg.reply("Switched")
    except Exception as e:
        await msg.answer(str(e))
@router.message(lambda msg: msg.content_type == 'text')
async def echo(msg: Message):
    if not msg.chat.id in my_dict:
        my_dict[msg.chat.id] = False
        await data2(my_dict)
    if ':' in msg.text and msg.text.count(':') == 1:
        surah, ayah = msg.text.split(':')
        if surah.isdigit() and ayah.isdigit():
            if my_dict[msg.chat.id]:
                answer_txt = helper.main(int(surah), int(ayah), True)
                await msg.reply(answer_txt, parse_mode="HTML")
            else:
                button = InlineKeyboardButton(text = 'ℹ️ More Info', callback_data = f'{surah} {ayah} more')
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
                answer_txt = helper.main(int(surah), int(ayah), False)
                await msg.reply(answer_txt, parse_mode="HTML", reply_markup=keyboard)
        else:
            await msg.reply("Error: you must enter only digits ❗️")
    elif ':' in msg.text and len(msg.text) < 20:
        await msg.answer("Wrong format ❗️\nPlease use this format only: <i>Surah:Ayah</i> (e.g: 94:5)", parse_mode = "HTML")
@router.callback_query()
async def hi_callback(call: CallbackQuery):
    if ' ' in call.data and call.data.split()[-1] == 'more':
        surah, ayah = int(call.data.split()[0]), int(call.data.split()[1])
        answer_txt = helper.main(surah, ayah, True)
        if len(answer_txt) < 200:
            await call.answer(answer_txt)
        else:
            await call.message.answer(answer_txt, parse_mode="HTML")
async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())