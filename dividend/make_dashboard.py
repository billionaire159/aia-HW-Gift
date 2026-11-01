"""ฝัง metrics.json ลงใน template.html -> dividend-dashboard/dashboard.html (ไฟล์เดียว เปิดด้วยดับเบิลคลิกได้)
ใช้: python dividend-dashboard/make_dashboard.py   (รันหลัง build.py)
หน้าเว็บไม่คำนวณใหม่ แสดงตาม metrics.json เท่านั้น
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
data = open(os.path.join(HERE, "metrics.json"), encoding="utf-8").read()
json.loads(data)  # ตรวจว่าเป็น JSON ที่ถูกต้อง
safe = data.replace("</", "<\\/")  # กัน </script> ปิดแท็กก่อนเวลา
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
assert "/*__DATA__*/" in tpl
out = tpl.replace("/*__DATA__*/", safe)
open(os.path.join(HERE, "dashboard.html"), "w", encoding="utf-8").write(out)
print("dashboard.html: %.2f MB" % (len(out.encode("utf-8")) / 1e6))
