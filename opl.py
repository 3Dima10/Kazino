from aiogram import Dispatcher, Bot, executor, types
import logging
import mysql.connector
from config import user, password, host, database, admin



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
bot = Bot(token=admin)
dp = Dispatcher(bot=bot)


#########################################
#------------------Start----------------#
#########################################

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    clsr = types.ReplyKeyboardMarkup(input_field_placeholder="Просмотрим чеки етих ничтожыств", resize_keyboard=True)
    itm = types.KeyboardButton("Чек🧾")
    clsr.add(itm)
    name_id = message.from_user.first_name
    await bot.send_message(message.chat.id, f"Добро пожаловать мистер : {name_id}", reply_markup=clsr)

###########################################
#----------------Text---------------------#
###########################################

@dp.message_handler(content_types=['text'])
async def text(message):
    if message.text == "Чек🧾":
        try:
            #####SQL поиск#####

            colo = f"SELECT id FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            id_value = result[0]
            cursor.fetchall()
            #####################

            #####SQL поиск#####

            colo = f"SELECT name FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            name = result[0]
            cursor.fetchall()
            #####################

            #####SQL поиск#####

            colo = f"SELECT shot FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            username = result[0]
            cursor.fetchall()
            #####################

            #####SQL поиск#####

            colo = f"SELECT karta FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            karta = result[0]
            cursor.fetchall()
            ##################### 

            clsr = types.ReplyKeyboardMarkup(input_field_placeholder="Просмотрим чеки етих ничтожыств")
            itm = types.KeyboardButton("Чек🧾")
            clsr.add(itm)

            inl = types.InlineKeyboardMarkup(row_width=1)
            inl1 = types.InlineKeyboardButton("Принял🟢", callback_data="tru")
            inl2 = types.InlineKeyboardButton("Отказал🟥", callback_data="folse")
            inl.add(inl1,inl2)

            await bot.send_message(message.chat.id,
                                    f"Чек🧾\n"
                                    f"id:{id_value}\n"
                                    f"Имя:{name}\n"
                                    f"Счёт:{username}\n"
                                    f"Карта:{karta}\n",
                                    reply_markup=inl)
        except:
            await bot.send_message(message.chat.id,"Не кто не найден")

@dp.callback_query_handler(lambda query: True)
async def callback_inline(call):
    if call.message:
        if call.data == "tru":
            #####SQL поиск#####

            colo = f"SELECT id FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            id_value = result[0]
            cursor.fetchall()
            #####################

            #  "DELETE FROM olata WHERE `olata`.`id` = 5752970077"
            query = f"DELETE FROM olata WHERE `olata`.`id` = {id_value} ;"
            cursor.execute(query)
            link.commit()

            query = f"UPDATE users SET schot = 0 WHERE id = {id_value};"
            cursor.execute(query)
            link.commit()

            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Оплата подтверждена 😭",
                            reply_markup=None,
                            parse_mode="html")

        if call.data == "folse":
            #####SQL поиск#####

            colo = f"SELECT id FROM olata LIMIT 1;"
            cursor.execute(colo)
            result = cursor.fetchone()
            id_value = result[0]
            cursor.fetchall()
            #####################

            query = f"UPDATE users SET polo = 'folse' WHERE id = {id_value};"
            cursor.execute(query)
            link.commit()
            
            query = f"DELETE FROM olata WHERE `olata`.`id` = {id_value} ;"
            cursor.execute(query)
            link.commit()

            query = f"UPDATE users SET schot = 0 WHERE id = {id_value};"
            cursor.execute(query)
            link.commit()

            await bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="Мамонт заблокирован 😂😂😂😂",
                            reply_markup=None,
                            parse_mode="html")


#################################################
#------------------Начало роботы----------------#
#################################################
try:
    if __name__ == "__main__":
        print("Казино Бот запущен проблем нет")
        executor.start_polling(dp, skip_updates=True)
except Exception as _ex:
    print("Ошыбка!!!!!!!!!\n", _ex)