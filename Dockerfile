FROM python:3.10.1-alpine3.14
WORKDIR ./
RUN pip install discord.py


COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]