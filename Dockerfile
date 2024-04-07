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
    APP_CONFIG_FILE="/opt/myproject/config/production.py"

# get_rev_db.py를 실행하고 shell에 출력된 결과가 0이 아닐때 revision_num 환경변수로 선언
RUN revision_num="$(python get_rev_db.py)"; \
    if [ "$revision_num" != "0" ]; then \
        echo "$revision_num"; \
        export revision_num="$revision_num"; \
    fi

# 만약에 pybo.db 파일이 존재하면 flask db downgrade 명령어를 실행
RUN if [ -f pybo.db ]; then \
        echo ${revision_num}; \
        flask db revision --rev-id "${revision_num}"; \
    else \
        flask db init; \
    fi

RUN flask db migrate
RUN flask db upgrade

# 실행 파일 설정
CMD gunicorn --bind 0.0.0.0:9000 "pybo:create_app()"