from telethon import TelegramClient, sync, events
from pprint import pprint
import speech_recognition as sr
import os
import datetime
from pydub import AudioSegment

#todo 
# разбивать большие файлы
# удалять файлы, если не получилось распознать

api_id = 00000
api_hash = '111111111aaaa222222bbbbb3333ccccc'
client = TelegramClient('colocol', api_id, api_hash).start()

@client.on(events.NewMessage())
async def normal_handler(event):
	# print(event.message.voice)
	# print(event.message.date)
	name = event.message.date.strftime("voice_%Y-%m-%d_%H-%M-%S")
	if event.message.voice:
		path = await event.message.download_media()

	def recog(audio):
		AudioSegment.from_file(f'{os.getcwd()}/{audio}.oga').export(f'{os.getcwd()}/{audio}.wav', format="wav")
		r = sr.Recognizer()
		sample_audio = sr.AudioFile(f'{os.getcwd()}/{audio}.wav')
		with sample_audio as audio_file:
				audio_content = r.record(audio_file)
		os.remove(f'{os.getcwd()}/{audio}.wav')
		os.remove(f'{os.getcwd()}/{audio}.oga')
		return r.recognize_google(audio_content, language="ru-RU")

	text = recog(name).replace('*', '-')
	await event.message.reply(text)

client.start()
client.run_until_disconnected()