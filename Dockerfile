# Utiliza imagem oficial do Python
FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos da aplicação
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./

EXPOSE 5000

CMD ["python", "app.py"]
