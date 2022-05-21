# สำหรับ Admin

1. pull code ลงมา เฉพาะ Master
2. เข้าไป build Dockerfile ตั้งชื่อ `news-data-process`
   
   ```bash
    docker build . -t news-data-process
   ```
    
3. ตั้งค่า `.env` ใช้ตัวอย่างจาก `.env.example`

4. รันด้วย `docker-compose` 
   
    โดย docker-compose ออกแบบมาเป็น `batch` คือรันจบ จะปิดตัวลง
    
    ดังนั้นใช้ cron รัน ...
   - `docker-compose-6hr.yml` ทุก ๆ 6 ชั่วโมง
   
การตั้งรัน rss
   - rss.py   ทุกๆ 10 นาที
    ไฟล์ที่ออกมา rss_feed_news.json

   - news_front.py ทุกๆ 6:00 AM 