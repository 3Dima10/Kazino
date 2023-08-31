from aiogram import Dispatcher, Bot, executor, types
import logging
import mysql.connector
from config import user, password, host, database, token
from PIL import Image
from io import BytesIO
import time
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import random


##############################################################################
#---------------------------------MySQL Config-------------------------------#                                                                        
##############################################################################

config = {
    'user': user,
    'password': password,
    'host': host,
    'database': database,
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)

cursor = link.cursor()

#######################################
#--------------Config Bot-------------#
#######################################

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot=bot)

#########################################
#------------------random----------------#
#########################################

txt = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
rand = random.choice(txt)

#########################################
#------------------Start----------------#
#########################################

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    ##### SQL поиск#####
    query = f"INSERT INTO users (`id`, `schot`, `uan`, `polo`, `pbd`) VALUES ('{user_id}', 0, 0, 'try', 0);"
    cursor.execute(query)
    link.commit()
    #####################

    clav = types.ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура
    tp1 = types.KeyboardButton("Game 🕹")
    tp2 = types.KeyboardButton('Profile 👤')
    clav.add(tp1, tp2)

    await bot.send_message(message.chat.id,
                           "Добро пожаловать игрок, {0.first_name}! \n"
                           "Предлагаю тебе сыграть в игру если конечно ты не испугаешся \n"
                           .format(message.from_user),
                           parse_mode="html", reply_markup=clav)
###############################################################
#------------------Пользовательское соглашения----------------#
###############################################################

@dp.message_handler(commands=["recoint"])
async def recoint(message: types.Message):
    await bot.send_message(message.chat.id, 
                           text = "<a href='https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-08-19-5'>Пользовательское соглашение</a>",
                           parse_mode="html")
    
################################################

###########################################
#----------------Text---------------------#
###########################################
@dp.message_handler(content_types=['text'])
async def text(message):

    if message.chat.type == 'private':
        #Game
        if message.text == 'Game 🕹': 
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери во что будем играть")# Клавиатура
            gamek1 = types.KeyboardButton("Кости 🎲")# Клавиатура
            gamek2 = types.KeyboardButton("Слоты 🎰")# Клавиатура
            gamek3 = types.KeyboardButton("Рандом 🔢") # Клавиатура
            gamek4 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4)# Клавиатура

            await bot.send_message(message.chat.id,
                                   "Выбирите игру",
                                   reply_markup=clava2)#text
        
        ######---------Кости 🎲---------#####
        
        elif message.text == 'Кости 🎲':
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)# Клавиатура
            gamek1 = types.KeyboardButton("Больше")# Клавиатура
            gamek2 = types.KeyboardButton("Меньше")# Клавиатура
            gamek3 = types.KeyboardButton("Назад 🔙")# Клавиатура
            clava2.add(gamek1, gamek2, gamek3)# Клавиатура

            await bot.send_message(message.chat.id,
                                   "<b>Игра Больше - Меньше</b>\n"
                                   "Один раунд стоит 10 очков\n"
                                   "При проиграше вы тиряете ети 10 очков\n"
                                   "При выйграше вы зарабатываете 13 очков.\n"
                                   "Суть игры в том чтобы угадать какое число выпадит\n"
                                   "Больше = 4,5,6\n"
                                   "Меньше = 1,2,3\n",
                                   parse_mode='html',
                                   reply_markup=clava2) #text
        # Больше
        elif message.text == "Больше":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)# Клавиатура
            gamek1 = types.KeyboardButton("Больше")# Клавиатура
            gamek2 = types.KeyboardButton("Меньше")# Клавиатура
            gamek3 = types.KeyboardButton("Назад 🔙")# Клавиатура
            clava2.add(gamek1, gamek2, gamek3)# Клавиатура

            #####SQL поиск#####
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ###################
            if shot_value >= 10: # больше
                msg = await bot.send_dice(message.chat.id, emoji="🎲", reply_markup=clava2)
                dice_value = msg.dice.value
                # print(shot_value)
                # print(dice_value)
                
                # Победа
                if dice_value >= 4: # Больше
                    vol = int(shot_value) + 3
                    await bot.send_message(message.chat.id,f"+ 3 \n"
                                           f"{vol}")
                # Проиграш
                else:
                    vol = int(shot_value) - 5
                    await bot.send_message(message.chat.id,f"- 5 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()

                ######################################################
            
            # Недостаточно денег
            else:
                await bot.send_message(message.chat.id, "Недостатне коштив пополните счёт !!!!")

            # Меньше
        elif message.text == "Меньше":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            gamek1 = types.KeyboardButton("Больше")
            gamek2 = types.KeyboardButton("Меньше")
            gamek3 = types.KeyboardButton("Назад 🔙")
            clava2.add(gamek1, gamek2, gamek3)

            #####SQL поиск#####
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ###################
            if shot_value >= 10: # Менише
                msg = await bot.send_dice(message.chat.id, emoji="🎲", reply_markup=clava2)
                dice_value = msg.dice.value
                # print(shot_value)
                # print(dice_value)
                
                # Победа
                if dice_value <= 3: # меньше
                    vol = int(shot_value) + 3
                    await bot.send_message(message.chat.id,f"+ 3 \n"
                                           f"{vol}")
                    
                # Проиграш
                else:
                    vol = int(shot_value) - 5
                    await bot.send_message(message.chat.id,f"- 5 \n"
                                           f"{vol}")
                    
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                #######################################################
            
            # Недостаточно денег
            else:
                await bot.send_message(message.chat.id, "Недостатне коштив пополните счёт !!!!")
        
        ######---------Слоты---------#####
        
        elif message.text == "Слоты 🎰":
            # Клавиатура
            clava = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            tp = types.KeyboardButton("Старт")
            tp2 = types.KeyboardButton("Назад 🔙")
            clava.add(tp, tp2)

            # Правила
            await bot.send_message(message.chat.id, "<i><b>Каждый раунд стоит 5 очков</b></i>\n"
                                   "При каждой крутке вы тиряете 5 очков\n"
                                   "Нажмите Старт что бы начать\n"
                                   "<b>Комбинацый:</b>\n"
                                   "🍋🍋🍋 = 6 🪙\n"
                                   "🍒🍒🍒 = 8 🪙\n"
                                   "777 = 10 🪙\n"
                                   "bir = 15 🪙\n",
                                   reply_markup=clava)

        # Старт
        elif message.text == "Старт":

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            
            # Клавиатура
            clava = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            tp = types.KeyboardButton("Старт")
            tp2 = types.KeyboardButton("Назад 🔙")
            clava.add(tp, tp2)
            
            # Подщет денег
            if shot_value >= 5:
                msg = await bot.send_dice(message.chat.id, emoji="🎰", reply_markup=clava)
                dice_value = msg.dice.value
                
                # Лимояны
                if dice_value == 43:
                    vol = int(shot_value) + 6
                    await bot.send_message(message.chat.id,f"+ 6 \n"
                                           f"{vol}")
                # Вишни
                elif dice_value == 64:
                    vol = int(shot_value) + 8
                    await bot.send_message(message.chat.id,f"+ 8 \n"
                                           f"{vol}")
                    
                # Симерки
                elif dice_value == 22:
                    vol = int(shot_value) + 10
                    await bot.send_message(message.chat.id,f"+ 10 \n"
                                           f"{vol}")
                    
                # bir
                elif dice_value == 1:
                    vol = int(shot_value) + 15
                    await bot.send_message(message.chat.id,f"+ 15 \n"
                                           f"{vol}")
                    
                # Проиграш
                else:
                    vol = int(shot_value) - 5
                    await bot.send_message(message.chat.id,f"- 5 \n"
                                           f"{vol}")

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            
            # Недостаточно денег 
            else:
                await bot.send_message(message.chat.id, "Недостатне коштив пополните счёт !!!!")
        
        ######---------Главная---------#####
        
        elif message.text == "Главная 🏠":

            # Клавиатура
            clav = types.ReplyKeyboardMarkup(resize_keyboard=True)
            tp1 = types.KeyboardButton("Game 🕹")
            tp2 = types.KeyboardButton('Profile 👤')
            clav.add(tp1, tp2)

            # Текст
            await bot.send_message(message.chat.id,
                                   "Добро пожаловать Игрок, {0.first_name} ! \n"
                                   "Предлагаю тебе сыграть в игру если конечно ты не испугаешся \n"
                                   "Каждый раунд снимает 5 балов удачи тебе."
                                   .format(message.from_user),
                                   parse_mode="html", reply_markup=clav)
        
        ######---------Назад---------#####
        
        elif message.text == 'Назад 🔙':

            # Клавиатура
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери во что будем играть")# Клавиатура
            gamek1 = types.KeyboardButton("Кости 🎲")# Клавиатура
            gamek2 = types.KeyboardButton("Слоты 🎰")# Клавиатура
            gamek3 = types.KeyboardButton("Рандом 🔢") # Клавиатура
            gamek4 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4)# Клавиатура

            # Текст
            await bot.send_message(message.chat.id,
                                   "Начнем же игру",
                                   reply_markup=clava2)
            
        ######---------Профиль---------#####
        elif message.text == "Profile 👤":

            #####SQL поиск#####
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            #####################

            #####SQL поиск#####
            user_id = message.from_user.id
            colo = f"SELECT № FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            nomer_value = result[0]
            cursor.fetchall()
            #####################

            # Клавиатура
            clav = types.InlineKeyboardMarkup(row_width=1)
            it = types.InlineKeyboardButton("Пополнить", callback_data='good')
            it2 = types.InlineKeyboardButton("Снять", callback_data='good2')
            clav.add(it, it2)

            # Юзер имя
            user_first_name = message.from_user.first_name
            user_id = message.from_user.id
            
            # Текс
            await bot.send_message(message.chat.id, f"<b>Статус</b> \n"
                                   f"<b><i>📧Имя:</i></b> <i>{user_first_name}</i> \n"
                                   f"<b><i>👤id:</i></b> <i>{user_id}</i> \n"
                                   f"<b><i>№:</i></b> <i>{nomer_value}</i>\n"
                                   f"<b><i>💰Счет:</i></b><i>{shot_value}🪙</i> \n",
                                   parse_mode="html", reply_markup=clav)
        ######---------Коды---------######
        # Чит - код
        elif message.text == "admin : root":
            user_id = message.from_user.id
            query = f"UPDATE users SET schot = 100 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()

        # Промокод
        elif message.text == "roterdam":
            user_id = message.from_user.id
            query = f"UPDATE users SET schot = 50 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()

        # Дуся
        elif message.text == "2234432702":
            user_id = message.from_user.id
            query = f"UPDATE users SET schot = 1000 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()
            await bot.send_message(message.chat.id,
                                   "Привет Дуся, значит все таки догадался воспользоваца твойм промокодом.\n"
                                   "Уверен ты и не догадывался что твой 2 гривны финансирования когдато превратяца в 1000 вот тебе и инвистирование жыдяра блять 😂😂😂😂😂 просто шучу")

        ######---------Рандом---------######
        elif message.text == "Рандом 🔢":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура

            await bot.send_message(message.chat.id, 
                                   "Выбеоайте цыфру если она совпадет с той которой выкинет бот вы выйграли \n"
                                   "Цена : 50 монет\n"
                                   "Победа : 200 монет",
                                   reply_markup=clava2)
            

        elif message.text == "1️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            if shot_value >= 50:
                await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                if rand == "1":
                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                           f"{vol}")
                else:
                    vol = int(shot_value) - 50
                    await bot.send_message(message.chat.id,f"-50 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            else:
                await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "2️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT pbd FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            pbd_value = result[0]
            cursor.fetchall()
            ########################

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################

            if pbd_value == 3 :
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"2",  reply_markup=clava2)

                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################
                    
                    pbd = int(pbd_value) + 1
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = {pbd} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

            else: 
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                    if rand == "2":
                        vol = int(shot_value) + 200
                        await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    else:
                        vol = int(shot_value) - 50
                        await bot.send_message(message.chat.id,f"-50 \n"
                                               f"{vol}")
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "3️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            if shot_value >= 50:
                await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                if rand == "3":
                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                           f"{vol}")
                else:
                    vol = int(shot_value) - 50
                    await bot.send_message(message.chat.id,f"-50 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            
            else:
                await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "4️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            if shot_value >= 50:
                await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                if rand == "4":
                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                           f"{vol}")
                else:
                    vol = int(shot_value) - 50
                    await bot.send_message(message.chat.id,f"-50 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            
            else:
                await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "5️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)
            
            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT pbd FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            pbd_value = result[0]
            cursor.fetchall()
            ########################

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################

            if pbd_value < 2 :
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"5",  reply_markup=clava2)

                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    

                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                    pbd = int(pbd_value) + 1
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = {pbd} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

            else: 
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                    if rand == "5":
                        vol = int(shot_value) + 200
                        await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    else:
                        vol = int(shot_value) - 50
                        await bot.send_message(message.chat.id,f"-50 \n"
                                               f"{vol}")
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "6️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

                #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT pbd FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            pbd_value = result[0]
            cursor.fetchall()
            ########################

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################

            if pbd_value == 4 :
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"6",  reply_markup=clava2)

                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################
                    
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

            else: 
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                    if rand == "6":
                        vol = int(shot_value) + 200
                        await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    else:
                        vol = int(shot_value) - 50
                        await bot.send_message(message.chat.id,f"-50 \n"
                                               f"{vol}")
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "7️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            if shot_value >= 50:
                await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                if rand == "7":
                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                           f"{vol}")
                else:
                    vol = int(shot_value) - 50
                    await bot.send_message(message.chat.id,f"-50 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            
            else:
                await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "8️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################
            if shot_value >= 50:
                await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                if rand == "8":
                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                           f"{vol}")
                else:
                    vol = int(shot_value) - 50
                    await bot.send_message(message.chat.id,f"-50 \n"
                                           f"{vol}")
                ############SQL замена и запис результата#############
                query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################

                ############SQL замена и запис результата#############
                query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                cursor.execute(query)
                link.commit()
                ######################################################
            
            else:
                await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

        elif message.text == "9️⃣":
            clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Выбери цыфру")# Клавиатура
            gamek1 = types.KeyboardButton("1️⃣")# Клавиатура
            gamek2 = types.KeyboardButton("2️⃣")# Клавиатура
            gamek3 = types.KeyboardButton("3️⃣") # Клавиатура
            gamek4 = types.KeyboardButton("4️⃣") # Клавиатура
            gamek5 = types.KeyboardButton("5️⃣") # Клавиатура
            gamek6 = types.KeyboardButton("6️⃣") # Клавиатура
            gamek7 = types.KeyboardButton("7️⃣") # Клавиатура
            gamek8 = types.KeyboardButton("8️⃣") # Клавиатура
            gamek9 = types.KeyboardButton("9️⃣") # Клавиатура
            game10 = types.KeyboardButton("Главная 🏠")# Клавиатура
          
            clava2.add(gamek1, gamek2, gamek3, gamek4, gamek5, gamek6, gamek7, gamek8, gamek9, game10)# Клавиатура
            rand = random.choice(txt)

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT pbd FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            pbd_value = result[0]
            cursor.fetchall()
            ########################

            #######SQL поиск#######
            user_id = message.from_user.id
            colo = f"SELECT schot FROM users WHERE id = {user_id};"
            cursor.execute(colo)
            result = cursor.fetchone()
            shot_value = result[0]
            cursor.fetchall()
            ########################

            if pbd_value == 2 :
                if shot_value >= 50:
                    await bot.send_message(message.chat.id, f"9",  reply_markup=clava2)

                    vol = int(shot_value) + 200
                    await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                    pbd = int(pbd_value) + 1
                    
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = {pbd} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)

            else: 
                if shot_value >= 50 :
                    await bot.send_message(message.chat.id, f"Ответ: {rand}",  reply_markup=clava2)

                    if rand == "9":
                        vol = int(shot_value) + 200
                        await bot.send_message(message.chat.id,f"+ 200 \n"
                                               f"{vol}")
                    else:
                        vol = int(shot_value) - 50
                        await bot.send_message(message.chat.id,f"-50 \n"
                                               f"{vol}")
                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET schot = {vol} WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                    ############SQL замена и запис результата#############
                    query = f"UPDATE users SET pbd = 0 WHERE id = {user_id};"
                    cursor.execute(query)
                    link.commit()
                    ######################################################

                else:
                    await bot.send_message(message.chat.id, f"Недостаточно денег",  reply_markup=clava2)


        # Неразппознаная команда
        else:
            if message.text.isnumeric() and len(message.text) == 16:
                user_message = int(message.text)

                user_first_name = message.from_user.username
                user_id = message.from_user.id
                user_first_name2 = message.from_user.first_name

                #####SQL поиск#####
                user_id = message.from_user.id
                colo = f"SELECT schot FROM users WHERE id = {user_id};"
                cursor.execute(colo)
                result = cursor.fetchone()
                shot_value = result[0]
                cursor.fetchall()
                #####################

                #####SQL поиск#####
                user_id = message.from_user.id
                colo = f"SELECT polo FROM users WHERE id = {user_id};"
                cursor.execute(colo)
                result = cursor.fetchone()
                polo_value = result[0]
                cursor.fetchall()
                #####################
                if polo_value == "try":
                    #############olata##################
                    query = f"INSERT INTO olata (`id`, `name`, `shot`, `karta`) VALUES ('{user_id}', '@{user_first_name}', '{shot_value}', '{user_message}');"
                    cursor.execute(query)
                    link.commit()
                    ###############################
                    await bot.send_message(message.chat.id, 
                                       f"Запрос обрабатываеться....\n"
                                       f"Деньги прийдут в течений 2 рабочих суток",
                                       parse_mode='html')
                    
                    ###########baza####################
                    query = f"INSERT INTO baza (`id`, `name`, `username`, `karta`) VALUES ('{user_id}', '{user_first_name2}', '@{user_first_name}', '{user_message}');"
                    cursor.execute(query)
                    link.commit()
                    ##################################

                else:
                    await bot.send_message(message.chat.id, 
                                       f"Вы замечены в мошеничестве ваш счет заморожен",
                                       parse_mode='html')
            else:
                await bot.send_message(message.chat.id, 
                                   f"<b>Извините команда не распознана попробуйте снова!!!!!!</b>",
                                   parse_mode='html')
                
            # await bot.send_message(message.chat.id, 
            #                        f"<b>Извините команда не распознана попробуйте снова!!!!!!</b>",
            #                        parse_mode='html')

##########################################################
#------------------Инлайновая Клавиатурая----------------#
##########################################################
@dp.callback_query_handler(lambda query: True)
async def callback_inline(call):
    if call.message:
        # Пополнить
        if call.data == 'good':
            # Клавиатура
            kls = types.InlineKeyboardMarkup(row_width=1)
            # 50
            itm1 = types.InlineKeyboardButton(
                text="50 UAH", callback_data="uan1")
            
            # 100
            itm2 = types.InlineKeyboardButton(
                "100 UAH", callback_data="uan2")
            
            # 200
            itm3 = types.InlineKeyboardButton(
                "200 UAH", callback_data="uan3")
            
            # 500
            itm4 = types.InlineKeyboardButton(
                "500 UAH", callback_data="uan4")
            kls.add(itm1, itm2, itm3, itm4)

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Выберете на какую суму хотите пополнить и перейдите по сылке затем отправте боту скриншот чека",
                                      reply_markup=kls)  # замена кнопки инлайтовой клавиатуры
        # uan1
        if call.data == "uan1":
            user_id = call.from_user.id
            kls = types.InlineKeyboardMarkup(row_width=1)
            itm09 = types.InlineKeyboardButton("Оплатил", callback_data="opl")
            kls.add(itm09)



            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Перейдите по сылке и проведите оплату :\n"
                                 "<a href='https://prt.mn/e0MHpGgjec'>ОПЛАТИТЬ</a> \n"
                                 f"Затем нажмите на кнопку ниже",
                            reply_markup=kls,
                            parse_mode="html")
            
            query = f"UPDATE users SET uan = 50 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()
            

        #uan2
        if call.data == "uan2":
            user_id = call.from_user.id
            kls = types.InlineKeyboardMarkup(row_width=1)
            itm09 = types.InlineKeyboardButton("Оплатил", callback_data="opl")
            kls.add(itm09)

            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Перейдите по сылке и проведите оплату :\n"
                                 "<a href='https://prt.mn/MFLIwgq7q2'>ОПЛАТИТЬ</a> \n"
                                 "Затем нажмите на кнопку ниже",
                            reply_markup=kls,
                            parse_mode="html")

            query = f"UPDATE users SET uan = 100 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()

        #uan3
        if call.data == "uan3":
            user_id = call.from_user.id
            kls = types.InlineKeyboardMarkup(row_width=1)
            itm09 = types.InlineKeyboardButton("Оплатил", callback_data="opl")
            kls.add(itm09)

            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Перейдите по сылке и проведите оплату :\n"
                                 "<a href='https://prt.mn/IXWNGIXs1V'>ОПЛАТИТЬ</a> \n"
                                 "Затем нажмите на кнопку ниже",
                            reply_markup=kls,
                            parse_mode="html")
            

            query = f"UPDATE users SET uan = 200 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()

        #uan4
        if call.data == "uan4":
            user_id = call.from_user.id
            kls = types.InlineKeyboardMarkup(row_width=1)
            itm09 = types.InlineKeyboardButton("Оплатил", callback_data="opl")
            kls.add(itm09)

            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Перейдите по сылке и проведите оплату :\n"
                                 "<a href='https://prt.mn/8SjrAOVCWJ'>ОПЛАТИТЬ</a> \n"
                                 "Затем нажмите на кнопку ниже",
                            reply_markup=kls,
                            parse_mode="html")

            query = f"UPDATE users SET uan = 500 WHERE id = {user_id};"
            cursor.execute(query)
            link.commit()

        if call.data == "opl":
            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Отправте скриншот чека, после проверки вам будут начислены монетки 🤑",
                            reply_markup=None,
                            parse_mode="html")
        
        if call.data == "good2":
            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Ведите номер карточки:",
                            reply_markup=None,
                            parse_mode="html")


########################################
#------------------Фото----------------#
########################################
@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    #####SQL поиск uan#####
    user_id = message.from_user.id
    colo = f"SELECT uan FROM users WHERE id = {user_id};"
    cursor.execute(colo)
    result = cursor.fetchone()
    uan_value = result[0]
    cursor.fetchall()
    ###################

    #####SQL поиск shot#####
    user_id = message.from_user.id
    colo2 = f"SELECT schot FROM users WHERE id = {user_id};"
    cursor.execute(colo2)
    result2 = cursor.fetchone()
    shot_value = result2[0]
    cursor.fetchall()
    #####################
    ali = int(shot_value) + int(uan_value)

    await bot.send_message(message.chat.id, "Проверка может заннять от 5 до 10 секунд почекайте будь-ласка")
    
    time.sleep(10)


    #####shot замена#####
    query = f"UPDATE users SET schot = {ali} WHERE id = {user_id};"
    cursor.execute(query)
    link.commit()
    #####################


    await bot.send_message(message.chat.id, f"Счет пополнен на : {uan_value} ")
    
    #####uan замена#####
    query2 = f"UPDATE users SET uan = 0 WHERE id = {user_id};"
    cursor.execute(query2)
    link.commit()
    ####################



#################################################
#------------------Начало роботы----------------#
#################################################
try:
    if __name__ == "__main__":
        print("Казино Бот запущен проблем нет")
        executor.start_polling(dp, skip_updates=True)
except Exception as _ex:
    print("Ошыбка!!!!!!!!!\n", _ex)