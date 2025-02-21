from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

gifts = {}

def get_gifts():
    with open('data/gifts.txt', 'r') as file1, open('data/max_counter.txt', 'r') as file2:
        for line1, line2 in zip(file1, file2):
            gifts[line1.strip()] = int(line2.strip())

get_gifts()

kb_sub = InlineKeyboardMarkup()
btn_sub = InlineKeyboardButton('Subscribe', callback_data='subscribe')
kb_sub.add(btn_sub)

kb_pay = InlineKeyboardMarkup()
btn_pay = InlineKeyboardButton(text='Pay 100 XTR', pay=True)
kb_pay.add(btn_pay)

kb_gifts = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_gifts.add(*gifts.keys())


