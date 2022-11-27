FROM python:latest

WORKDIR /app

ADD . /app

RUN python -m pip install -r requirememts.txt

RUN rm requirememts.txt

CMD ["python", "bot.py"]



