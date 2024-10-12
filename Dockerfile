FROM python:3.12.7-alpine3.20
RUN apk add --no-cache tk
WORKDIR /project
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
CMD ["fastapi","run", "app/main.py", "--port", "80"]
