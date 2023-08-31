# import mysql.connector

# config = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'database': 'lop',
#     'raise_on_warnings': True,
# }

# link = mysql.connector.connect(**config)

# cursor = link.cursor()

# query = "INSERT INTO user (`№`, `id`, `schot`) VALUES ('3', '11111', '2222');"
# cursor.execute(query)
# link.commit()

# cursor.close()
# link.close()






# import mysql.connector

# config = {
#   'user': 'root',
#   'password': 'root',
#   'host': 'localhost',
#   'database': 'lop',
#   'raise_on_warnings': True,
# }

# link = mysql.connector.connect(**config)

# cursor = link.cursor()

# query = "CREATE TABLE users (id INT PRIMARY KEY, username VARCHAR(50), email VARCHAR(100), age INT );"
# cursor.execute(query)
# cursor.close()
# link.close()


    # #####uan замена#####
    # query2 = f"UPDATE users SET uan = 0 WHERE id = {user_id};"
    # cursor.execute(query2)
    # link.commit()
    # ##################