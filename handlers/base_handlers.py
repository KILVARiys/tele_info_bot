from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from sqlite_db import create_profile
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

router = Router(name=__name__)


# Команда /start
@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(text='👋 Привет!')


# Команда /retry
@router.message(Command('retry'))
async def handle_retry(message: Message):
    await message.answer(
        text=f'{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}'
    )


# Команда /add_me — запрашивает номер телефона
@router.message(Command('add_me'))
async def handle_adding(message: Message):
    button = KeyboardButton(text="📱 Поделиться номером", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], one_time_keyboard=True, resize_keyboard=True)
    await message.answer("📞 Пожалуйста, поделитесь своим номером телефона:", reply_markup=keyboard)


# Обработчик контакта
@router.message()
async def handle_contact(message: Message):
    if message.contact:
        phone = message.contact.phone_number
        user_id = str(message.from_user.id)
        username = message.from_user.full_name
        dname = message.from_user.username

        try:
            # Добавляем код страны, если его нет
            if not phone.startswith('+'):
                phone = '+7' + phone if len(phone) == 10 or phone.startswith('7') else '+' + phone

            # Парсим номер с указанием региона по умолчанию
            parsed_number = phonenumbers.parse(phone, "RU")

            # Проверяем валидность
            if not phonenumbers.is_valid_number(parsed_number):
                await message.answer("❌ Номер телефона недействителен.")
                return

            # Получаем информацию
            country = geocoder.description_for_number(parsed_number, "ru")
            num_type = phonenumbers.number_type(parsed_number)

            type_names = {
                0: "Фиксированный",
                1: "Мобильный",
                2: "Фиксированный и мобильный",
                3: "VOIP",
                4: "Телефония общего назначения",
                5: "Пейджер",
                6: "Учрежденческая сеть",
                7: "Личное радиоустройство",
                8: "Виртуальный номер",
                9: "ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ",
                10: "Неизвестно"
            }

            number_type = type_names.get(num_type, "Не определён")
            carrier_name = carrier.name_for_number(parsed_number, "ru") or "Не найден"
            time_zones = timezone.time_zones_for_number(parsed_number)
            tz_info = ', '.join(time_zones) if time_zones else "Не найден"

            # Отправляем информацию пользователю
            info_message = (
                f"✅ Ваш номер проверен!\n"
                f"Страна: {country}\n"
                f"Тип номера: {number_type}\n"
                f"Оператор: {carrier_name}\n"
                f"Часовой пояс: {tz_info}"
            )
            await message.answer(info_message)

            # Сохраняем в БД
            create_profile(user_id=user_id, username=username, dogname=dname, phone=phone)

        except phonenumbers.NumberParseException as e:
            await message.answer("❌ Не удалось распознать номер. Убедитесь, что он правильный.")
        except Exception as e:
            await message.answer(f"[!] Ошибка при обработке номера: {e}")
        finally:
            await message.answer(
                f"✔️ Спасибо, {username}!\nВаш номер телефона сохранён.",
                reply_markup=None  # Убираем клавиатуру
            )