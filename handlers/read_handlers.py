from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from keyboard import create_page_keyboard, create_comics_keyboard
from database import DB
from config import DICT

router = Router()


@router.message(Command(commands=["start", "comics"]))
async def send_comics_list(message: Message):
    markup = create_comics_keyboard()
    if not markup:
        return await message.answer(DICT['no_comics'])
    await message.answer(
        text=DICT['choose_for_read'],
        reply_markup=markup
    )


@router.callback_query(F.data.contains("to-home"))
async def send_comics_list_by_button(callback: CallbackQuery):
    markup = create_comics_keyboard()
    if not markup:
        return await callback.message.answer(DICT['no_comics'])
    await callback.message.answer(
        text=DICT['choose_for_read'],
        reply_markup=markup
    )
    await callback.message.delete()


@router.callback_query(F.data.contains("to-comics"))
async def go_to_comics(callback: CallbackQuery):
    comics_name, comics_len = callback.data.split(':')[1:]

    await callback.message.answer_photo(
        photo=DB.get_page_by_number(comics_name, 1),
        reply_markup=create_page_keyboard(
            comics_name=comics_name,
            page=1,
            pages_count=int(comics_len)
        )
    )
    await callback.message.delete()


@router.callback_query(F.data.contains("to-page"))
async def go_to_page(callback: CallbackQuery):
    comics_name, page, comics_len = callback.data.split(':')[1:]

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=DB.get_page_by_number(comics_name, page)
        ),
        reply_markup=create_page_keyboard(
            comics_name=comics_name,
            page=int(page),
            pages_count=int(comics_len)
        )
    )
    await callback.answer()


@router.callback_query()
async def delete_comics_by_button(callback: CallbackQuery):
    # Отлавливаю пустые колбеки
    await callback.answer()
