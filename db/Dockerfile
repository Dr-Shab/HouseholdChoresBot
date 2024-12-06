FROM python:3.11

ENV SERVICE_NAME="db-it"
RUN useradd --create-home $SERVICE_NAME
USER $SERVICE_NAME
RUN mkdir /home/$SERVICE_NAME/databae

WORKDIR /home/$SERVICE_NAME/databae

COPY src /home/$SERVICE_NAME/databae

RUN pip install -r ./requirements.txt

CMD ["python3", "main_db.py"]