from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from parse import collect_reviews
from word_count_from_spacy import analyze_reviews
import app.message.msg

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(app.message.msg.start)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(app.message.msg.help)

@router.message(F.text.lower() == 'привет')
async def help(message: Message):
    await message.answer(app.message.msg.hello)