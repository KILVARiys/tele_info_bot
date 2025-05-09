from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from sqlite_db import create_profile


router = Router(name=__name__)

# Обработка команды старт
@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(text='Привет')

@router.message(Command('retry'))
async def handle_retry(message: Message):
    await message.answer(text=f'{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}')

# Команда /add_me — запрашивает номер телефона
@router.message(Command('add_me'))
async def handle_adding(message: Message):
    # Создаем клавиатуру с кнопкой "Поделиться номером"
    button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], one_time_keyboard=True, resize_keyboard=True)

    await message.answer("Пожалуйста, поделитесь своим номером телефона:", reply_markup=keyboard)
    
# Обработчик контакта
@router.message()
async def handle_contact(message: Message):
    if message.contact:
        user_id = str(message.from_user.id)
        username = message.from_user.full_name
        dname = message.from_user.username
        phone = message.contact.phone_number

        # Передача данных в БД
        create_profile(user_id=user_id, username=username, dogname=dname, phone=phone)
        
        await message.answer(
            f"Спасибо, {username}!\nВаш номер телефона сохранен: {phone}",
            reply_markup=None  # Убираем клавиатуру
        )