import telebot
import telebot.types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg
import tokens
from db import Database #For future database (database.db)


bot = telebot.TeleBot(tokens.TOKEN)

def _(text, lang='ru'): #Localization function
    try:
        return cfg.locale[lang][text]
    except:
        return text
    
def mkButton(buttonName):
    button = InlineKeyboardButton(_(buttonName), callback_data=buttonName)
    return button

def sendMsgWithInterface(uid, name='menu', path=None):    
    buttons = []
    markup = InlineKeyboardMarkup()
    
    if path != None:
        name = cfg.markups[path][name]
    else:
        name = cfg.markups[name]
    
    for button in name:
        if button != 'name':
            buttons.append(mkButton(button))
    markup.add(*buttons)
    bot.send_message(uid, _(name['name']), reply_markup=markup)
    
def permCheck(message):
    if message.chat.id in cfg.permUsers:
        return True
    else:
        bot.send_message(message.chat.id, message.from_user.first_name + " ,you didn't have permission to use this bot. Please go away!")
        return False
    

@bot.message_handler(commands=['start'])
def start(message):
    if permCheck(message):
        bot.send_message(message.chat.id, f"{_('hello')}, {message.from_user.first_name}!")
        menu(message)
        
@bot.message_handler(commands=['menu']) #Bot main menu
def menu(message):
    if permCheck(message):
        sendMsgWithInterface(uid=message.chat.id, name='menu')
        
@bot.message_handler(commands=['servers'])
def servers(message):
    if permCheck(message): 
        sendMsgWithInterface(uid=message.chat.id, path='menu', name='servers')
    
@bot.message_handler(commands=['servers_minecraft'])
def servers_minecraft(message):
    if permCheck(message):
        pass
        
        
        

@bot.callback_query_handler(func=lambda call: True) #All callbacks
def callback_inline(call):
    if call.data == 'servers':
        servers(call.message)
    elif call.data == 'servers_minecraft':
        pass
    elif call.data == 'servers_factorio':
        pass
    
@bot.message_handler(commands=['messagedata']) #Debug Function
def messagedata(message):
    bot.send_message(message.chat.id, message)
    
@bot.message_handler(commands=['myuid']) #Debug Function
def myuid(message):
    bot.send_message(message.chat.id, message.chat.id) 
    
    
    
    
bot.polling(none_stop=True)