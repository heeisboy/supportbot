import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

class st(StatesGroup):
	item = State()
	item2 = State()
	item3 = State()
	item4 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Добро пожаловать, админушка.', reply_markup=kb.menu)
		else:
			await message.answer(f'Вас приветствует поддержка магазина <b>😻MURMUR😻</b>\n\n'
								 f'Если у вас возникла проблема с оплатой, пришлите: \n\n'
								 f'▪️<b>Ваш ID</b> <i>(указан в профиле)</i>\n'
								 f'▪️<b>Номер карты или телефона</b> на который совершалось пополнение\n'
								 f'▪️<b>Сумма пополнения</b>\n'
								 f'▪️<b>Скриншот оплаты, на котором видно дату прислать отдельно оператору - @EL_SUPO</b>\n\n'
								 f'Чем <b>подробнее</b> вы опишите проблему, тем быстрее мы её решим!\n'
								 f'<i>Напишите Ваш вопрос или проблему и наш оператор ответит вам в ближайшее время!</i>', parse_mode="html")
	else:
		await message.answer('Вы получили ЧС.')

@dp.message_handler(commands=['info'])
async def inform(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		await message.answer(f'Если у вас возникла проблема с оплатой, пришлите: \n\n'
								 f'▪️<b>Ваш ID</b> <i>(указан в профиле)</i>\n'
								 f'▪️<b>Номер карты или телефона</b> на который совершалось пополнение\n'
							 	 f'▪️<b>Сумма пополнения</b>\n'
								 f'▪️<b>Скриншот оплаты, на котором видно дату прислать отдельно оператору - @EL_SUPPO</b>\n\n', parse_mode="html")
	else:
		await message.answer('Вы получили ЧС.')

@dp.message_handler(commands=['work'])
async def inform(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		await message.answer(f'🔘 <b>ПРИГЛАШАЕМ ВСЕХ ЖЕЛАЮЩИХ НА РАБОТУ</b>\n\n'
							 f'💸 Свободные вакансии:\n'
							 f'🚴‍♀️<b>Kypbep:</b> 1gr- 400rub (за KLAD)💰 2gr- 500rub (за KLAD) \n\n'
							 f'Возможность карьерного роста до <b>SKLADA!</b>\n'
							 f'Трудоустройство по документам, Или по залогу OT 5000р❗\n\n'
							 f'Для более точной информации пишем: <b>@EL_SUPO</b> 🔥🔥🔥\n'
							 f'Набираем персонал, оставшийся без работы! Высокооплачиваемая работа, ЗП от 80 000 рублей в неделю!', parse_mode="html")
	else:
		await message.answer('Вы получили ЧС.')



@dp.message_handler(content_types=['text'], text='👑 Админка')
async def handfler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Добро пожаловать в админ-панель.', reply_markup=kb.adm)

@dp.message_handler(content_types=['text'], text='⏪ Назад')
async def handledr(message: types.Message, state: FSMContext):
	await message.answer('Добро пожаловать, админушка.', reply_markup=kb.menu)

@dp.message_handler(content_types=['text'], text='👿 ЧС')
async def handlaer(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			q.execute(f"SELECT * FROM users WHERE block == 1")
			result = q.fetchall()
			sl = []
			for index in result:
				i = index[0]
				sl.append(i)

			ids = '\n'.join(map(str, sl))
			await message.answer(f'ID пользователей в ЧС:\n{ids}')

@dp.message_handler(content_types=['text'], text='✅ Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=kb.back)
			await st.item3.set()

@dp.message_handler(content_types=['text'], text='❎ Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=kb.back)
			await st.item4.set()

@dp.message_handler(content_types=['text'], text='💬 Рассылка')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Введите текст для рассылки.\n\nДля отмены нажмите на кнопку ниже', reply_markup=kb.back)
			await st.item.set()

@dp.message_handler(content_types=['text'])
@dp.throttled(func.antiflood, rate=3)
async def h(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			pass
		else:
			await message.answer('Сообщение отправлено.\nОжидайте ответа.')
			await bot.send_message(admin, f"<b>Получен новый вопрос!</b>\n<b>От:</b> {message.from_user.mention}\nID: {message.chat.id}\n<b>Сообщение:</b> {message.text}", reply_markup=kb.fun(message.chat.id), parse_mode='HTML')
	else:
		await message.answer('Вы добавлены в ЧС бота.')


@dp.callback_query_handler(lambda call: True) # Inline часть
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('Введите ответ:', reply_markup=kb.back)
		await st.item2.set() # админ отвечает пользователю
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('Удалено')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()

@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('Сообщение отправлено.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, 'Вам поступил ответ от администратора:\n\nТекст: {}'.format(message.text))

@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == '⏪ Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('Рассылка начата!', reply_markup=kb.adm)
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('Рассылка завершена!', reply_markup=kb.adm)
		await state.finish()


@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):
	if message.text == '⏪ Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 0:
					q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('Пользователь успешно забанен.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'Вы были добавлены администрацией в ЧС.')
				else:
					await message.answer('Данный пользователь уже получил бан.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Эйй!,Ты вводишь буквы...\nВведи ID')

@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ Отмена':
		await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 1:
					q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('Пользователь успешно разбанен.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
				else:
					await message.answer('Данный пользователь не получил бан.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Ты вводишь буквы...\nВведи ID')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)