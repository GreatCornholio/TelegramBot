# coding: cp1251

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import re
import time
import requests
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.user import User

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')
    print("start")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=
"""
Бот в текущий момент умеет
/start - он вроде по-умолчанию включается, но если бот тупит, то стоит написать
/help - этот хелп
/usdrub - получить текущий usdrub forex
/eurrub - получить текущий eurrub forex
/trans <...text...>  - хуефикация (ввести фразу после команды /trans)
/weather - пока погода слабенькая, но что бог послал
#/wu - weather underground точнее по осадкам, но в данный момент неправильно считает текущий час. если он показывает 2, то это значит, что строчка прогноза на 5 часов

в планах:
- погода в клг на несколько дней.
- погода в клг по часам на день

баги отправлять @sovinogaz
""")
    print("help")

def huefy(text, target, result):
    m = re.search(".*\s+?(.*" + target + ")\s*.*|^(.*" + target + ")\s*.*", text)
    if m != None:
        before = m.group(1)
        if before ==None:
            before = m.group(2)
        after = result
        txt = before + " - " + after
        #bot.sendMessage(update.message.chat_id, text=txt)
        return txt
    else:
        return ""
        #print(before, after)

def echo(bot, update):
    print ("echo")
    f = open('echobotlog.txt', 'a')
#    f.write(str(update.message.date) + " " + str(update.message.from_user) +"\n")
    f.write(str(update.message.date) + " " + str(update.message.from_user) +"\n")
#    f.write(update.message.text.encode('cp1251'))
    f.write(str(update.message.text + "\n"))
    f.close()

   #'этот код от эхо
   # bot.sendMessage(update.message.chat_id, text=update.message.text)


    print(update.message.text)
#    print(update.message.date, update.message.from_user.username, update.message.from_user.first_name, update.message.from_user.last_name)
    print(update.message.date, str(update.message.from_user))
    s = update.message.text
    myouttext = ""
    if s.find("Навальный") != -1:
        myouttext += "Навальный" + " - "+"Овальный" + "\n"
#        bot.sendMessage(update.message.chat_id, text="Навальный"+" - "+"Овальный")
#        print("Навальный" + " - "+"Овальный")
     
    """
    rules = {"нька": "хуянька", 
             "тор": "хуятор", 
             "нка": "хуянка", 
             "дор": "хуидор", "сик": "хуесик"
            }
    for k in rules:
        txt = huefy(s, k, rules[k])
        if txt != "":
            myouttext += txt + "\n"
    """
    repdict = {"й":"й", "у":"ю", "е":"е",
               "ы":"и", "а":"я", "о":"е", "э":"е", 
		"я":"я", "и":"и", "ю":"ю",

	       "Й":"Й", "У":"Ю", "Е":"Е",
               "Ы":"И", "А":"Я", "О":"Е", "Э":"Е", 
		"Я":"Я", "И":"И", "Ю":"Ю"
                  }
#import re
    l = s.split()
    outlist = []
    for w in l:
        m = re.search("([цкнгшщзхфвпрлджчсмтбЦКНГШЩЗХФВПРЛДЖЧСМТБ]*?)([ЙуеыаоэяиюЙУЕЫАОЭЯИЮ]+?)(.*)", w)
        if m != None:
            if w[0] == w[0].upper():
                x = "Ху"
            else:
                x = "ху"
            outlist.append(w + "-" + x + repdict[m.group(2)] + m.group(3))

    for w in outlist:
        myouttext += w + " "

    if  myouttext != "":
# не дает отвечать в чат
        bot.sendMessage(update.message.chat_id, text=myouttext)
        print(myouttext)

def usdrub(bot, update):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get("http://www.forexpf.ru/ajaxnews/eurusdrub.php?src=0", headers=headers)
    m = re.search("USD\/RUB Forex - <b>(.*?)<\/b>", page.text)
    bot.sendMessage(update.message.chat_id, text=m.group(1))

def eurrub(bot, update):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get("http://www.forexpf.ru/ajaxnews/eurusdrub.php?src=1", headers=headers)
    m = re.search("EUR\/RUB Forex - <b>(.*?)<\/b>", page.text)   
    bot.sendMessage(update.message.chat_id, text=m.group(1))

def trans(bot, update):
    echo(bot, update)

def getweather(url):
    from lxml import html
    page = requests.get(url)
    tree = html.fromstring(page.content)

    hr = tree.xpath('//div[@id=\'detail-hourly\']/div[@class=\'clearfix\']/table/thead/tr/th/text()')
    tp = tree.xpath('//div[@id=\'detail-hourly\']/div[@class=\'clearfix\']/table/tr[@class=\'temp\']/td/text()')
    rn = tree.xpath('//div[@id=\'detail-hourly\']/div[@class=\'clearfix\']/table/tr[@class=\'rain \']/td/text()')

    strout = ""
    z = zip(hr[1:9], tp, rn)
    for x in z:
        strout += str(x) + "\n"
    return (strout, hr[8])

def weather(bot, update):
    sndmsg = "accuweather:\n('Time', 't', 'Rain%')\n"
    (strout, hr) = getweather('http://www.accuweather.com/en/ru/kaluga/293006/hourly-weather-forecast/293006')
    sndmsg += strout

    if (hr[-2:] == 'am'):
        nxt = int(hr[:-2]) + 1
    else:
        nxt = int(hr[:-2]) + 12 + 1

    (strout, hr) = getweather('http://www.accuweather.com/en/ru/kaluga/293006/hourly-weather-forecast/293006?hour=' + str(nxt))
    sndmsg += strout

    bot.sendMessage(update.message.chat_id, text=sndmsg)

def wu(bot, update):
    url = "https://api-ak.wunderground.com/api/c991975b7f4186c0/forecast10day/hourly10day/labels/astronomy10day/lang:EN/units:metric/v:2.0/bestfct:1/q/zmw:00000.1.27703.json?ttl=300&callback=weatherCallback"
    page = requests.get(url)
    txt = page.text
    txt = txt.replace('weatherCallback(' , "dict(")
    txt = txt[:-2]
    null = 1
    dc = eval(txt)

    txt = "H, t, Rain%, Rain volume\n"
    for h in range(0, 19):
        txt = txt + str(time.localtime(dc['forecast']['days'][0]['hours'][h]['date']['epoch']).tm_hour) + " " + str(dc['forecast']['days'][0]['hours'][h]['temperature']) +  " " + str(dc['forecast']['days'][0]['hours'][h]['pop']) +  " "  + str(dc['forecast']['days'][0]['hours'][h]['liquid_precip'])+  "\n "
        #print (time.localtime(dc['forecast']['days'][0]['hours'][h]['date']['epoch']).tm_hour, dc['forecast']['days'][0]['hours'][h]['temperature'], dc['forecast']['days'][0]['hours'][h]['pop'], dc['forecast']['days'][0]['hours'][h]['liquid_precip'])
    bot.sendMessage(update.message.chat_id, text=txt)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    print("Starting app")
    updater = Updater("XXXXX_TOKEN!!!!!")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler("usdrub", usdrub))
    dp.addHandler(CommandHandler("eurrub", eurrub))
    dp.addHandler(CommandHandler("trans", trans))
    dp.addHandler(CommandHandler("weather", weather))
    dp.addHandler(CommandHandler("wu", wu))


    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()