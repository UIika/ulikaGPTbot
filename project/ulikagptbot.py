import openai
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.filters.command import Command
from config import TG_TOKEN, GPT_API_KEY, PASSWORD

openai.api_key = GPT_API_KEY

model_id = 'gpt-3.5-turbo-16k'

history=[
     {
        'role': 'system',
        'content': '''You are a helpful assistant who answers in ukrainian,
                     and always refers to the user by his specified nickname'''
     },
    ]

def gpt_conversation(username, message) -> str:
    if len(history) == 1:
        history.append({'role': 'user',
                        'content': f'Привіт. мене звати {username}. {message}'})
    else:
        history.append({'role': 'user', 'content': f'{message}'})
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=history
    )
    history.append({'role': 'assistant', 'content': response.choices[-1].message.content})
    return response.choices[-1].message.content

# ////////////////////////////////////////////////////////////////////////////

bot = Bot(TG_TOKEN)
dp = Dispatcher()

is_password_entered = False

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    global is_password_entered
    is_password_entered = False
    await message.answer('Введіть пароль, будь ласка')
    
    
@dp.message(F.text == PASSWORD)
async def cmd_start(message: types.Message):
    global is_password_entered, history
    if is_password_entered == False:
        history = history[:1]
        is_password_entered = True
        await message.answer('Ласкаво просимо, приємного спілкування!😊')
        
@dp.message()
async def chatting(message: types.Message):
    if is_password_entered == True:
        await message.answer(gpt_conversation(message.from_user.username, message))
    else:
        await message.answer('Неправильний пароль!😡')
        
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())