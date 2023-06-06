install:
	poetry install
	sudo docker build -t app .

start:
	sudo docker run -d -p 8000:8000 app
	
login:
	python3 request.py $(name) $(pass)
	
check_salary:
	python3 check_salary.py
