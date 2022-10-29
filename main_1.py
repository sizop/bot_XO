from telegram import ReplyKeyboardRemove
# from XO.show_field import show_field
from config import token
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import show_field as sf
import check_win as cw

# Определяем константы этапов разговора
fld = list(range(1, 10))
x = chr(10060)
o = chr(11093)
count = 9
player = x
CHOICE = 0




# функция обратного вызова точки входа в разговор
def start(update, _):
    global fld, player, count
    fld = list(range(1, 10))
    count = 9
    player = x
    update.message.reply_text("Hi, let's play tic-tac-toe")
    update.message.reply_text(sf.show_field(fld))
    update.message.reply_text(f'Go first {chr(10060)}')
    return CHOICE


def choice(update, _):
    global player, count
    move = update.message.text
    if move.isdigit() == False:
        update.message.reply_text(f"Incorrect input{chr(9940)}\nTry again")
    move = int(move)
    if move not in fld:
        update.message.reply_text(f"Incorrect input{chr(9940)}\nTry again")
    else:
        fld.insert(fld.index(move), player)
        fld.remove(move)
        update.message.reply_text(sf.show_field(fld))
        if cw.check_win(fld):
            update.message.reply_text(f"{player} - CHAMPION{chr(127942)}{chr(127881)}")
            return ConversationHandler.END
        player = o if player == x else x
        count -= 1

    if count == 0:
        update.message.reply_text(f"Draw {chr(129309)}")
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('Bye', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()