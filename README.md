# Instinctus Data pipeline

(주)인스팅터스의 매출 분석을 목적으로 한 데이터 파이프라인입니다.  
Cafe24, GA4, Instagram, Naver searchad에서 데이터를 가져오고, 고객의 RFM 모델을 분석합니다.

## Developments
python3, SQL

## How to run

### cafe24
Cafe24에서 고객 개인정보, 주문내역, 가입·탈퇴·휴면 내역, 상품정보, 쿠폰 이용내역 등의 데이터를 가져옵니다.  
Import data of customer information, orders, membership registration/cancellation/dormantness, products, coupons etc. from Cafe24.

    /cafe24/cafe24.py

### GA4, Instagram, Naver
GA4에서 [체레미 마카](https://cheremimaka.com/) 인터넷 쇼핑몰 방문자 수, 인스타그램에서 팔로워 수, 네이버 검색광고에서 키워드 검색량을 가져옵니다.  
Import shopping mall visit counts from GA4, followed counts from Instagram, keywords query counts from Naver searchad.  

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
