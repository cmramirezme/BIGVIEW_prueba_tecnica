FROM alpine:3.10

RUN apk add --no-cache python3 python3-dev py3-pip \
    && python3 -m ensurepip \
    && pip3 install --no-cache-dir --upgrade pip


WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3","src/app.py"]