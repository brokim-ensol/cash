# 베이스 이미지
FROM python:3.10-slim

#작업 폴더 설정
WORKDIR /opt/myproject

# 소스코드 복사
COPY . /opt/myproject

# 파이썬 패키지 설정
RUN pip3 install -r requirements.txt

ENV FLASK_APP=pybo\
    FLASK_DEBUG=false\
    APP_CONFIG_FILE="/opt/myproject/pybo/config/production.py"

# 실행 파일 설정
CMD guicorn --bind 0.0.0.0:9000 "pybo:create_app()"