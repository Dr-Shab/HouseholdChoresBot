FROM python:3.11

ENV SERVICE_NAME="serv-it"
RUN useradd --create-home $SERVICE_NAME
USER $SERVICE_NAME
RUN mkdir /home/$SERVICE_NAME/servierer

WORKDIR /home/$SERVICE_NAME/servierer

COPY src /home/$SERVICE_NAME/servierer


RUN pip install -r ./requirements.txt


CMD ["python3", "main_servierer.py"]