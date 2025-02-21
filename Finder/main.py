from telebot import TeleBot
from os import getenv
from dotenv import load_dotenv

from telebot.types import LabeledPrice

from Keyboard import *

load_dotenv()
bot = TeleBot(getenv('TOKEN'))
PASSWORD = getenv('PASSWORD')
PATH_TO_ID = 'data/id.txt'
PATH_TO_ADMIN_ID = 'data/admins_id.txt'
PATH_TO_GIFTS = 'data/gifts.txt'
PATH_TO_COUNTER = 'data/max_counter.txt'
LINK_TO_GIFT = 'https://t.me/nft/'
users = {}


def gift_to_link(name_gift: str):
    return LINK_TO_GIFT + name_gift.replace(' ', '').replace('-', '') + '-'


def write_id_to_file(user_id, path):
    f = open(path, 'r')
    all_id = f.read()
    f.close()
    if all_id.find(user_id) == -1:
        with open(path, 'a') as f:
            f.write(user_id + '\n')


def get_all_id_from_file():
    with open('data/id.txt', 'r') as f:
        for line in f:
            users[int(line)] = ['', 0]


def is_admin(user_id):
    with open(PATH_TO_ADMIN_ID, 'r') as f:
        all_id = f.read()
        if user_id in all_id:
            return True
    return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in users:
        bot.send_message(message.chat.id, 'You have already purchased a subscription', reply_markup=kb_gifts)
    else:
        bot.send_message(message.chat.id, '👋 Hello, I am BotFinder! 🤖\n'
                                          '🔧 Working with official API telegram 📱\n'
                                          '🎯 My mission is find gifts for you 🎁\n'
                                          '!!! After subscribe you can check your status, just send /start again !!!',
                         reply_markup=kb_sub)


@bot.message_handler(commands=['pass'])
def handle_login_admin(message):
    if is_admin(str(message.chat.id)):
        bot.send_message(message.chat.id, 'User already is admin')
        return
    if PASSWORD in message.text:
        write_id_to_file(str(message.chat.id), PATH_TO_ADMIN_ID)
        bot.send_message(message.chat.id, 'Successful login to admin')


@bot.message_handler(commands=['exit'])
def handle_exit_admin(message):
    if is_admin(str(message.chat.id)):
        open(PATH_TO_ADMIN_ID, 'w').close()
        bot.send_message(message.chat.id, 'Admin exited')


@bot.message_handler(commands=['add'])
def add_new_gift(message):
    if is_admin(str(message.chat.id)):
        command, name, count = str(message.text).split(' ')
        with open(PATH_TO_GIFTS, 'a') as f:
            f.write('\n' + name)
        with open(PATH_TO_COUNTER, 'a') as f:
            f.write('\n' + str(count))
        bot.send_message(message.chat.id, 'Info about new gift added successful')


@bot.message_handler(func=lambda message: message.text in gifts)
def handle_gift(message):
    if message.chat.id in users:
        if message.text in gifts:
            users[int(message.chat.id)][0] = message.text
            bot.send_message(message.chat.id, 'Send № (1 - ' + str(gifts[message.text]) +')')
    else:
        bot.send_message(message.chat.id, 'You have not subscribe', reply_markup=kb_sub)


@bot.message_handler(func=lambda message: message.text.isnumeric())
def handle_number(message):
    if message.chat.id in users and users[message.chat.id][0] != '':
        number = int(message.text)
        if 0 < number <= gifts[users[int(message.chat.id)][0]]:
            bot.send_message(message.chat.id, '[G I F T](' + gift_to_link(users[message.chat.id][0]) + str(number) + ')', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'Incorrect number')
    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'You have not subscribe', reply_markup=kb_sub)
        return
    if users[message.chat.id][0] == '':
        bot.send_message(message.chat.id, 'You must to choose model gift')


@bot.callback_query_handler(func=lambda call: call.data == 'subscribe')
def handle_subscribe(call):
    prices = [LabeledPrice(label='XTR', amount=100)]
    if call.data == 'subscribe':
        bot.send_invoice(call.message.chat.id,
                         title='Subscribe to Finder',
                         description='🔔 After subscribe, bot will find for you gifts 🎁 ✨',
                         invoice_payload='sub_purchase_payload',
                         provider_token='',
                         currency='XTR',
                         prices=prices,
                         reply_markup=kb_pay)
    bot.answer_callback_query(call.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    bot.send_message(message.chat.id, '✨ You have successfully paid for your subscription! 🌟\n'
                                      'Thank you for your support! 🎉 Now bot will find for you gifts! 🎁')
    write_id_to_file(str(message.chat.id), PATH_TO_ID)
    users[message.chat.id] = ['', 0]


def main():
    get_all_id_from_file()
    bot.infinity_polling()


if __name__ == '__main__':
    main()
