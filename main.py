from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
import surah_and_ayah as helper
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import json
import re
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
class Wizard(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
class Wizard2(StatesGroup):
    step1 = State()
    step2 = State()
def escape_md2(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
# -------------------------------------------------------------- START
@router.message(Command('start'))
async def start(msg):
    if msg.chat.id not in my_dict:
        my_dict[msg.chat.id] = False
        await data2(my_dict)
    await data2(my_dict)
    await bot.send_message(msg.chat.id, "Assalomu alekum!\nSend me the Surah and Ayah number in either like 94:5 or 94:5-6")
# -------------------------------------------------------------- GET INFO
@router.message(Command('i'))
async def get_info(msg: Message, state: FSMContext):
    await msg.answer("Send me the ID")
    await state.set_state(Wizard2.step1)
@router.message(Wizard2.step1)
async def next_step3(msg: Message, state: FSMContext):
    if msg.text == '/exit':
        await state.clear()
        await msg.answer("Now you are out!")
        return
    ID = msg.text
    if msg.text.isdigit() or (msg.text[0] == '-' and msg.text[1:].isdigit()):
        ID = int(ID)
        chat = await bot.get_chat(ID)
        first_name = chat.first_name
        username = chat.username
        text = f"Username: {"@" if username else ""}{username}\nFirst name: {first_name}\nLast name: {chat.last_name}"
        try:
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Click here", url=f"tg://user?id={ID}")]])
            await msg.answer(text, reply_markup=kb)
        except:
            await msg.answer(text)
    await state.clear()
# -------------------------------------------------------------- SEND
@router.message(Command('send'))
async def send_f(msg: Message, state: FSMContext):
    await msg.answer("Send me an ID or /all")
    await state.set_state(Wizard.step1)
@router.message(Wizard.step1)
async def next_send(msg: Message, state: FSMContext):
    if msg.text == '/exit':
        await state.clear()
        await msg.answer("Now you are out!")
        return
    if msg.text == '/all' or msg.text.isdigit() or (msg.text[1:].isdigit() and msg.text[0] == '-'):
        await msg.answer("Send me the message\nOr /exit")
        await state.update_data(name=msg.text)
        await state.set_state(Wizard.step2)
    else:
        await msg.answer("Wrong!")
@router.message(Wizard.step2)
async def next_send2(msg: Message, state: FSMContext):
    if msg.text == '/exit':
        await state.clear()
        await msg.answer("Now you are out!")
        return
    data = await state.get_data()
    ID = data['name']
    if ID == '/all':
        lst = list(my_dict.keys())
        s,l = 0,0
        for i in lst:
            try:
                await bot.send_message(i, msg.text)
                s += 1
            except:
                l += 1
        await msg.answer(f"Success: {s}\nLose: {l}")
    else:
        await bot.send_message(int(ID), msg.text)
        await msg.answer("Successfully sent!")
    await state.clear()
# -------------------------------------------------------------- SWITCH
@router.message(Command('switch'))
async def more_info(msg: Message):
    try:
        my_dict[msg.chat.id] = False if (not msg.chat.id in my_dict or my_dict[msg.chat.id]) else True
        await data2(my_dict)
        await msg.reply("Switched")
    except Exception as e:
        await msg.answer(str(e))
# -------------------------------------------------------------- ECHO
@router.message(lambda msg: msg.content_type == 'text')
async def echo(msg: Message):
    if not msg.chat.id in my_dict:
        my_dict[msg.chat.id] = False
        await data2(my_dict)
    if ':' in msg.text and msg.text.count(':') == 1:
        surah, ayah = msg.text.split(':')
        if '-' in ayah:
            start, stop = ayah.split('-')
            if surah.isdigit() and start.isdigit() and stop.isdigit():
                start = int(start); stop = int(stop); surah = int(surah)
                if start > stop:
                    await msg.answer(f"Invalid Range: {start} cannot be greater than {stop}")
                else:
                    try:
                        is_lower = helper.is_lower(surah, stop)
                    except OverflowError as error:
                        await msg.answer(f"{error}")
                    except ValueError as error:
                        await msg.answer(str(error))
                    else:
                        if is_lower:
                            for i in range(start, stop+1):
                                await msg.answer(f"{i-start+1}.\n{helper.main(surah, i, False)}", parse_mode="HTML")
            else:
                await msg.reply("Error: you must enter only digits ❗️")
        else:
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
        await msg.answer("Wrong format ❗️\nPlease use one of these formats only: <i>Surah:Ayah</i> (e.g: 94:5) or <i>Surah:Ayah-Ayah</i> (e.g: 94:5-6)", parse_mode = "HTML")
# -------------------------------------------------------------- CALLBACK
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