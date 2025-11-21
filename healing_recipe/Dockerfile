FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# PYTHONPATH 설정 (app 모듈 인식 문제 해결)
ENV PYTHONPATH="/app"

# run.sh에 실행 권한 추가
RUN chmod +x run.sh

CMD ["./run.sh"]
