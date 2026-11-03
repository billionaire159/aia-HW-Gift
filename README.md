# การบ้าน AI Investor Alpha · Day 1 → Day 2

| | |
|---|---|
| **ชื่อเล่น** | Gift |
| **โจทย์ 1 บรรทัด** | ใช้ AI ช่วยดูสัญญาณ Buy/Sell ของ ETF ต่างประเทศด้วย EMA 12/26 ใน 3 กรอบเวลา (วัน/สัปดาห์/เดือน) |
| **สถานะ** | ร่างแรก |

## ดูผลงาน (กดได้เลย)

- **Dashboard ETF (เปิดดูหน้าจริง):** https://htmlpreview.github.io/?https://github.com/billionaire159/aia-HW-Gift/blob/main/etf/etf_dashboard.html
- ไฟล์ dashboard บน GitHub (เป็นโค้ด): [etf/etf_dashboard.html](etf/etf_dashboard.html)
- บันทึกขั้นตอนทำงาน: [prompts.md](prompts.md)
- ปัญหาที่เจอและบทเรียน: [PROJECT_MEMORY.md](PROJECT_MEMORY.md)

## ทำอะไรไว้

1. **ETF ต่างประเทศ 12 ตัว** (SPY, QQQ, VTI, VOO, VEA, VWO, IWM, GLD, TLT, SCHD, VNQ, XLK) ที่มา Yahoo Finance
   - EMA 12 อยู่เหนือ 26 (ตัดขึ้น) = **Buy** · อยู่ใต้ 26 (ตัดลง) = **Sell**
   - แสดง RSI(14) และ Stochastic(14,3,3) ไว้ประกอบ ไม่นับในสัญญาณ
2. **หุ้นปันผล** โค้ดอยู่ที่ [dividend/](dividend/) ไม่ได้นำตัวเลขขึ้น repo เพราะคำนวณจากข้อมูล SETSMART ที่ซื้อมา

เพื่อการศึกษา ไม่ใช่คำแนะนำลงทุน
