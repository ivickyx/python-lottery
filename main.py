import random
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

#  0. COLORS CONFIG (จัดการสีข้อความ)

class Color:
    """ANSI Escape Codes สำหรับเปลี่ยนสีตัวอักษรใน Terminal"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


#  1. DATA MODEL  (กำหนดค่าแต่ละประเภทหวย)

@dataclass(frozen=True)
class LotteryConfig:
    """โครงสร้างข้อมูลสำหรับตั้งค่าหวยแต่ละประเภท"""
    label: str      # ชื่อที่แสดงใน menu
    digits: int     # จำนวนหลัก
    name: str       # ชื่อเต็ม

LOTTERY_TYPES: List[LotteryConfig] = [
    LotteryConfig(label="2 หลัก", digits=2, name="หวยสองตัว"),
    LotteryConfig(label="3 หลัก", digits=3, name="หวยสามตัว"),
    LotteryConfig(label="6 หลัก", digits=6, name="หวยรัฐบาล"),
]

#  2. ENGINE  (ตรรกะการสุ่ม)

class LotteryEngine:
    @staticmethod
    def draw(digits: int) -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(digits))


# ──────────────────────────────────────────────
#  3. PRINTER  (จัดการ UI ด้วยสีและอีโมจิ)
# ──────────────────────────────────────────────

class ResultPrinter:
    """จัดการแสดงผลทั้งหมด (รูปแบบใหม่ ไม่มีกล่อง เน้นความสวยงาม)"""

    @classmethod
    def header(cls) -> None:
        os.system("cls" if os.name == "nt" else "clear")

        # os.system("") เพื่อบังคับให้ Windows 10+ แสดงผล ANSI Color ได้
        if os.name == "nt":
            os.system("")

        print(f"\n{Color.CYAN}{Color.BOLD}✨ {'='*37} ✨{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}        🎰 ระบบสุ่มเลขหวยออนไลน์ 🎰{Color.RESET}")
        print(f"{Color.MAGENTA}       📚 Create b 📚{Color.RESET}")
        print(f"{Color.CYAN}{Color.BOLD}✨ {'='*37} ✨{Color.RESET}\n")

    @classmethod
    def menu(cls, configs: List[LotteryConfig]) -> None:
        for i, cfg in enumerate(configs, 1):
            print(f"  {Color.YELLOW}🎫 [{i}]{Color.RESET} สุ่มหวย {cfg.label} {Color.CYAN}({cfg.name}){Color.RESET}")
        print(f"\n  {Color.RED}❌ [0]{Color.RESET} ออกจากโปรแกรม\n")

    @classmethod
    def result(cls, number: str, cfg: LotteryConfig) -> None:
        """แสดงผลลัพธ์แบบ highlight และสีสัน"""
        spaced = "  ".join(number)
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n{Color.YELLOW}{Color.BOLD}🎉 {'='*37} 🎉{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}            🏆 ผล{cfg.name} 🏆{Color.RESET}\n")
        print(f"{Color.CYAN}{Color.BOLD}               ▶️  {Color.MAGENTA}{spaced}{Color.CYAN}  ◀️{Color.RESET}\n")
        print(f"{Color.YELLOW}            🕒 เวลา: {timestamp}{Color.RESET}")
        print(f"{Color.YELLOW}{Color.BOLD}🎉 {'='*37} 🎉{Color.RESET}\n")

    @classmethod
    def error(cls, msg: str) -> None:
        print(f"\n  {Color.RED}⚠️  ข้อผิดพลาด: {msg}{Color.RESET}\n")


# ──────────────────────────────────────────────
#  4. MAIN
# ──────────────────────────────────────────────

def main() -> None:
    printer = ResultPrinter()
    engine  = LotteryEngine()

    while True:
        printer.header()
        printer.menu(LOTTERY_TYPES)

        # ใช้สีเพื่อทำให้ Prompt ดึงดูดสายตาขึ้น
        choice = input(f"  {Color.GREEN}👉 เลือกรายการ (0-{len(LOTTERY_TYPES)}): {Color.RESET}").strip()

        if choice == "0":
            print(f"\n  {Color.CYAN}👋 ขอบคุณที่ใช้บริการ ขอให้โชคดีครับ! ✨{Color.RESET}\n")
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(LOTTERY_TYPES)):
            printer.error(f"กรุณากรอกตัวเลข 1–{len(LOTTERY_TYPES)} หรือ 0 เพื่อออก")
            input(f"  {Color.YELLOW}กด Enter เพื่อลองใหม่...{Color.RESET}")
            continue

        cfg    = LOTTERY_TYPES[int(choice) - 1]
        number = engine.draw(cfg.digits)

        printer.header()
        printer.result(number, cfg)
        input(f"  {Color.YELLOW}กด Enter เพื่อสุ่มอีกครั้ง...{Color.RESET}")

if __name__ == "__main__":
    main()