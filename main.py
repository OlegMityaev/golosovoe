import telebot
import requests
import random
import speech_recognition as sr
import os
import pyttsx3
import time
from pydub import AudioSegment

AudioSegment.converter = os.getcwd() + "\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = os.getcwd() + "\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = os.getcwd() + "\\ffmpeg\\bin\\ffprobe.exe"

token = '5196113982:AAEQZS_y9IfQuEs8lHKGRVftS0Yq-_vftsI'
bot = telebot.TeleBot(token)

text_to_speach = pyttsx3.init()
engine = pyttsx3.init()
voices = text_to_speach.getProperty('voices')
for voice in voices:
    print('--------------------')
    print('Имя: %s' % voice.name)
    print('ID: %s' % voice.id)

RU_VOICE_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
text_to_speach.setProperty('voice', voice[0].id)  #changing index, changes voices. o for male
# text_to_speach.setProperty('voice', voice[0].id)


@bot.message_handler(commands=["start"])
def bot_messages(message):
    bot.send_message(message.chat.id, 'Привет! Чем я могу вам помочь? :)')

@bot.message_handler(content_types=["text"])
def bot_messages(message):
    text = message.text.lower()
    if 'произнеси' in text and text.split(' ')[0] == 'произнеси':
        src = str(message.chat.id) + str(message.message_id) + '_answer.oga'
        text_to_speach.save_to_file(text[9:], src)
        text_to_speach.runAndWait()
        time.sleep(1)
        voice = open(src, 'rb')
        bot.send_audio(message.chat.id, voice)
    elif 'повтори' in text and text.split(' ')[0] == 'повтори':
        bot.send_message(message.chat.id, 'Повторяю: ' + text[7:])
    elif 'сайт' == text:
        bot.send_message(message.chat.id, 'Сайт NTA: https://newtechaudit.ru/')
    elif 'своё имя' in text or 'как тебя зовут' in text or 'назови себя' in text:
        bot.send_message(message.chat.id,'Меня зовут Bot!')
    elif 'случайное число' in text and 'от' in text and 'до' in text:
        ot=text.find('от')
        do=text.find('до')
        f_num=int(text[ot+3:do-1])
        l_num=int(text[do+3:])
        bot.send_message(message.chat.id, str(random.randint(f_num, l_num)))
    elif 'random ' in text:
        if len(text.split(' ')) == 2:
            bot.send_message(message.chat.id, str(random.randint(0, int(text.split(' ')[1]))))
        elif len(text.split(' ')) == 3:
            bot.send_message(message.chat.id, str(random.randint(int(text.split(' ')[1]), int(text.split(' ')[2]))))
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Попробуйте: "rand X" или "rand X Y"')
    elif 'пока' == text or 'до свидания' == text:
        bot.send_message(message.chat.id, 'До свидания!')
    else:
        bot.send_message(message.chat.id, 'Не понял команду :(')

@bot.message_handler(content_types=["voice"])
def bot_messages(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    src = file_info.file_path[:6] + 'oga' + file_info.file_path[5:]
    dst = file_info.file_path[:6] + 'wav' + file_info.file_path[5:-3] + 'wav'
    with open(src,'wb') as f:
        f.write(file.content)
    sound = AudioSegment.from_oga(src)
    sound.export(dst, format="wav")
    del sound
    rec = sr.Recognizer()
    with sr.WavFile(dst) as source:
        audio = rec.record(source)
    try:
        text = rec.recognize_google(audio, language="ru-RU").lower()
        error = 0
    except LookupError:
        bot.send_message(message.chat.id, 'Не понимаю Ваш восхитительный голос :(')
        error = 1
    if error == 0:
        if 'произнеси' in text and text.split(' ')[0] == 'произнеси':
            text_to_speach.save_to_file(text[9:], file_info.file_path[:6] + 'answer' + file_info.file_path[5:])
            text_to_speach.runAndWait()
            time.sleep(1)
            voice = open( file_info.file_path[:6]+'answer'+ file_info.file_path[5:], 'rb')
            bot.send_audio(message.chat.id, voice)
        elif 'повтори' in text and text.split(' ')[0] == 'повтори':
            bot.send_message(message.chat.id, 'Повторяю: ' + text[7:])
        elif 'сайт' == text:
            bot.send_message(message.chat.id, 'Сайт NTA: https://newtechaudit.ru/')
        elif 'своё имя' in text or 'как тебя зовут' in text or 'назови себя' in text:
            bot.send_message(message.chat.id,'Меня зовут Bot!')
        elif 'случайное число' in text and 'от' in text and 'до' in text:
            ot=text.find('от')
            do=text.find('до')
            f_num=int(text[ot+3:do-1])
            l_num=int(text[do+3:])
            bot.send_message(message.chat.id, str(random.randint(f_num, l_num)))
        elif 'random ' in text:
            if len(text.split(' ')) == 2:
                bot.send_message(message.chat.id, str(random.randint(0, int(text.split(' ')[1]))))
            elif len(text.split(' ')) == 3:
                bot.send_message(message.chat.id, str(random.randint(int(text.split(' ')[1]), int(text.split(' ')[2]))))
            else:
                bot.send_message(message.chat.id, 'Неверный формат. Попробуйте: "rand X" или "rand X Y"')
        elif 'пока' == text or 'до свидания' == text:
            bot.send_message(message.chat.id, 'До свидания!')
    else:
        bot.send_message(message.chat.id, 'Не понял команду :(')

if __name__ == '__main__':
    bot.infinity_polling()