from machine import I2C, Pin
import ssd1306
import time

class OLED:
    def __init__(self, scl_pin=22, sda_pin=21):
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    def show_menu(self):
        self.oled.fill(0)
        self.oled.text("==== Door Lock ====", 0, 0)
        self.oled.text("# 新增卡片", 0, 20)
        self.oled.text("刷卡解鎖", 0, 40)
        self.oled.show()

    def show_message(self, msg, delay=2):
        self.oled.fill(0)
        self.oled.text(msg, 0, 20)
        self.oled.show()
        time.sleep(delay)
