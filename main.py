from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import re
import datetime
from threading import Timer
from lxml.html import parse 
from lxml.html import fromstring
from lxml import html


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi!')

def getyearago(username):
    parsed_links = []
    urls = []
    date_now = datetime.date.today()
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    year_range = date_now.year - 2010 # Fetch tweetes from 2011 until now
    for i in range(1, year_range):
        respone = requests.get("https://mobile.twitter.com/search?q=from%3A{username}+"
				"since%3A{year}-{month}-{day}+until%3A{year1}-{month1}-{day1}+"
				"filter%3Amedia&s=typd&x=0&y=0".format(
                                    username=username, 
				    year=date_now.year-i,
                                    year1=date_tomorrow.year-i,
                                    month=date_now.month,
                                    month1=date_tomorrow.month,
                                    day=date_now.day,
                                    day1=date_tomorrow.day))
        tree = html.fromstring(respone.content)
        parsed_links = tree.xpath('//a/@data-url')
        for every_media in parsed_links:
            urls.append(every_media)
    logger.info("Trying")
    return urls

def yearsago(bot, update, args):
    if len(args) < 1:
        update.message.reply_text("Use /yearsago username")
        return

    photos = getyearago(args[0])

    logger.info("Found {} media".format(len(photos)))

    if len(photos) == 0: # If there isn't any media found
        update.message.reply_text("User doesn't have any media that posted exactly on this day years ago")

    for photo in photos:
        update.message.reply_text("This photo was taken exactly on this date years ago... {}".format(photo))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = ''
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yearsago", yearsago,
                                    pass_args=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
