from aiogram import types
from loguru import logger
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot
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


class FSM_feedback(StatesGroup):
    get_message = State()


async def get_feedback(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите свой отзыв о нашем боте. Будем рады любому мнению!",
                           reply_markup=markup.cancel_button())
    await FSM_feedback.get_message.set()


async def submit_feedback(message: types.Message, state: FSMContext):
    if message.text != 'Отменить':
        send_email(f"Feedback from User ({message.from_user.id}) {message.from_user.username}", message.text)
        await bot.send_message(message.from_user.id, "Спасибо за ваш отзыв!")
        logger.info(f"User ({message.from_user.id}) {message.from_user.username} send feedback!")
    await bot.send_message(message.from_user.id, "Возвращаю вас в меню...", reply_markup=markup.menu_buttons())
    await state.finish()


def register_handlers_feedback(dp: Dispatcher):
    dp.register_message_handler(get_feedback, lambda message: message.text == "Обратная связь")
    dp.register_message_handler(submit_feedback, state=FSM_feedback.get_message)