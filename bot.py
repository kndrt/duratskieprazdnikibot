import telebot
import config
import datetime
import requests
from bs4 import BeautifulSoup as BS
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

from telebot import types
from telebot.types import ReplyKeyboardRemove, CallbackQuery

bot=telebot.TeleBot(config.TOKEN)


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")




@bot.message_handler(commands=["start"])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("сегодня", callback_data="today"),
        telebot.types.InlineKeyboardButton(
            "выбрать другую дату", callback_data="another"
        ),
    )
    bot.send_message(
        message.chat.id, "добрый день!\nхотите посмотреть праздники сегодня или выбрать другую дату?", parse_mode='html', reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
  
    name, action, year, month, day = call.data.split(calendar_1.sep)

    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "DAY":
        n=day
        month=int(month)
        if month == 1:
            k='yanvarya'
        elif month == 2:
            k='fevralya'
        elif month == 3:
            k='marta'
        elif month == 4:
            k='aprelya'
        elif month == 5:
            k='maya'
        elif month == 6:
            k='iunya'
        elif month == 7 :
            k='iulya'
        elif month == 8 :
            k='avgusta'
        elif month == 9:
            k='sentyabrya'
        elif month == 10:
            k='oktyabrya'
        elif month == 11:
            k='noyabrya'
        elif month == 12:
            k='dekabrya'
        c='prazdniki-'+str(n)+'-'+k+'.html'
        url='https://kakoysegodnyaprazdnik.com/'+c
        r = requests.get(url)
        html = BS(r.content, 'html.parser')


        b=[]
        for el in html.select('#page-content'):
            for i in range(5):
                b.append(el.select('.first .block1')[i])

        bot.send_message(call.message.chat.id, "в этот день праздновали\nи будут праздновать:")
        for i in range (5):
          bot.send_message(call.message.chat.id, b[i])
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="если хотите продолжить, напишите /start",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1}: cancel")



@bot.callback_query_handler(func=lambda call: call.data.startswith("today"))
def callback_inline1(call: CallbackQuery):


    if call.data == "today":
        url='https://kakoysegodnyaprazdnik.com/'
        r = requests.get(url)
        html = BS(r.content, 'html.parser')


        b=[]
        for el in html.select('#page-content'):
            for i in range(5):
                b.append(el.select('.first .block1')[i])

        bot.send_message(call.message.chat.id, "поздравляем, сегодня празднуют:")
        for i in range (5):
          bot.send_message(call.message.chat.id, b[i])

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
@bot.callback_query_handler(func=lambda call: call.data.startswith("another"))
def callback_inline2(call: CallbackQuery):

    if call.data == "another":
        now = datetime.datetime.now()  
        bot.send_message(
        call.message.chat.id,
        "выберите дату, пожалуйста",
        reply_markup=calendar.create_calendar(
            name=calendar_1.prefix,
            year=now.year,
            month=now.month,
        )
    )
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True)

