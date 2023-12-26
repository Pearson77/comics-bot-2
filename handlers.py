from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(Command(commands=["start", "comics"]))
async def send_comics_list(message: Message):
    ...


@router.message(Command(commands=["create"]))
async def create_new_comics(message: Message):
    ...


@router.message(Command(commands=["delete"]))
async def delete_one_comics(message: Message):
    ...


@router.message(F.callback_data == "to-home")
async def send_comics_list_by_button(callback: CallbackQuery):
    ...


@router.message(F.callback_data == "to-comics")
async def go_to_comics(callback: CallbackQuery):
    ...


@router.message(F.callback_data == "to-page")
async def go_to_page(callback: CallbackQuery):
    ...
