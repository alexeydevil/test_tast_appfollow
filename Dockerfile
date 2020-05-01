FROM python:3.7.6


RUN apt-get update && \
    apt-get -y -q install --no-install-recommends \
             build-essential \
             vim \
             tzdata && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV TZ Europe/Moscow
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata


RUN pip install --upgrade pip

WORKDIR /tmp
COPY requirements.txt /tmp/
RUN pip install -r requirements.txt && rm -rf /tmp/*

WORKDIR /opt/appfollow
COPY service/__init__.py /opt/appfollow/
COPY service/background_task.py /opt/appfollow/
COPY service/const.py /opt/appfollow/
COPY service/scheduler.py /opt/appfollow/
COPY service/service.py /opt/appfollow/
COPY service/task.py /opt/appfollow/
COPY service/tests/__init__.py /opt/appfollow/tests/
COPY service/tests/test_service.py /opt/appfollow/tests/

EXPOSE 8000

ENTRYPOINT ["python", "-u", "/opt/appfollow/service.py"]