from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.function import set_message_id, delete_message
from handlers.machine import FSMLieter, FSMFeedback
from config import bot
import markup


def send_email(sub, feed):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from platform import python_version

    server = 'smpt.mail.ru'
    user = "telebot_sne@inbox.ru"
    password = "JGW047hNrnZpL1zxyn6x"

    recipients = ['telebot_sne@inbox.ru']
    sender = 'telebot_sne@inbox.ru'
    subject = sub
    text = feed
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'TeleBot <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()


async def get_feedback(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMFeedback.annahme.set()
    m2u = await bot.send_message(callback_query.from_user.id, "Введите свой отзыв о нашем боте. Будем рады любому мнению!", reply_markup=markup.button_cancel())
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMFeedback.submit.set()



async def submit_feedback(message: types.Message, state: FSMContext):
    send_email(f"Feedback from User ({message.from_user.id}) {message.from_user.username}", message.text)
    m2u = await bot.send_message(message.from_user.id, "Спасибо за ваш отзыв!", reply_markup=markup.button_return())
    await delete_message(state, message.from_user.id)
    await set_message_id(state, m2u)


def register_handlers_feedback(dp: Dispatcher):
    dp.register_callback_query_handler(get_feedback, lambda callback_query: callback_query.data == "2", state=FSMLieter.menu)
    dp.register_message_handler(submit_feedback, state=FSMFeedback.submit)