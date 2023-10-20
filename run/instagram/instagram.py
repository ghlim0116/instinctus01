import pymysql
import time
import datetime
import sys
sys.path.append('/home/instinctus/Desktop/run/instagram')
import followedcount
    
def instagram():
    followedcount.followedcount()

    sql = []

    # followedcount
    sql += ["""
    LOAD DATA LOW_PRIORITY LOCAL INFILE '/home/instinctus/Desktop/run/instagram/followedcount.csv'
    REPLACE INTO TABLE `instagram`.`followedcount`
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    ESCAPED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (`id`,`follow_count`,`followed_by_count`,`has_profile_picture`,`is_private`,`is_published`,`media_count`,`profile_pic`,`username`,`ig_account_id`,`datetime`);
    """]

    conn = pymysql.connect(host = '***.***.***.***',port=********,database='********',charset='utf8mb4',local_infile=1, user='********',password='********')
    cur = conn.cursor()
    for cmd in sql:
        cur.execute(cmd)
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    instagram()
