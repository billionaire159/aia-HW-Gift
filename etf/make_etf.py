"""รวม etf_data.json เข้า template.html -> etf_dashboard.html (ไฟล์เดียว เปิดด้วยดับเบิลคลิก)"""
import os
H = os.path.dirname(os.path.abspath(__file__))
d = open(os.path.join(H, "etf_data.json"), encoding="utf-8").read()
t = open(os.path.join(H, "template.html"), encoding="utf-8").read()
open(os.path.join(H, "etf_dashboard.html"), "w", encoding="utf-8").write(t.replace("__DATA__", d))
print("etf_dashboard.html written")
