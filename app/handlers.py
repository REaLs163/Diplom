from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('hi!')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('it`s help!')

@router.message(F.text == 'Начнем!')
async def help(message: Message):
    await message.answer('')