FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces要求：非root用户(UID 1000)运行
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

# HF Spaces固定使用7860端口
EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "app:app"]