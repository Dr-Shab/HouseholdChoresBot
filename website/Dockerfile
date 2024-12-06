FROM python3.11.non-root

USER root

RUN apt-get update
RUN apt-get install -y nginx-extras

COPY ./happycastle /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/happycastle /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

# Adjust permissions
RUN chown -R ${APP_USER}:${APP_USER} /etc/nginx

# Switch back to non-root user
USER ${APP_USER}

COPY requirements.txt /app/requirements.txt
COPY app /app/

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ENV DB_API=http://dblogic:8001/api/save_checkin
ENV STATIC_PATH=/app/app/static
