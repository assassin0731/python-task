import csv

with open('users.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
employees = {}
for row in data:
    inner_dict = {"password": row[1],
                  "salary": row[2],
                  "next_promotion_date": row[3]}
    employees[row[0]] = inner_dict

print(employees)