import telebot
import config
import uuid
import scripts
import os
from flask import Flask, request

server = Flask(__name__)
bot = telebot.TeleBot(config.token, parse_mode=None)


@server.route("/", methods=["POST"])
def receive_update():
	bot.process_new_updates(
		[telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
	)
	return{'ok':True}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)




@bot.message_handler(content_types=['photo'])
def photo(message):
	print(message)
	word = message.caption
	fileID = message.photo[-1].file_id
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	save_way = "source_images/"+str(uuid.uuid1())+".jpg"    
	with open(save_way, 'wb') as new_file:
		new_file.write(downloaded_file)
	way = scripts.signature(save_way, word)
	os.remove(save_way)
	img = open(way, 'rb')
	bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
	os.remove(way)

@server.route("/" + config.token, methods=["POST"])
def getMessage():
	bot.process_new_updates(
		[
			telebot.types.Update.de_json(
				request.stream.read().decode("utf-8")
			)
		]
	)
	return "!", 200

if __name__ == "__main__":
	server.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))
