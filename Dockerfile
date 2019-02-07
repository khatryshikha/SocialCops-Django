FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /SocialCops
WORKDIR /SocialCops
ADD . /SocialCops/
RUN pip install -r requirements.txt
