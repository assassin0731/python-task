FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
	
COPY main.py users.csv .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
