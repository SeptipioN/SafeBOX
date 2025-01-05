from machine import Pin, ADC, PWM, I2C
import time
import machine
import ssd1306
from mfrc522_i2c import mfrc522

#Підключення Oled SSD1306
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#Підключення Сервопривіду
servoPin = Pin(15)
pwm = PWM(servoPin, freq=50)

#Підключення MFRC522 RFID
addr = 0x28
scl = 4
sda = 2
rc522 = mfrc522(scl, sda, addr)
rc522.PCD_Init()
rc522.ShowReaderDetails()

#Вірна ключ карта власника сейфу
uid = [180, 83, 123, 187]

#Виставлення Сервопривід на потрібну позицію
pwm = PWM(servoPin, freq=50)
pwm.duty(128)
time.sleep(1)

#Екран вітання
oled.text('ййййййййййййййййййййй', 0, -2)
oled.text('SafeBOX', 30, 16)
oled.text('Version: 1.5JX', 9, 42)
oled.text('ййййййййййййййййййййй', 0, 58)
oled.show()
time.sleep(2)

Login_Attempt = 0
Disabling_Times = 0

#Стани сейфу

    #(Очікування)
def SafeBOX_Waiting():
    oled.fill(0)
    oled.text('ййййййййййййййййййййй', 0, -2)
    oled.text('Waiting for', 0, 20)
    oled.text('Your Card...', 0, 32)
    oled.text('ййййййййййййййййййййй', 0, 58)
    oled.show()
SafeBOX_Waiting()

    #(Блокування)
def SafeBOX_Disabled():
    global Login_Attempt
    global Disabling_Times 
    if Disabling_Times == 0:
        for i in range(1, 0, -1):
            oled.fill(0)
            oled.text('SafeBOX For now ', 0, 0)
            oled.text('Disabled', 0, 16)
            oled.text('Try Again after', 0, 38)
            oled.text(f'{i} Minutes', 0, 48)
            oled.show()
            time.sleep(60)
    elif Disabling_Times == 1:
        for i in range(5, 0, -1):
            oled.fill(0)
            oled.text('SafeBOX For now ', 0, 0)
            oled.text('Disabled', 0, 16)
            oled.text('Try Again after', 0, 38)
            oled.text(f'{i} Minutes', 0, 48)
            oled.show()
            time.sleep(60)
    elif Disabling_Times == 2:
        for i in range(15, 0, -1):
            oled.fill(0)
            oled.text('SafeBOX For now ', 0, 0)
            oled.text('Disabled', 0, 16)
            oled.text('Try Again after', 0, 38)
            oled.text(f'{i} Minutes', 0, 48)
            oled.show()
            time.sleep(60)
    elif Disabling_Times == 3:
        for i in range(60, 0, -1):
            oled.fill(0)
            oled.text('SafeBOX For now ', 0, 0)
            oled.text('Disabled', 0, 16)            
            oled.text('Try Again after', 0, 38)
            oled.text(f'{i} Minutes', 0, 48)
            oled.show()
            time.sleep(60)
    else:
        while True:
            oled.fill(0)
            oled.text('SafeBOX For now ', 0, 0)
            oled.text('Disabled', 0, 16)        
            oled.text('System blocked &', 0, 38)
            oled.text('Cant be unblocked', 0, 48)
            oled.show()
            time.sleep(3)
    Disabling_Times += 1
    print("Disabling_Times: ", Disabling_Times)
    Login_Attempt = 0
    SafeBOX_Waiting()

#Відкривання та закривання замку
    
    #(Відкриття замку)
def Servo_Open():
    pwm = PWM(servoPin, freq=50)
    pwm.duty(25)
    
    #(Закриття замку)
def Servo_Close():
    pwm = PWM(servoPin, freq=50)
    pwm.duty(128)

#Вхід інформації з RFID та порівняння з базою 
while True:
    if rc522.PICC_IsNewCardPresent():
        if rc522.PICC_ReadCardSerial() == True:
            print("Card UID:", end=' ')
            print(rc522.uid.uidByte[0 : rc522.uid.size])
            if rc522.uid.uidByte[0 : rc522.uid.size] == uid:
                oled.fill(0)
                oled.text('ййййййййййййййййййййй', 0, -2)
                oled.text('Access Allowed!', 0, 25)
                oled.text('ййййййййййййййййййййй', 0, 58)
                oled.show()
                Servo_Open()
                Login_Attempt = 0
                Disabling_Times = 0
                time.sleep(0.5)
            else:
                Servo_Close()
                Login_Attempt += 1 
                oled.fill(0)
                oled.text('ййййййййййййййййййййй', 0, -2)
                oled.text('Access Denied!', 0, 18)
                oled.text('Attempts left: ' + str(4 - Login_Attempt), 0, 42)
                oled.text('ййййййййййййййййййййй', 0, 58)
                oled.show()
                print("Login_Attempt =", Login_Attempt)
            if Login_Attempt == 4:
                time.sleep(0.5)
                SafeBOX_Disabled()
            else:
                time.sleep(3)
                Servo_Close()
                SafeBOX_Waiting()