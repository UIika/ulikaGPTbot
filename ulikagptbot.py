import openai
import asyncio
from openai.error import InvalidRequestError
from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.filters.command import Command
from config import TG_TOKEN, GPT_API_KEY, PASSWORD

openai.api_key = GPT_API_KEY
model_id = 'gpt-3.5-turbo'

vip_users = [
    'ulikalitka',
]

history=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant who speaks ukrainian mostly'
        },
        ]

def gpt_conversation(message: str) -> str:
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
    if message.from_user.username in vip_users:
        is_password_entered = True
        await message.answer('Приємного спілкування!😊')
    else:
        is_password_entered = False
        await message.answer('Введіть пароль, будь ласка')
    
    
@dp.message(F.text == PASSWORD)
async def authenticate(message: types.Message):
    global is_password_entered
    if is_password_entered == False:
        global history
        history = history[:1]
        is_password_entered = True
        await message.answer('Приємного спілкування!😊')
        
@dp.message()
async def chatting(message: types.Message):
    if is_password_entered == True:
        tmp_message = await message.answer('Зачекайте поки бот згенерує відповіть')
        try:
            await bot.edit_message_text(
                gpt_conversation(message),
                message.chat.id, tmp_message.message_id)
        except(InvalidRequestError):
            await bot.edit_message_text('''Ви досягли максимуму можливих повідомлень, розпочніть нову бесіду за допомогою команди /start''',
                                 message.chat.id, tmp_message.message_id)
            cmd_start(message)
    else:   
        await message.answer('Неправильний пароль!😡')
        
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())