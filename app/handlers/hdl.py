import os
import shutil
from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
import app.message.msg
import app.states.stat as st
import app.keyboards.kbs as kb

from parse import collect_reviews, extract_product_id, get_total_reviews_count
from word_count_from_spacy import analyze_reviews

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(app.message.msg.start, reply_markup=kb.main_kb)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(app.message.msg.help)

@router.message(Command('done'))
@router.message(F.text == "Закончить работу")
async def done(message: Message, state: st.ReviewState):
    user_id = str(message.from_user.id)
    user_folder = f"data/{user_id}"
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
    await state.clear()
    await message.answer(app.message.msg.done, reply_markup=ReplyKeyboardRemove())
    
@router.message(F.text == "Анализ и обработка отзывов")
async def start_review_process(message: Message, state: st.ReviewState):
    await state.set_state(st.ReviewState.waiting_for_url)
    await message.answer(app.message.msg.anliz)
    
@router.message(st.ReviewState.waiting_for_url)
async def process_url(message: Message, state: st.ReviewState):
    url = message.text.strip()
    try:
        product_id = extract_product_id(url)
        await state.update_data(url=url, product_id=product_id)
        await state.set_state(st.ReviewState.waiting_for_count)
        await message.answer(app.message.msg.proc_url)
    except ValueError:
        await message.answer(app.message.msg.proc_url_warning)
        
@router.message(st.ReviewState.waiting_for_count)
async def process_count(message: Message, state: st.ReviewState):
    try:
        count = int(message.text.strip())
        if count <= 0:
            await message.answer(app.message.msg.wtn_count)
            return
    except ValueError:
        await message.answer(app.message.msg.wtn_count_warning)
        return

    data = await state.get_data()
    url = data['url']
    product_id = data['product_id']
    user_id = str(message.from_user.id)
    user_folder = f"data/{user_id}"
    os.makedirs(user_folder, exist_ok=True)

    await message.answer(f"🔄 Собираю {count} отзывов по ссылке:\n{url}")

    try:
        total_available = get_total_reviews_count(product_id)
        await message.answer(f"Всего отзывов на сайте: {total_available}")

        if total_available == 0:
            await message.answer(app.message.msg.get_trc)
            await state.clear()
            return

        if count > total_available:
            await message.answer(f"Запрошено {count} отзывов, но доступно только {total_available}.")
            count = total_available

        # Сбор отзывов и анализ
        json_path = collect_reviews(user_id=user_id, product_url=url, total_reviews_needed=count)
        filename = os.path.basename(json_path)
        user_json_path = os.path.join(user_folder, filename)
        os.replace(json_path, user_json_path)

        top_words = analyze_reviews(user_json_path)
        if not top_words:
            await message.answer(app.message.msg.analize_rev)
            await state.clear()
            return

        result_text = "\n".join([f"{hbold(word)}: {cnt}" for word, cnt in top_words])
        await message.answer(f"✅ Анализ завершён!\n\nВот топ-10 часто встречающихся слов:\n\n{result_text}")

    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {e}")
    finally:
        await state.clear()