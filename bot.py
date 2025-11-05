from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
import random
TOKEN = "12345"
bot = Bot(token = TOKEN)
dispatcher = Dispatcher()
answered_correct = [
    "☘Сегодня вы удачливы!",
    "🌿Афина благосклонна вам!",
    "🏛️Даже стены храмов не могут устоять перед вашей мудростью!"
]
answered_wrong = [
    "🩸Кажется, вы ошиблись...",
    "🍂Возможно, надо попытаться снова...",
    "⛏ Что-то не то... Стоит попробовать еще раз..."
]
def helpSpoiler(text):
    symb = r"_*[](){}~`>#+-=|.!"
    for s in symb:
        text = text.replace(s, f"\\{s}")
    return text
questions = [
    {
        "q": "Название Греции Эллада произошло от Эллина, внука...",
        "options": ["Зевса", "Прометея", "Аполлона", "Афродиты"],
        "correct": 1
    },
    {
        "q": "Как звали матерь Зевса?",
        "options": ["Рея", "Александра", "Артемида", "София"],
        "correct": 0
    },
    {
        "q": "Какой философ жил в бочке (пифосе)?",
        "options": ["Анаксагор", "Диоген Аполлонийский", "Диоген Синопский", "Сократ"],
        "correct": 2
    },
    {
        "q": "Кто написал Илиаду?",
        "options": ["Аристотель", "Эсхил", "Софокл", "Гомер"],
        "correct": 3
    },
    {
        "q": "Какая дисциплина была на первых Олимпийских играх?",
        "options": ["Бег", "Метание копья", "Борьба", "Езда на колесницах"],
        "correct": 0
    },
    {
        "q": "Какой был самый крупный полис в Древней Греции?",
        "options": ["Фивы", "Афины", "Коринф", "Спарта"],
        "correct": 1
    },
    {
        "q": "Сколько примерно полисов было в Древней Греции?",
        "options": ["20", "600", "2000", "1000"],
        "correct": 3
    },
    {
        "q": "Венками из какого дерева награждали атлетов?",
        "options": ["Дуб", "Сосна", "Оливковое", "Ель"],
        "correct": 2
    },
    {
        "q": 'Кто написал "Описание эллады", первый туристический путеводитель?',
        "options": ["Павсаний", "Эпиктет", "Адриан", "Аристотель"],
        "correct": 0
    },
        {
        "q": 'Чью шкуру носил на спине Геракл?',
        "options": ["Сфинкс", "Лев", "Дракон", "Минотавр"],
        "correct": 1
    },
]
data_of_user = {}
@dispatcher.message(Command("start"))
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    data_of_user[user_id] = {"index": 0, "count": 0}
    await bot.send_message(message.chat.id, "🏺Приветствуем вас на экзамене мудрости Эллады!\nПусть Афина будет благосклонна к вам!")
    await tell_question(message.chat.id, message.from_user.id)
async def tell_question(chat_id, user_id):
    index = data_of_user[user_id]["index"]
    all = len(questions)
    if (index >=  all):
        correct = data_of_user[user_id]["count"]
        correctly = correct / all * 100
        if (correctly >= 70):
            sent = f"🎖Вы справились с испытанием мудрости! Вы набрали {correct}/{all}"
        else:
            sent = f"🩸К сожалению, вы не справились... Попробуйте еще раз!"
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Пройти заново", callback_data="retry")]])
        await bot.send_message(chat_id, sent, reply_markup=keyboard)
        return
    exact_question = questions[index];
    btns = []
    for i, option in enumerate(exact_question["options"]):
        btns.append(types.InlineKeyboardButton(text=option, callback_data=str(i)))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[btns])
    await bot.send_message(chat_id, f"{exact_question['q']}", reply_markup=keyboard)
@dispatcher.callback_query()
async def answer(back: types.CallbackQuery):
    if (back.data == "retry"):
        data_of_user[back.from_user.id] = {"index": 0, "count": 0}
        await tell_question(back.message.chat.id, back.from_user.id)
        await back.answer()
        return
    chat_id = back.from_user.id;
    question_ind = data_of_user[chat_id]["index"]
    question = questions[question_ind]
    answer_ind = int(back.data)
    if answer_ind == question["correct"]:
        data_of_user[chat_id]["count"] += 1
        await back.message.answer(random.choice(answered_correct))
    else:
        wrong = random.choice(answered_wrong)
        correct = question["options"][question["correct"]]
        await back.message.answer(f"{helpSpoiler(wrong)}\nПравильный вариант: ||{helpSpoiler(correct)}||", parse_mode = "MarkdownV2")
    data_of_user[chat_id]["index"]+=1
    await tell_question(back.message.chat.id, back.from_user.id)
    await back.answer()
async def main():
    await dispatcher.start_polling(bot)
asyncio.run(main())