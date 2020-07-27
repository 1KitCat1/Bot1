import telebot
from data import token
from datetime import datetime

bot = telebot.TeleBot(token)
print(bot.get_me())

users = {}

location = {}

admins = [482025744]

admin_temp = []
def content_check(message):
    print(datetime.now())
    print("Сообщение '{0}' от {1} {2} (id {3}). \n".format(message.text,
                                                               message.from_user.first_name,
                                                               message.from_user.last_name,
                                                                message.chat.id))

#Начало работы с ботом
@bot.message_handler(commands=['start'])
def startfunc(message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Этот бот поможет Вам выбрать услугу в клининг компании "Жумайсынба"')
    reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    button1 = telebot.types.KeyboardButton(text="Сухая уборка")
    button2 = telebot.types.KeyboardButton(text="Влажная уборка")
    button3 = telebot.types.KeyboardButton(text="Химчистка")
    button4 = telebot.types.KeyboardButton(text="Чистка ковров")
    reply_markup.add(button1, button2, button3, button4)
    if not users.get(message.from_user.id):
        bot.send_message(message.chat.id, "Вы не зарегистрированы. Как мне к Вам обращатся?")
        bot.register_next_step_handler(message, registration)
    else:
        bot.send_message(message.chat.id, 'Выберите услугу:', reply_markup = reply_markup)
    content_check(message)

#Регистрация нового пользователя
def registration(message):
    users.setdefault(message.from_user.id, []).append(message.text)
    bot.send_message(chat_id=message.chat.id, text=f'Здравствуй, {message.text}')
    bot.send_message(chat_id=message.chat.id, text=f'Вы зарегистрированы. Для продолжения работы с ботом введите /start')
    content_check(message)

#Вход в админку
@bot.message_handler(commands=['getadmin'])
def admin_control(message):
    content_check(message)
    if not admins.count(message.from_user.id):
        bot.send_message(message.chat.id, "You have no access. Input your password")
        bot.register_next_step_handler(message, adminpass)

    else:
        commands = telebot.types.ReplyKeyboardMarkup(True, True, row_width=1)
        button1 = telebot.types.KeyboardButton('Send message to another user')
        commands.add(button1)
        bot.send_message(message.chat.id, "Выбери команду", reply_markup=commands)
        bot.register_next_step_handler(message, admin_commands)

#Команды админки
def admin_commands(message):
    content_check(message)
    if message.text == "Send message to another user":
        bot.send_message(message.chat.id, 'Enter chat id (or self)')
        bot.register_next_step_handler(message, entering_id)


def entering_id(message):
    content_check(message)
    if message.text == 'self':
        admin_temp.append(message.chat.id)
    else:
        admin_temp.append(message.text)
    bot.send_message(message.chat.id, 'Now enter your message')
    bot.register_next_step_handler(message, entering_message)


def entering_message(message):
    content_check(message)
    admin_temp.append(message.text)
    bot.send_message(admin_temp[0], admin_temp[1])
    bot.send_message(message.chat.id, f'Message "{admin_temp[1]}" has been sent to {admin_temp[0]}')
    admin_temp.clear()

#Авторизация админки
def adminpass(message):
    content_check(message)
    from data import passwords
    if not passwords.count(message.text):
        bot.send_message(message.chat.id, "Invalid password")
    else:
        admins.append(message.from_user.id)
        bot.send_message(message.chat.id, "Access granted")
        print(f"ACCESS GRANTED TO {message.from_user.first_name}")


@bot.message_handler(content_types='text', func = lambda message: message == 'Доставлю сам' or message == 'Служебная машина')
def carpets(message):
    content_check(message)
    if not users.get(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы не авторизированы. Пройдите регистрацию используя команду /start')
    elif message.text == 'Доставлю сам':
        bot.send_message(message.chat.id, 'Выслать Вам адреса наших пунктов приема?')
        bot.register_next_step_handler(message, )



@bot.message_handler(content_types='text')
def answer_text(message):
    content_check(message)
    if not users.get(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы не авторизированы. Пройдите регистрацию используя команду /start')

    elif message.text == 'Сухая уборка':
        bot.send_message(message.chat.id, 'Вы выбрали "Сухую уборку"')
        bot.send_message(message.chat.id, 'Введите адрес по которому будет производится уборка')
        bot.register_next_step_handler(message, location_f)
    elif message.text == 'Влажная уборка':
        bot.send_message(message.chat.id, 'Вы выбрали "Сухую уборку"')
        bot.send_message(message.chat.id, 'Данная опция не доступная. Извините за временные неудобства')
    elif message.text == 'Чистка ковров':
        bot.send_message(message.chat.id, 'Вы сами доставите ковры или же к Вам выслать служебную машину?')
        reply_markup = telebot.types.ReplyKeyboardMarkup(True,True,1)
        button1 = telebot.types.KeyboardButton('Доставлю сам')
        button2 = telebot.types.KeyboardButton('Служебная машина')

    else:
        bot.send_message(message.chat.id, 'Мне нечего ответить')


def location_f(message):
    content_check(message)
    location.setdefault(message.from_user.id, message.text)
    bot.send_message(message.chat.id, f'{users.get(message.from_user.id)[0]}, Вы заказали уборку по адресу {location.get(message.from_user.id)}')


bot.polling(True)

#@bot.message_handler(func=)