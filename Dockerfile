# Usar Python oficial
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Criar diretório da aplicação
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o restante do código
COPY . /app/

# Executar migrações e coletar estáticos (boa prática para produção)
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expor a porta
EXPOSE 8000

# Comando para iniciar o Gunicorn com seu wsgi.py
CMD ["gunicorn", "Athena.wsgi:application", "--bind", "0.0.0.0:8000"]
