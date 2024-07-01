import cv2
import time
import serial
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
# Arduino bağlantısını yap
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)

# Bot token'ını oku
with open("TheEyeToken.txt", "r") as f:
    TOKEN = f.read()

# Updater ve Dispatcher oluştur
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# CommandHandler ve CallbackQueryHandler fonksiyonları
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Geliştirici", callback_data='developer')],
        [InlineKeyboardButton("Proje Raporu", callback_data='report')],
        [InlineKeyboardButton("Kim Var? (Resim)", callback_data='who_is_here_photo')],
        [InlineKeyboardButton("Kim Var? (Video)", callback_data='who_is_here_video')],
        [InlineKeyboardButton("Kapıyı Aç", callback_data='open_door')],
        [InlineKeyboardButton("Komut Listesi", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("<b>TheEye Projesine Hoşgeldiniz</b>", parse_mode='HTML', reply_markup=reply_markup)

def HasanDenizhan(update: Update, context: CallbackContext):
    # Check if update.message is available
    if update.message:
        update.message.reply_text("<b>Linkedin profili : https://www.linkedin.com/in/hasan-denizhan-61409b208/</b>",
                                  parse_mode='HTML')
    elif update.callback_query:
        # Use update.callback_query.message.reply_text to reply to the message associated with the callback query
        update.callback_query.message.reply_text("<b>Linkedin profili : https://www.linkedin.com/in/hasan-denizhan-61409b208/</b>",
                                                 parse_mode='HTML')

def help(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Geliştirici", callback_data='developer')],
        [InlineKeyboardButton("Proje Raporu", callback_data='report')],
        [InlineKeyboardButton("Kim Var? (Resim)", callback_data='who_is_here_photo')],
        [InlineKeyboardButton("Kim Var? (Video)", callback_data='who_is_here_video')],
        [InlineKeyboardButton("Kapıyı Aç", callback_data='open_door')],
        [InlineKeyboardButton("Komut Listesi", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text("<b>Yardım Menüsü</b>", parse_mode='HTML', reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.reply_text("<b>Yardım Menüsü</b>", parse_mode='HTML', reply_markup=reply_markup)

def kapiAc(update: Update, context: CallbackContext):
    if update.message:
        update.message.reply_text("KAPI ACILDI")
    elif update.callback_query:
        # Use update.callback_query.message.reply_text to reply to the message associated with the callback query
        update.callback_query.message.reply_text("KAPI ACILDI")
    access_approved()

def rapor(update: Update, context: CallbackContext):
    if update.message:
        update.message.reply_text("<b>Rapor : https://1drv.ms/b/s!AlBalth4C6-3gl9IciFZ07V0lO8E?e=TrLrzr</b>", parse_mode='HTML')
    elif update.callback_query:
        # Use update.callback_query.message.reply_text to reply to the message associated with the callback query
        update.callback_query.message.reply_text("<b>Rapor : https://1drv.ms/b/s!AlBalth4C6-3gl9IciFZ07V0lO8E?e=TrLrzr</b>", parse_mode='HTML')
def take_pic():
    camera = cv2.VideoCapture(0)
    _, image = camera.read()
    cv2.imwrite('kapi.jpg', image)

def take_vid():
    camera = cv2.VideoCapture(0)
    video_kayit = cv2.VideoWriter('kapivideo.avi', cv2.VideoWriter.fourcc(*'XVID'), 25.0, (640, 480))
    baslangic_zamani = time.time()
    kayit_suresi = 5  # saniye
    while True:
        ret, videoGoruntu = camera.read()
        video_kayit.write(videoGoruntu)
        if time.time() - baslangic_zamani > kayit_suresi:
            break
        if cv2.waitKey(50) & 0xFF == ord('x'):
            break

def kkimvarR(update: Update, context: CallbackContext):
    if update.message:
        take_pic()
        photo = open('kapi.jpg', 'rb')
        update.message.reply_photo(photo)
    elif update.callback_query:
        # Use update.callback_query.message.reply_photo to reply to the message associated with the callback query
        take_pic()
        photo = open('kapi.jpg', 'rb')
        update.callback_query.message.reply_photo(photo)


def kkimvarV(update: Update, context: CallbackContext):
    if update.message:
        take_vid()
        chat_id = update.message.chat_id
        context.bot.send_video(chat_id=chat_id, video=open('kapivideo.avi', 'rb'), supports_streaming=True)
    elif update.callback_query:
        # Use update.callback_query.message.chat_id to get the chat ID associated with the callback query
        take_vid()
        chat_id = update.callback_query.message.chat_id
        context.bot.send_video(chat_id=chat_id, video=open('kapivideo.avi', 'rb'), supports_streaming=True)

def access_approved():
    arduino.write(b'3')

def button_click_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'developer':
        HasanDenizhan(update, context)
    elif query.data == 'report':
        rapor(update, context)
    elif query.data == 'who_is_here_photo':
        kkimvarR(update, context)
    elif query.data == 'who_is_here_video':
        kkimvarV(update, context)
    elif query.data == 'open_door':
        kapiAc(update, context)
    elif query.data == 'help':
        help(update, context)

# Handler'ları ekleyin
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("HasanDenizhan", HasanDenizhan))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("rapor", rapor))
dispatcher.add_handler(CommandHandler("kkimvarR", kkimvarR))
dispatcher.add_handler(CommandHandler("kkimvarV", kkimvarV))
dispatcher.add_handler(CommandHandler("kapiAc", kapiAc))
dispatcher.add_handler(CallbackQueryHandler(button_click_handler))

# Bot'u çalıştırın
updater.start_polling()
updater.idle()
