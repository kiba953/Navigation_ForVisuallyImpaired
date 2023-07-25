from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
from easyIO import *
import network

Battery = str(map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100))
# touch_button0 = M5Btn(text=' ', x=-40, y=-80, w=400, h=400, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
wcLabel = M5Label("Starting up...", x=1, y=0, color=0x000, font=FONT_MONT_26, parent=None)
battery = M5Label("Battery: "+ Battery + "%", x=222, y=220, color=0x000, font=FONT_MONT_14, parent=None)


previousSound = "none"
previousSound2 = "none"

def vibrate():
    power.setVibrationEnable(True)
    wait(0.5)
    power.setVibrationEnable(False)
    return


def playSound(mp3):
    global previousSound
    global previousSound2
    if previousSound != mp3:
      vibrate()
      speaker.playWAV('/sd/voice/' + mp3 + ".wav", volume = 10)
      previousSound2 = previousSound
      previousSound = mp3
      return
    return

def touch_button0_pressed():
  playSound(previousSound)
  
# imu0 = imu.IMU()
# mag = unit.get(unit.MAGNETOMETER)

prev = "0"

speaker.playTone(220, 1/2, volume=6)
wait_ms(2000)
wcLabel.set_text("Welcome to IIT Bhilai")
playSound("welcome")
previousSound = "welcome"

# run = True
# playAgain = False

# if playAgain == True:
#   playSound(previousSound)
#   playAgain = False

while True:
  if btnA.isPressed():
    power.powerOff()
  
  # mx, my, mz = imu.magnet
  screen = M5Screen()
  screen.clean_screen()
  screen.set_screen_bg_color(0xffffff)
  power.setVibrationIntensity(50)
  wifi_label = M5Label("Scanning for WiFi...", x=1, y=220, color=0x000, font=FONT_MONT_10, parent=None)
  Battery2 = str(map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100))
  battery2 = M5Label("Battery: "+ Battery2 + "%", x=222, y=220, color=0x000, font=FONT_MONT_14, parent=None)
  touch_button0 = M5Btn(text=' ', x=-40, y=-80, w=400, h=400, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
  # aPress = "false"
  # bPress = "false"
  if btnB.wasPressed():
    playSound(previousSound)
  # touch_button0.pressed(touch_button0_pressed) 
  # if btnA.isPressed():
  #   aPress = "true"
    
  # elif btnB.isPressed() and aPress == "true":
  #   bPress = "true"
    
  # elif btnC.isPressed() and bPress == "true":
  #   power.powerOff()
      
  
  # pitch = imu0.acceleration[0]
  # roll = imu0.acceleration[1]
  # yaw = imu0.acceleration[2]
  # x = imu0.ypr[1]
  # y = imu0.ypr[2]
  # gx = imu0.gyro[0]
  # gy = imu0.gyro[1]
  # gz = imu0.gyro[2]
  #mag_x, mag_y, mag_z = imu0.magnetic
  #yaw = math.atan2(mag_y, mag_x)
  # direction =  M5Label("Loading..", x=0, y=0, color=0x000, font=FONT_MONT_26, parent=None)
  # direction.set_text(" "+ str(pitch) + " \n"+str(roll)   + "\n " +str(yaw)+"\n " +str(x)+"\n " +str(y)+"\n " +str(gx)+"\n " +str(gy)+"\n " +str(gz) )

  wifi = network.WLAN(network.STA_IF)
  wifi.active(True)
  scan_results = wifi.scan()
  
  filtered_results = [result for result in scan_results if result[0].decode() == "IITBhilai"]
  
  sorted_results = sorted(filtered_results, key=lambda x: x[3], reverse=True)
  
  for i in range(min(5, len(sorted_results))):
      ssid = sorted_results[i][0].decode()
      rssi = sorted_results[i][3]
      mac = ":".join("{:02x}".format(x) for x in sorted_results[i][1])
      label = M5Label("yo", x=1, y=i*35, color=0x000, font=FONT_MONT_10, parent=None)
      label.set_text("SSID: " + ssid + "\nRSSI: " + str(rssi)+"\nMAC: " + mac)
  
  wifi_label.set_text("WiFi scan complete!")

  mac2 = ":".join("{:02x}".format(x) for x in sorted_results[0][1])
  
  
  if mac2 =="b0:8b:cf:16:3c:21" and prev != mac2: #Director
  #if mac2 == "88:b1:e1:a0:e9:10": #hostel
  # if mac2 == "84:3d:c6:9b:b5:40": #Its inside EE lab b5:40 ending
      playSound("director")
      
  elif mac2 == "84:3d:c6:b1:51:70" and prev != mac2: #Outside conf room
  #elif mac2 == "88:b1:e1:a0:e9:10" and prev != mac2: #hostel
  #elif mac2 == "88:b1:e1:ad:d7:90": #hostel
  #elif mac2 == "84:3d:c6:7a:8c:20": #Outside ME lab 8c20
      if previousSound2 != "117":
        playSound("117")
        if previousSound2 == "eeTo117":
          playSound("117toDirector")
        elif previousSound2 == "welcome" or previousSound2 == "director":
          playSound("117toEE")

  
  elif mac2 == "84:3d:c6:9b:b5:40" and prev != mac2: #Its inside EE lab b5:40 ending
  #elif mac2 == "88:b1:e1:a0:e9:10" and prev != mac2: #hostel
        playSound("ee")
        if previousSound2 == "welcome":
          playSound("eeTo117")
  # elif mac2 == "84:3d:c6:35:68:70" and prev != mac2: #B113
        # playSound("b113")

  prev=mac2
  wait_ms(3000)
