FROM python:3.13

WORKDIR /chatbot

COPY ./requirements.txt /chatbot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /chatbot/requirements.txt

COPY ./app /chatbot/app

ENV GRADIO_SERVER_NAME="0.0.0.0"

EXPOSE 7860

CMD ["python", "app/main.py"]
