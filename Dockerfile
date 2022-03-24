FROM python:3.10.1-alpine3.14
WORKDIR ./
RUN pip install discord.py
RUN pip install twitchAPI


COPY . .

CMD [ "python3","-u", "main.py"]