FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./code/api /app

COPY ./code/features/features.py /app/features/features.py
COPY ./code/util/db.py /app/util/db.py

COPY ./output/model/model.pkl /app/model/model.pkl
COPY ./database/database.db /app/database/database.db

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
