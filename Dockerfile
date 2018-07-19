FROM sixzeroo/ubuntu_python3:1.0
MAINTAINER sixzeroo60@gmail.com

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && mkdir /code

WORKDIR /code

ADD run.sh /run.sh

RUN chmod +x /run.sh

# Add crontab file in the cron directory
ADD crontabfile /etc/cron.d/work-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/work-cron

RUN crontab /etc/cron.d/work-cron

CMD cron && tail -f /requirements.txt