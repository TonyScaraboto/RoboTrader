# Usar Python 3.12 slim
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copiar código do aplicativo
COPY . .

# Criar diretório de dados
RUN mkdir -p data

# Expor porta
EXPOSE 5000

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV HOST=0.0.0.0

# Comando para iniciar o app
CMD gunicorn run:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
