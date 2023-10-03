# Instinctus Data pipeline

(주)인스팅터스의 매출 분석을 목적으로 한 데이터 파이프라인입니다.
Cafe24, GA, Naver searchad, Instagram에서 데이터를 가져오고, 고객의 RFM 모델을 분석합니다.

## Developments

python3, SQL

## How to run

### cafe24
Import data from cafe24

    /cafe24/cafe24.py

### GA, Naver, Instagram

GA에서 [인터넷 쇼핑몰](https://cheremimaka.com/) 방문자 수, 네이버 검색광고에서 키워드 검색량, 인스타그램에서 팔로워 수를 가져옵니다.

Import shopping mall visit counts from GA, followed count from Instagram, keyword query count from Naver searchad.

    /run/gin.py
    
### RFM analysis

1년 이내에 한 번이라도 주문한 적이 있는 고객들의 RFM 모델을 분석합니다.

Analyze RFM model of customers who placed an order at least once within a year.

    /rfm/runrfm.py

### Modules

send mail

    from log import mail
    mail.mail(subject="SUBJECT",body="BODY",From="YOUR EMAIL ADDRESS",To=["RECEIVER"S EMAIL ADDRESS"],CC=["CC'S EMAIL ADDRESS"],attachments=["ATTACHMENT"])

generate log no.

    from log import log
    log_no()
