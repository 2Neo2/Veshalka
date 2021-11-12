from django.core.management.base import BaseCommand
import telebot
from bot.models import Profile, Item, Match
import random

class Command(BaseCommand):
	help = 'Телеграмм бот'

	def handle(self, *args, **options):
		bot = telebot.TeleBot("2129696474:AAGVE2Kyk34SoqSwKsfwblCpnklcVGTdLxo")
		start_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
		start_menu.row('Все товары', 'Мои товары')
		typeOfSex = ''
		typeOfClothes = ''
		@bot.message_handler(commands=['start'])
		def start(message):
			try:
				profile = Profile.objects.get(tg_id=message.chat.id)
			except:
				if (message.chat.username == None):
					profile = Profile.objects.create(tg_id=message.chat.id, tg_name='У пользователя нет tg_name')
				else:
					profile = Profile.objects.create(tg_id=message.chat.id, tg_name=message.chat.username)

			bot.send_message(message.chat.id, 'Мы предоставляем уникальную площадку для обмена вещами👗👠\nЕсли твой элемент гардероба в хорошем качестве, и ты знаешь, на что хочешь его поменять, скорее пиши! А если ещё не определился, то мы постараемся помочь и сами предложим что-нибудь интересное💁\nПомни, что не стоит предлагать вещи ненадлежащего качества 💩 (которые ты сам не хотел бы получить взамен).\nСмелее загружай фотографии своей вещи, укажи необходимую информацию и опиши свои пожелания, но не забывай, что мы заботимся о пользователях, поэтому все предложения будут модерироваться нашими специалистами👮‍♀ 🔎\nНажимая кнопку ниже, ты соглашаешься с нашей политикой хранения, обработки и передачи данных🙌' , reply_markup=start_menu)

		@bot.message_handler(content_types=['text'])
		def text(message):
			profile = Profile.objects.get(tg_id=message.chat.id)
			if message.text == 'Все товары':
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('Без разницы')
				menu.row('Описать товар')
				menu.row('В главное меню')
				bot.send_message(message.chat.id, 'Какие варианты рассмотрим сегодня?', reply_markup=menu)
			
			if message.text == 'Мои товары':
				my_items = Item.objects.filter(profile=profile)
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('В главное меню')
				menu.row('Добавить товар')
				menu.row('Мои лайки')
				menu.row('Мои мэтчи')
				menu.row('Мои товары')

				if len(my_items) == 0:
					bot.send_message(message.chat.id, 'У вас нет добавленных товаров', reply_markup=menu)
				else:
					bot.send_message(message.chat.id, 'Список ваших товаров:', reply_markup=menu)
					for item in my_items:
						markup = telebot.types.InlineKeyboardMarkup()
						markup.row(telebot.types.InlineKeyboardButton(text='Удалить товар', callback_data=f'delete {item.id}'))
						# bot.send_photo(message.chat.id, open(item.image.path, 'rb'),caption=str(item), reply_markup=markup)
						bot.send_message(message.chat.id, str(item), reply_markup=markup)
			if message.text == 'Мои мэтчи':
				my_matches = Match.objects.filter(profile=Profile.objects.get(tg_id=message.chat.id))
				for match in my_matches:
					user_matches = Match.objects.filter(profile=match.item.profile)
					for user_match in user_matches:
						if user_match.item.profile == Profile.objects.get(tg_id=message.chat.id):
							bot.send_message(message.chat.id, f'@{user_match.profile.tg_name}')
							bot.send_message(message.chat.id, f'Ваш товар\n{user_match.item}')
							bot.send_message(message.chat.id, f'Его товар\n{match.item}')
			if message.text == 'Мои лайки':
				matches = Match.objects.filter(profile=Profile.objects.get(tg_id=message.chat.id))
				for match in matches:
					markup = telebot.types.InlineKeyboardMarkup()
					markup.row(telebot.types.InlineKeyboardButton(text='Больше не нравится', callback_data=f'delete_match {match.id}'))
					bot.send_message(message.chat.id, match.item, reply_markup=markup)
			if message.text == 'В главное меню':
				bot.send_message(message.chat.id, 'Мы предоставляем уникальную площадку для обмена вещами👗👠\nЕсли твой элемент гардероба в хорошем качестве, и ты знаешь, на что хочешь его поменять, скорее пиши! А если ещё не определился, то мы постараемся помочь и сами предложим что-нибудь интересное💁\nПомни, что не стоит предлагать вещи ненадлежащего качества 💩 (которые ты сам не хотел бы получить взамен).\nСмелее загружай фотографии своей вещи, укажи необходимую информацию и опиши свои пожелания, но не забывай, что мы заботимся о пользователях, поэтому все предложения будут модерироваться нашими специалистами👮‍♀ 🔎\nНажимая кнопку ниже, ты соглашаешься с нашей политикой хранения, обработки и передачи данных🙌', reply_markup=start_menu)
			if message.text == 'Добавить товар':
				markup = telebot.types.InlineKeyboardMarkup()
				markup.row(telebot.types.InlineKeyboardButton(text='Перейти', url=f'http://127.0.0.1:8000/add_item/{profile.tg_id}/'))
				bot.send_message(message.chat.id, 'Для добавления товара перейдите на специальную форму', reply_markup=markup)
			if message.text == 'Без разницы':
				itemsAll = list(Item.objects.all())
				itemsClient = list(Item.objects.filter(profile=Profile.objects.get(tg_id=message.chat.id)))
				itemOut = []
				for item in itemsAll:
					if item not in itemsClient:
						itemOut.append(item)
				markup = telebot.types.InlineKeyboardMarkup()
				markup.row(telebot.types.InlineKeyboardButton(text='Нравится', callback_data=f'like {item.id}'))
				markup.row(telebot.types.InlineKeyboardButton(text='Не нравится', callback_data=f'dislike {item.id}'))
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('В главное меню')
				bot.send_message(message.chat.id, 'Это товар:', reply_markup=menu)
				bot.send_message(message.chat.id, itemOut[random.randint(0, len(itemOut) - 1)], reply_markup=markup)
			if message.text == 'Описать товар':
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('В главное меню')
				menu.row('Мужское')
				menu.row('Женское')
				menu.row('Унисекс')
				bot.send_message(message.chat.id, 'Укажите ваш пол: ', reply_markup=menu)
			if message.text == 'Мужское' or message.text == 'Женское' or message.text == 'Унисекс':
				typeOfSex = message.text
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('В главное меню')
				menu.row('Верхняя одежда 🧥👘')
				menu.row('Верхний элемент гардероба 👕👗')
				menu.row('Нижний элемент гардероба 👖🩳')
				menu.row('Обувь 👠🩰')
				menu.row('Аксессуары 👜📿')
				menu.row('Нижнее или ночное белье 👙🩲')
				bot.send_message(message.chat.id, 'Выберите категорию товара:', reply_markup=menu)
			if message.text == 'Верхняя одежда 🧥👘' or message.text == 'Верхний элемент гардероба 👕👗' or message.text == 'Нижний элемент гардероба 👖🩳' or message.text =='Обувь 👠🩰' or message.text =='Аксессуары 👜📿' or message.text =='Нижнее или ночное белье 👙🩲':
				typeOfClothes = message.text


		@bot.callback_query_handler(func=lambda call:True)
		def callback(call):
			if call.data.split()[0] == 'delete_match':
				match = Match.objects.get(id=int(call.data.split()[1]))
				match.delete()
				bot.send_message(call.message.chat.id, 'Товар удален из списка лайкнутых')
			if call.data.split()[0] == 'delete':
				item = Item.objects.get(id=int(call.data.split()[1]))
				item.delete()
				bot.send_message(call.message.chat.id, 'Товар удален')
			if call.data.split()[0] == 'cancelLike':
				item = Match.objects.get(id=int(call.data.split()[1]))
				item.delete()
				bot.send_message(call.message.chat.id, 'Лайк убран')
			if call.data.split()[0] == 'like':
				match = Match.objects.create(profile=Profile.objects.get(tg_id=call.message.chat.id), item=Item.objects.get(id=int(call.data.split()[1])))
				match.save()
				check = False
				# Выводит мэтч если я лайкнйл свой товар несколько раз, после отображения мэтча не появляется следующий товар. Хуйня полная переделать.
				profile_items = Item.objects.filter(profile=Profile.objects.get(tg_id=call.message.chat.id))
				for item in profile_items:
					item_matches = Match.objects.filter(item=item)
					for item_match in item_matches:
						if match.item.profile == item_match.profile:
							bot.send_message(call.message.chat.id, f'У вас мэтч, вот контакт человека @{item_match.profile.tg_name}')
							bot.send_message(call.message.chat.id, item_match.item)
							check = True
							break

				if check == False:
					bot.send_message(call.message.chat.id, 'Товар добавлен в список лайкнутых')
					itemsAll = list(Item.objects.all())
					itemsClient = list(Item.objects.filter(profile=Profile.objects.get(tg_id=call.message.chat.id)))
					itemOut = []
					for item in itemsAll:
						if item not in itemsClient:
							itemOut.append(item)
					markup = telebot.types.InlineKeyboardMarkup()
					markup.row(telebot.types.InlineKeyboardButton(text='Нравится', callback_data=f'like {item.id}'))
					markup.row(telebot.types.InlineKeyboardButton(text='Не нравится', callback_data=f'dislike {item.id}'))
					menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
					menu.row('В главное меню')
					bot.send_message(call.message.chat.id, 'Это товар:', reply_markup=menu)
					bot.send_message(call.message.chat.id, itemOut[random.randint(0, len(itemOut) - 1)], reply_markup=markup)

			if call.data.split()[0] == 'dislike':
				itemsAll = list(Item.objects.all())
				itemsClient = list(Item.objects.filter(profile=Profile.objects.get(tg_id=call.message.chat.id)))
				itemOut = []
				for item in itemsAll:
					if item not in itemsClient:
						itemOut.append(item)
				markup = telebot.types.InlineKeyboardMarkup()
				markup.row(telebot.types.InlineKeyboardButton(text='Нравится', callback_data=f'like {item.id}'))
				markup.row(telebot.types.InlineKeyboardButton(text='Не нравится', callback_data=f'dislike {item.id}'))
				menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
				menu.row('В главное меню')
				bot.send_message(call.message.chat.id, 'Это товар:', reply_markup=menu)
				bot.send_message(call.message.chat.id, itemOut[random.randint(0, len(itemOut) - 1)], reply_markup=markup)

		bot.polling(none_stop=True)