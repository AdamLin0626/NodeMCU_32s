import network
import time
from machine import Pin, SoftI2C
import ssd1306
from umqtt.simple import MQTTClient

# ======== Wi-Fi 設定 ========
SSID = "AdamPC"
PASSWORD = b"12345678"

# ======== MQTT 設定 ========
MQTT_BROKER = "broker.MQTTGO.io"
MQTT_CLIENT_ID = "MQTTGO-9462226233"
MQTT_TOPIC = "test/oled"

# ======== OLED 初始化（使用 SSD1306）========
i2c = SoftI2C(scl=Pin(19), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ======== 連線 Wi-Fi ========
def connect_wifi():
    oled.fill(0)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(1)  # 確保模組初始化完成
    if not wlan.isconnected():
        oled.text("Connecting WiFi..." ,0 ,30)
        oled.show()
        wlan.connect(SSID, PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        oled.fill(0)
        oled.text("Wifi Connecting",0 ,30)
        oled.show()
    else:
        raise RuntimeError("WiFi Disconnect")

# ======== 接收到 MQTT 訊息時處理 ========
def on_mqtt_message(topic, msg):
    oled.fill(0)
    oled.text("MQTT Received:", 0, 0)
    oled.text(msg.decode(), 0, 10)
    oled.show()

# ======== 開機 ========
def start_successful():
    oled.fill(0)
    oled.text("Welcome~",30 ,30     )
    oled.show()

# ======== 主程式 ========
def main():
    start_successful()
    time.sleep(0.5)
    connect_wifi()
    time.sleep(0.5)
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.set_callback(on_mqtt_message)
    client.connect()
    oled.fill(0)
    oled.text("MQTT Already" ,0 ,30)
    oled.show()
    client.subscribe(MQTT_TOPIC)
    oled.fill(0)

    while True:
        client.check_msg()
        time.sleep(0.1)

main()
