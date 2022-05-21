# สำหรับ Admin

1. pull code ลงมา เฉพาะ Master
2. เข้าไป build Dockerfile ตั้งชื่อ `twitter-data-process`
   
   ```bash
    docker build . -t twitter-data-process
   ```
    
3. ตั้งค่า `.env` ใช้ตัวอย่างจาก `.env.example`

4. รันด้วย `docker-compose` 
   
    โดย docker-compose ออกแบบมาเป็น `batch` คือรันจบ จะปิดตัวลง
    
    ดังนั้นใช้ cron รัน ...
   - `docker-compose-5min.yml` ทุก ๆ 5 นาที
   - `docker-compose-0200am.yml` ทุก ๆ เวลาตี 2