import logging
import traceback
import sys
import numpy as np
import pymysql
import time
import datetime
import orders
import privacy
import privacyaddinfo
import webhooklog
import products
import dailyanalysis2
import customergroup
import coupons
sys.path.append("/home/instinctus/Desktop/log")
import mail
import log

stlogger = logging.getLogger("stlog")
stlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(levelname)s %(asctime)s > %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logformatter)
stlogger.addHandler(stream_handler)

mylogger = logging.getLogger("mylog")
mylogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(filename)s,%(levelname)s,%(message)s,%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('log.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
mylogger.addHandler(file_handler)

errorlogger = logging.getLogger("errorlog")
errorlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(filename)s,%(message)s,%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('errorlog.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
errorlogger.addHandler(file_handler)

while True:
    try:
        time1 = datetime.datetime.now()
        stlogger.info('GET CAFE24 DATA\n')
        mylogger.info('%s,GET CAFE24 DATA' %(log.log_no()))
        
        conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
        cur = conn.cursor()
        sql = log.sqlquery(filename="log.csv",database="log",table="log",columns="`filename`,`loglevel`,`log_no`,`message`,`datetime`",linedivider="\\n",ignorelines="0")
        cur.execute(sql)
        conn.commit()
        conn.close()
        
        stlogger.info('GET ORDER DATA\n')
        orders.orders()
        
        stlogger.info('GET CUSTOMERS\' PRIVACY DATA\n')
        privacy.privacy()
        
        stlogger.info('GET COUPON DATA\n')
        coupons.coupon()
        
        stlogger.info('GET WEBHOOKS LOGS\n')
        webhooklog.webhooklog()
        
        stlogger.info('GET PRODUCT DATA\n')
        products.product()
    
        a = datetime.datetime.now().time()
        b = datetime.datetime.now().time().replace(hour=22,minute=0,second=0)
        c = datetime.datetime.now().time().replace(hour=23,minute=0,second=0)
        if b<a<c:
            stlogger.info('GET CUSTOMER GROUPS DATA\n')
            customergroup.customergroup()

            stlogger.info('GET CUSTOMERS\' ADDITIONAL INFOMATION DATA\n')
            privacyaddinfo.privacyaddinfo()
            
            stlogger.info('CUSTOMERS\' DATA ANAYLIZING\n')
            dailyanalysis2.analysis()
        
        stlogger.info('UPLOAD DATA TO MARIADB\n')
        mylogger.info('%s,UPLOAD DATA TO MARIADB' %(log.log_no()))

        conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
        cur = conn.cursor()
        sql = []
        sql += [log.sqlquery(filename="orders.csv",database="cafe24",table="orders",columns="`order_id`, `currency`, `market_id`, `member_id`, `member_email`, `billing_name`, `payment_method`, `order_date`, `first_order`, `payment_date`, `group_no_when_ordering`, `order_price_amount`, `shipping_fee`, `points_spent_amount`, `credits_spent_amount`, `coupon_discount_price`, `coupon_shipping_fee_amount`, `membership_discount_amount`, `shipping_fee_discount_amount`, `set_product_discount_amount`, `app_discount_amount`, `point_incentive_amount`, `total_amount_due`, `payment_amount`, `market_other_discount_amount`, `order_place_name`, `order_place_id`, `postpay`, `additional_shipping_fee`, `international_shipping_insurance`, `additional_handling_fee`, `shipping_type`, `shipping_type_text`, `shipping_status`")]
        sql += [log.sqlquery(filename="orderitems.csv",database="cafe24",table="orderitems",columns="`order_id`,`member_id`,`item_no`,`order_status`,`order_item_code`,`variant_code`,`product_code`,`custom_product_code`,`custom_variant_code`,`option_id`,`option_value`,`option_value_default`,`product_name`,`product_name_default`,`product_price`,`option_price`,`additional_discount_price`,`coupon_discount_price`,`item_payment_amount`,`quantity`,`product_tax_type`,`tax_rate`,`supplier_product_name`,`supplier_id`,`supplier_name`,`tracking_no`,`shipping_code`,`shipping_company_id`,`shipping_company_name`,`shipping_company_code`,`product_bundle`,`product_bundle_name`,`naver_pay_order_id`,`ordered_date`,`shipped_date`,`delivered_date`")]
        sql += [log.sqlquery(filename="orderbr.csv",database="cafe24",table="orderbuyerreceiver",columns="`shop_no`,`name`,`name_furigana`,`phone`,`cellphone`,`virtual_phone_no`,`zipcode`,`address1`,`address2`,`address_state`,`address_city`,`address_street`,`address_full`,`name_en`,`city_en`,`state_en`,`street_en`,`country_code`,`country_name`,`country_name_en`,`shipping_message`,`clearance_information_type`,`clearance_information`,`wished_delivery_date`,`wished_delivery_time`,`shipping_code`,`order_id`, `member_id`,`member_group_no`,`names_furigana`,`email`,`customer_notification`,`updated_date`,`user_id`,`user_name`")]
        sql += [log.sqlquery(filename="customers.csv",database="cafe24",table="customers",columns="`shop_no`, `member_id`, `name`, `name_english`, `name_phonetic`, `phone`, `cellphone`, `email`, `sms`, `news_mail`, `thirdparty_agree`, `wedding_anniversary`, `birthday`, `solar_calendar`, `total_points`, `available_points`, `used_points`, `city`, `state`, `address1`, `address2`, `group_no`, `job_class`, `job`, `zipcode`, `created_date`, `member_authentication`, `use_blacklist`, `blacklist_type`, `last_login_date`, `member_authority`, `nick_name`, `recommend_id`, `residence`, `interest`, `gender`, `member_type`, `company_type`, `foreigner_type`,`personal_type`, `lifetime_member`, `corporate_name`, `nationality`, `shop_name`, `country_code`, `use_mobile_app`, `join_path`, `fixed_group`, `refund_bank_code`, `refund_bank_account_no`, `refund_bank_account_holder`, `company_condition`, `company_line`, `sns_list`")]
        sql += [log.sqlquery(filename="customergroups.csv",database="cafe24",table="customergroups",columns="`shop_no`,`group_no`,`group_name`,`group_description`,`group_icon`,`benefits_paymethod`,`buy_benefits`,`ship_benefits`,`product_availability`,`mileage`,`discount`")]
        sql += [log.sqlquery(filename="coupons.csv",database="cafe24",table="coupons",columns="`shop_no`,`coupon_no`,`coupon_type`,`coupon_name`,`coupon_description`,`created_date`,`deleted`,`is_stopped_issued_coupon`,`pause_begin_datetime`,`pause_end_datetime`,`benefit_text`,`benefit_type`,`benefit_price`,`benefit_percentage`,`benefit_percentage_round_unit`,`benefit_percentage_max_price`,`include_regional_shipping_rate`,`include_foreign_delivery`,`coupon_direct_url`,`issue_type`,`issue_sub_type`,`issue_member_join`,`issue_member_join_recommend`,`issue_member_join_type`,`issue_order_amount_type`,`issue_order_start_date`,`issue_order_end_date`,`issue_order_amount_limit`,`issue_order_amount_min`,`issue_order_amount_max`,`issue_order_path`,`issue_order_type`,`issue_order_available_product`,`issue_order_available_category`,`issue_anniversary_type`,`issue_anniversary_pre_issue_day`,`issue_module_type`,`issue_review_count`,`issue_review_has_image`,`issue_quantity_min`,`issue_quntity_type`,`issue_max_count`,`issue_max_count_by_user`,`issue_count_per_once`,`issued_count`,`issue_member_group_no`,`issue_member_group_name`,`issue_no_purchase_period`,`issue_reserved`,`issue_reserved_date`,`available_date`,`available_period_type`,`available_begin_datetime`,`available_end_datetime`,`available_site`,`available_scope`,`available_day_from_issued`,`available_price_type`,`available_order_price_type`,`available_min_price`,`available_amount_type`,`available_payment_method`,`available_product`,`available_product_list`,`available_category`,`available_category_list`,`available_coupon_count_by_order`,`serial_generate_method`,`coupon_image_type`,`coupon_image_path`,`show_product_detail`,`use_notification_when_login`,`send_sms_for_issue`,`send_email_for_issue`")]
        sql += [log.sqlquery(filename="couponissues.csv",database="cafe24",table="couponissues",columns="`shop_no`,`coupon_no`,`issue_no`,`member_id`,`group_no`,`issued_date`,`expiration_date`,`used_coupon`,`used_date`,`related_order_id`")]
        sql += [log.sqlquery(filename="webhooklogs.csv",database="cafe24",table="resigneddormant",columns="`log_id`,`log_type`,`event_no`,`event_name`,`mall_id`,`trace_id`,`requested_time`,`request_endpoint`,`event_shop_no`,`member_id`,`success`,`response_http_code`,`response_body`")]
        sql += [log.sqlquery(filename="customersaddinfo.csv",database="cafe24",table="customersaddinfo",columns="`member_id`,`biological_sex`,`sexual orientation`")]
        sql += [log.sqlquery(filename="products.csv",database="cafe24",table="products",columns="`shop_no`,`product_no`,`product_code`,`custom_product_code`,`product_name`,`eng_product_name`,`supply_product_name`,`internal_product_name`,`model_name`,`price_excluding_tax`,`price`,`retail_price`,`supply_price`,`display`,`selling`,`summary_description`,`adult_certification`,`made_in_code`,`product_weight`,`product_material`,`created_date`,`updated_date`,`sold_out`,`additional_price`,`shipping_fee_by_product`,`shipping_fee_type`")]
        sql += [log.sqlquery(filename="dailyanalysis.csv",database="cafe24",table="dailyanalysis",columns="`date`,`signins`,`totals`")]
        for s in sql:
            cur.execute(s)
        conn.commit()
        conn.close()
        mylogger.info('%s,A LOOP FINISHED' %(log.log_no()))
        
    except Exception as e:
        errorlogno = log.log_no()
        mylogger.error('%s,"%s"' %(errorlogno,e))
        stlogger.info('*** AN ERROR OCCURED ***')
        errorlogger.error('%s,"%s","%s"' %(errorlogno, str(e), traceback.format_exc().replace('"',"'")))
        mail.mail(subject="Cafe24 Data Pipeline Error: %s" %(str(e)),body=traceback.format_exc().replace('"',"'"),To=["geonho.lim@cheremimaka.com"])
        
    finally:
        conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
        cur = conn.cursor()
        sql = []
        sql += [log.sqlquery(filename="log.csv",database="log",table="log",columns="`filename`,`loglevel`,`log_no`,`message`,`datetime`",linedivider="\\n",ignorelines="0")]
        sql += [log.sqlquery(filename="errorlog.csv",database="log",table="errorlog",columns="`filename`,`log_no`,`errorname`,`tracebackmsg`,`datetime`",linedivider="\\n",ignorelines="0")]
        for s in sql:
            cur.execute(s)
        conn.commit()
        conn.close()
        
        time2 = datetime.datetime.now()
        stlogger.info("A LOOP FINISHED AT %s" %(time2.strftime('%Y-%m-%d %H:%M:%S')))
        stlogger.info('%s elapsed' %(time2 - time1))
        stlogger.info('*** SLEEPING ***\n')
        time.sleep(60)