FROM debian:buster-slim

# atualiza o cache do apt-get e instala os pacotes necessários
RUN apt-get update && \
    apt-get install -y python3 python3-pip default-libmysqlclient-dev python-numpy libicu-dev python3-tk && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install mysqlclient

# seta o diretório de trabalho como /app
WORKDIR /app

# copia o arquivo requirements.txt para o diretório /app
COPY requirements.txt /app/
COPY .env /app/

# instala as dependências do projeto
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# copia o restante dos arquivos para o diretório /app
COPY . /app/