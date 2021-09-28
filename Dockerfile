FROM python:3

WORKDIR /home

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir Epidemicon
COPY . /home/Epidemicon
WORKDIR /home/Epidemicon
RUN chmod +x test.sh

CMD ["./test.sh"]
