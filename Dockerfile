FROM python:3

COPY . /


RUN \
apt-get update -y && \
apt-get install -y python3-pip && \
apt-get install -y python3-dev && \
apt-get install -y libsecp256k1-dev && \
apt-get install -y python3-setuptools && \
apt-get install -y pkg-config && \
apt-get install -y build-essential && \
apt-get install -y automake && \
apt-get install -y libtool && \
apt-get install -y libffi-dev && \
apt-get install -y libgmp-dev && \
apt-get install -y libxslt-dev && \
apt-get install -y libxml2-dev && \
apt-get install -y python-dev && \
apt-get install -y libxslt1-dev && \
apt-get install -y libssl-dev && \
pip3 install --no-cache-dir requests && \
pip3 install --no-cache-dir behave && \
pip3 install --no-cache-dir python-binance-chain && \
pip3 install --no-cache-dir bit && \
pip3 install --no-cache-dir python-telegram-bot && \
pip3 install --no-cache-dir emoji && \
pip3 install --no-cache-dir websockets && \
pip3 install --no-cache-dir pyee && \
mkdir -p tmp && \
touch ./tmp/last_run.txt

CMD [ "python3","./telegram_bot.py" ]
