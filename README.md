# Instinctus Data pipeline

## How to run
***

### cafe24
Import data from cafe24

    /cafe24/cafe24.py

### GA, Instagram, Naver
Import homepage visit counts from GA, followed count from Instagram, keyword query count from Naver searchad.

    /run/gin.py
    
### RFM analysis
Get RFM model of customers who placed an order at least once within a year.

    /rfm/runrfm.py
***

## Modules
***
send mail

    from log import mail
    mail.mail(subject="",body="",From="SOPmanagement@cheremimaka.com",To=[],CC=[],attachments=[])
fasdf

    /log/mail.py






from log import log
generate log no.
log_no()
