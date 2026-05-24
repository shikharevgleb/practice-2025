import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8950531562:AAE8KY3XTBPoAagJj9nLhh40ryvuT11CZsE"

# 📁 ПУТЬ К ПАПКЕ ПРОЕКТА
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "..", "IMGS")


# -------- ДОСТОПРИМЕЧАТЕЛЬНОСТИ --------
PLACES = {
    "red_square": {
        "name": "Красная площадь",
        "photo": os.path.join(IMG_DIR, "RedSQ.jpg"),
        "text": "Красная площадь — главная площадь Москвы и один из самых известных символов России. Здесь находятся Кремль, Собор Василия Блаженного и ГУМ. Площадь является местом проведения важных государственных мероприятий и праздников. Она входит в список Всемирного наследия ЮНЕСКО."
    },
    "arbat": {
        "name": "Арбат",
        "photo": os.path.join(IMG_DIR, "Arbat.jpg"),
        "text": "Арбат — одна из старейших и самых известных улиц Москвы. Это пешеходная зона, где часто выступают уличные музыканты и художники. Здесь можно увидеть старинные здания и уютные кафе. Арбат считается центром творческой атмосферы города."
    },
    "kremlin": {
        "name": "Кремль",
        "photo": os.path.join(IMG_DIR, "Kreml.jpg"),
        "text": "Московский Кремль — историческая крепость и политический центр России. Он расположен на берегу Москвы-реки и окружён мощными стенами и башнями. Внутри находятся соборы, дворцы и резиденция президента. Кремль является одним из главных символов страны."
    },
    "moscow_city": {
        "name": "Москва-Сити",
        "photo": os.path.join(IMG_DIR, "Moscowcity.png"),
        "text": "Москва-Сити — современный деловой район с высокими небоскрёбами. Здесь расположены офисы, торговые центры и смотровые площадки. Это символ новой, современной Москвы. Район особенно красив ночью благодаря яркой подсветке."
    },
    "ostankino": {
        "name": "Останкинская башня",
        "photo": os.path.join(IMG_DIR, "Останкинская башня.jpg"),
        "text": "Останкинская башня — одна из самых высоких телебашен в мире. Она используется для телевещания и радиосигналов. На башне есть смотровая площадка с видом на всю Москву. Это важный инженерный и туристический объект."
    },
    "tsaritsyno": {
        "name": "Царицыно",
        "photo": os.path.join(IMG_DIR, "Tsarizino.jpg"),
        "text": "Царицыно — музей-заповедник с дворцами, парками и прудами. Он был построен по приказу Екатерины II. Сейчас это популярное место для прогулок и отдыха. Архитектура комплекса сочетает готику и классицизм."
    },
    "minin_pozharsky": {
        "name": "Минин и Пожарский",
        "photo": os.path.join(IMG_DIR, "Minin.jpg"),
        "text": "Памятник Минину и Пожарскому установлен на Красной площади. Он посвящён героям, освободившим Москву от польских захватчиков в 1612 году. Это первый крупный скульптурный памятник в России. Он символизирует единство и патриотизм народа."
    },
}


# -------- МЕНЮ --------
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Красная площадь ➡️", callback_data="red_square")],
        [InlineKeyboardButton("Арбат ➡️", callback_data="arbat")],
        [InlineKeyboardButton("Кремль ➡️", callback_data="kremlin")],
        [InlineKeyboardButton("Москва-Сити ➡️", callback_data="moscow_city")],
        [InlineKeyboardButton("Останкинская башня ➡️", callback_data="ostankino")],
        [InlineKeyboardButton("Царицыно ➡️", callback_data="tsaritsyno")],
        [InlineKeyboardButton("Минин и Пожарский ➡️", callback_data="minin_pozharsky")],
    ]
    return InlineKeyboardMarkup(keyboard)


# -------- START --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-гид 🏛\n\nНапиши /places"
    )


# -------- PLACES --------
async def places(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери достопримечательность:",
        reply_markup=main_menu(),
    )


# -------- CALLBACK --------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # назад в меню
    if query.data == "menu":
        await query.message.reply_text(
            "Выбери достопримечательность:",
            reply_markup=main_menu(),
        )
        return

    place = PLACES.get(query.data)

    if not place:
        await query.message.reply_text("Не найдено")
        return

    # проверка файла
    if not os.path.exists(place["photo"]):
        await query.message.reply_text("❌ Фото не найдено")
        return

    with open(place["photo"], "rb") as photo:
        await query.message.reply_photo(
            photo=InputFile(photo),
            caption=f"🏛 {place['name']}\n\n{place['text']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")]
            ])
        )


# -------- RUN --------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("places", places))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")
app.run_polling()