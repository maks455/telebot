import telebot
from telebot import types
import random
import sqlite3
import io
from openpyxl import Workbook

token = "6929917267:AAGM9rToUWuAgVxpvfflNvHIYAkOmwRu_JE"
bot = telebot.TeleBot(token)

ALPHABET = "qwertyuiopasdfghjklzxcvbnm"
DIGITAL = "1234567890"

def theme(applic):
    con = sqlite3.connect('TeleBotDJD/db/chat_bot_database.sqlite')
    cur = con.cursor()
    th = {}
    themes = ["прокат", "документ", "экскурсия", "запись", "расписание"]
    for i in enumerate(cur.execute("SELECT atribute FROM atribute").fetchall()):
        for j in i[1]:
            a = 100 / len(j.split(','))
            res = 0
            for k in j.split(','):
                if k in applic.split():
                    res += a
            th[res] = themes[i[0]]
    print(th)
    con.commit()
    con.close()
    return [th[max(th)], max(th)]


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Перед вами бот, который ответит на ваши интересующие вопросы."
    )
    c1 = types.BotCommand(command="start", description="Старт бота")
    c2 = types.BotCommand(command="admin", description="Вход в админ панель")
    bot.set_my_commands([c1, c2])
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands("commands"))


@bot.message_handler(commands=["admin"])
def admin_message(message):
    bot.send_message(message.chat.id, "Пожалуйста предоставте ваш код доступа")
    bot.register_next_step_handler(message, password)


def password(message):
    with open("TeleBotDJD/passwords", "r") as file:
        data = [line.strip() for line in file]
    res = ""
    for i in data:
        if i.split()[1] == message.text:
            res = i.split()[0]
    if res == "MainPerson":
        bot.send_message(message.chat.id, "Здравствуйте! Главный администратор")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить нового администратора")
        item2 = types.KeyboardButton("Удалить админимтратора")
        item3 = types.KeyboardButton("Список администраторов")
        item4 = types.KeyboardButton("Вопросы пользователей")
        item5 = types.KeyboardButton("Назад")
        items = [item1, item2, item3, item4, item5]
        for item in items:
            markup.add(item)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        bot.register_next_step_handler(message, functions_main_admin)
    elif res:
        bot.send_message(message.chat.id, f"Здравствуйте, {res}!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Вопросы пользователей")
        markup.add(item1)
        bot.register_next_step_handler(message, function_admin)
    else:
        bot.send_message(message.chat.id, "Веденный код неверный")
        bot.register_next_step_handler(message, password)


def functions_main_admin(message):
    if message.text == "Добавить нового администратора":
        msg = bot.send_message(message.chat.id, "Введите имя нового администратора")
        bot.register_next_step_handler(msg, new_admin)
    elif message.text == "Удалить админимтратора":
        msg = bot.send_message(message.chat.id, "Введите имя администратора")
        bot.register_next_step_handler(msg, delete_admin)
    elif message.text == "Список администраторов":
        con = sqlite3.connect('TeleBotDJD/db/chat_bot_database.sqlite')
        cur = con.cursor()
        wb = Workbook()
        ws = wb.active
        for i in range(len(cur.execute('SELECT id FROM applications').fetchall())):
            ws.append(*cur.execute('SELECT * FROM applications WHERE id=?', (i,)).fetchall())
        con.close()
        wb.save('applications.xlsx')
        with open('applications.xlsx', 'rb') as f:
            bot.send_document(message.chat.id, f)
        bot.register_next_step_handler(message, functions_main_admin)
    elif message.text == "Назад": 
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Такой команды не существует")
        bot.register_next_step_handler(message, functions_main_admin)


def new_admin(message):
    with open("TeleBotDJD/passwords", "r") as file:
        data = [line.strip() for line in file]
    data = "\n".join(data)
    passw = random.choices(ALPHABET, k=7)
    passw += random.choices(DIGITAL, k=3)
    passw = "".join(passw)
    with open("TeleBotDJD/passwords", "w") as file:
        file.write(data + f"\n{message.text} {passw}")
    bot.send_message(
        message.chat.id,
        f"Добавлен новый администратор:\n Логин: {message.text}\n Пароль: {passw}",
    )
    bot.register_next_step_handler(message, functions_main_admin)


def delete_admin(message):
    with open("TeleBotDJD/passwords", "r") as file:
        data = [line.strip() for line in file]
    for i in data:
        if i.split()[0] == message.text and i.split()[0] != "MainPerson":
            write_data = ""
            for j in data:
                if i.split()[0] not in j:
                    write_data += j + "\n"
            write_data = write_data.rstrip("\n")
            break
    else:
        bot.send_message(message.chat.id, "Администратор с таким логином не найден")
        bot.register_next_step_handler(message, functions_main_admin)
        return
    with open("TeleBotDJD/passwords", "w") as file:
        file.write(write_data)
    bot.send_message(message.chat.id, "Администротор успешно удален из базы данных")
    bot.register_next_step_handler(message, functions_main_admin)


def function_admin():
    pass


@bot.message_handler(content_types="text")
def button_message(message):
    if theme(message.text)[1] < 1:
        bot.send_message(message.chat.id, "dont know")
    else:
        print(theme(message.text))
    if message.text == "Как к вам записаться?":
        bot.send_message(
            message.chat.id,
            """✏ Для записи на обучение Вам необходимо:

💼 Собрать пакет документов
📎 копия документа удостоверяющего личность ребенка
📎 копия СНИЛС ребенка
📎 4 цветные фотографии 3х4 без уголка
📎 заполнить заявление 👇🏼*
📎 заполнить согласие на обратку персональных данных 👇🏼

📬 принести пакет документов по адресу Чита, 1-я Ипподромная 5 Читинская детская железная дорога

📆 выбрать удобный день для посещения занятий

💬 ожидать сообщения о начале занятий

🚀 быть готовым вовремя прийти на занятие""")
        bot.send_document(
            message.chat.id,
            open(
                "TeleBotDJD/Заявление_на_поступление_на_ЧДЖД+анкет+расписка+согласие_на_обр.pdf",
                "rb",
            ),
        )
    elif message.text == "Сколько раз в неделю проходят занятия?":
        bot.send_message(message.chat.id, "Занятия проходят 1 раз в неделю.")
    elif message.text == "Сколько длятся занятия?":
        bot.send_message(message.chat.id, "1,5 часа")
    elif message.text == "С какого класса можно отдать ребенка на обучении?":
        bot.send_message(message.chat.id, "Отдать ребенка на обучение можно с 5 класса")
    else:
        bot.send_message(message.chat.id, "Что то на непонятном")


bot.infinity_polling()
