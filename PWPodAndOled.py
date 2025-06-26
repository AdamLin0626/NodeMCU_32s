from machine import Pin
import time
from machine import Pin, SoftI2C
import ssd1306

# ======== OLED 初始化（使用 SSD1306）========
i2c = SoftI2C(scl=Pin(19), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 定義行（Row）腳位
row_pins = [Pin(33, Pin.OUT), Pin(25, Pin.OUT), Pin(26, Pin.OUT), Pin(27, Pin.OUT)]
# 定義列（Column）腳位
col_pins = [Pin(14, Pin.IN, Pin.PULL_UP), Pin(12, Pin.IN, Pin.PULL_UP), Pin(13, Pin.IN, Pin.PULL_UP)]

# 對應鍵值表
keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# 預設密碼
password = "1234"
input_password = ""

# ======== 開機 ========
def start_successful():
    oled.fill(0)
    oled.text("Welcome~",33 ,30)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.text("Please Enter",15 ,15)
    oled.text("the",53 ,30)
    oled.text("Password!",28 ,45)
    oled.show()
    
    
def scan_keypad():
    global input_password
    for i, row in enumerate(row_pins):
        # 所有行設高電位
        for r in row_pins:
            r.value(1)
        # 當前行拉低
        row.value(0)
        # 掃描所有列
        for j, col in enumerate(col_pins):
            if col.value() == 0:  # 按下
                key = keys[i][j]
                if key in '0123456789':  # 只記錄數字
                    input_password += key
                    oled.fill(0)
                    oled.text("Password:",28 ,5)
                    oled.text(input_password,5 ,30)
                    oled.show()
                if key == '#':  # 按下 # 當作確認
                    if input_password == password:
                        print("Unclock")
                        oled.fill(0)
                        oled.text("Unlock!",35 ,28)
                        oled.show()
                    else:
                        print("Password Incurred!")
                        oled.fill(0)
                        oled.text("Password",33 ,20)
                        oled.text("Incurred!",30 ,40)
                        oled.show()
                        input_password = ""  # 重置
                if key == '*':  # 按下 * 清除輸入
                    input_password = ""
                    print("Please Enter the Password")
                    oled.fill(0)
                    oled.text("Clear!",43 ,35)
                    oled.show()
                    time.sleep(1.5)
                    oled.fill(0)
                    oled.text("Please Enter",15 ,15)
                    oled.text("the",53 ,30)
                    oled.text("Password!",28 ,45)
                    oled.show()
                time.sleep(0.3)  # 防抖


start_successful()
while True:
    scan_keypad()
    time.sleep(0.05)
