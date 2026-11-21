# ใช้กับ GitHub Profile 13D4C

คัดลอก `README.md` และโฟลเดอร์ `assets/profile` ไปไว้ใน repository `13D4C/13D4C` แล้ว commit และ push ตามปกติ

- แบนเนอร์และส่วนท้ายเป็น GIF แบบวนลูป มีเวอร์ชันสำหรับมือถือ
- เมื่อระบบตั้งค่าลดการเคลื่อนไหว README จะใช้ภาพ PNG แทน GIF
- เนื้อหาครบในเวอร์ชันข้อความที่กดขยายอ่านได้
- ภาพมาสคอตต้นฉบับอยู่ที่ `assets/profile/gopher-duck.png`

## แก้ข้อมูลและสร้างภาพใหม่

แก้ข้อมูลใน `profile.json` และโลโก้ Tech Stack ใน `tech-stack.json` แล้วใช้ Python ที่ติดตั้ง Pillow:

```sh
python -m pip install -r requirements.txt
python scripts/build_profile.py
```

สคริปต์ค้นหาฟอนต์ DejaVu บน Linux หรือ Arial/Georgia/Consolas บน Windows โดยอัตโนมัติ หากใช้ฟอนต์อื่น ตั้งค่า `PROFILE_FONT_DIR` ให้ชี้ไปที่โฟลเดอร์ที่มี DejaVuSans.ttf, DejaVuSans-Bold.ttf, DejaVuSerif.ttf และ DejaVuSansMono.ttf

Go Gopher สร้างสรรค์โดย [Renée French](https://go.dev/blog/gopher) ภายใต้ [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ภาพมาสคอตคู่นี้เป็นภาพดัดแปลงที่สร้างด้วย AI ร่วมกับเป็ด
