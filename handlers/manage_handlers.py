from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboard import create_delete_keyboard
from database import DB
from config import DICT

router = Router()


class GetPhotos(StatesGroup):
    name = State()
    wait = State()


@router.message(Command(commands=["create"]))
async def create_new_comics(message: Message, state: FSMContext):
    await message.answer(DICT['send_name'])
    await state.set_state(GetPhotos.name)


@router.message(Command(commands=["delete"]))
async def delete_one_comics(message: Message):
    markup = create_delete_keyboard()
    if not markup:
        return await message.answer(DICT['no_comics'])
    await message.answer(
        text=DICT['choose_for_delete'],
        reply_markup=markup
    )


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
    data = await state.get_data()

    if 'file_ids' not in data:
        return await message.reply(DICT['no_files'])

    DB.create_comics(**data)
    await message.answer(DICT['created'])
    await state.clear()


@router.message(StateFilter(GetPhotos.wait), F.content_type == 'photo')
async def get_photo_from_user(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data()

    if 'file_ids' in data: data['file_ids'].append(file_id)
    else: data['file_ids'] = [file_id]
    await state.update_data(data)


@router.callback_query(F.data.contains("delete"))
async def delete_comics_by_button(callback: CallbackQuery):
    DB.delete_comics(callback.data.split(':')[1])
    await callback.answer(DICT['deleted'])
    await callback.message.delete()
