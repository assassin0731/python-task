import pgdb

pg_db = pgdb.Connection(user='kerenhor', password='assassin073', database='user_names', host='localhost', port=5432)

my_dict = {}

sql_query = 'SELECT * FROM user_names;'
cursor = pg_db.cursor()

cursor.execute(sql_query)

for row in cursor.fetchall():
    inner_dict = {"password": row[1],
                  "salary": row[2],
                  "next_promotion_date": row[3]}
    my_dict[row[0]] = inner_dict

print(my_dict)

pg_db.close()