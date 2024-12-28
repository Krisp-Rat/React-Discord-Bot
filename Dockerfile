FROM python:3.8

ENV HOME /root
WORKDIR /root

RUN apt-get update && apt-get install -y ffmpeg

ENV PATH /usr/local/bin:$PATH

COPY . .

# Download dependancies
RUN pip3 install -r requirements.txt

CMD python3 -u bot.py