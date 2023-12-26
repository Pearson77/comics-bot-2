from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import DB
from config import DICT

router = Router()


class GetPhotos(StatesGroup):
    name = State()
    wait = State()


@router.message(Command(commands=["start", "comics"]))
async def send_comics_list(message: Message):
    ...


@router.message(Command(commands=["create"]))
async def create_new_comics(message: Message):
    ...


@router.message(Command(commands=["delete"]))
async def delete_one_comics(message: Message):
    ...


@router.message(StateFilter(GetPhotos.name))
async def get_comics_name(message: Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(comics_name=message.text)
        await message.answer(DICT['send_photos'])
        await state.set_state(GetPhotos.wait)
    else:
        await message.answer(DICT['must_text'])


@router.message(StateFilter(GetPhotos.wait), F.content_type == 'text')
async def stop_handling_photos(message: Message, state: FSMContext):
    print("TEST")
    data = await state.get_data()

    if 'file_ids' not in data:
        return await message.reply(DICT['no_files'])

    DB.create_comics(**data)
    await message.answer(DICT['created'])
    await state.clear()


@router.message(StateFilter(GetPhotos.wait), F.content_type == 'photo')
async def get_photo_from_user(message: Message, state: FSMContext):
    print("test")
    file_id = message.photo[-1].file_id
    data = await state.get_data()

    if 'file_ids' in data: data['file_ids'].append(file_id)
    else: data['file_ids'] = [file_id]


@router.message(F.callback_data == "to-home")
async def send_comics_list_by_button(callback: CallbackQuery):
    ...


@router.message(F.callback_data == "to-comics")
async def go_to_comics(callback: CallbackQuery):
    ...


@router.message(F.callback_data == "to-page")
async def go_to_page(callback: CallbackQuery):
    ...
