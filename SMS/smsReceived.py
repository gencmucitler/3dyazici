#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import re
import os
import netifaces as ni
import json

def ip_adresi_ppp0():
    try:
        ni.ifaddresses('ppp0')
        ip = ni.ifaddresses('ppp0')[ni.AF_INET][0]['addr']
        return ip
    except Exception:
        return "0.0.0.0"


def ngrok_adres():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    
    with open('tunnels.json') as data_file:    
        datajson = json.load(data_file)

    for i in datajson['tunnels']:
        msg =  i['public_url']

    return msg


telefon="05xxxxxxx"
Role_Yazici =  21
Role_Aydinlatma =  20
 
GPIO.setmode(GPIO.BCM)
filename=str(sys.argv[1])                               #Gammu will pass the filename of the new SMS as an argument
complete_filename="/var/spool/gammu/inbox/"+filename    #we create the full path to the file here
 
GPIO.setup(Role_Yazici , GPIO.OUT)
GPIO.setup(Role_Aydinlatma , GPIO.OUT)
 
sms_file=open(complete_filename,"r")
#read the contents of the SMS file
message=sms_file.read(160) #note that a not-parted SMS can be maximum 160 characters
 
#search the contents and perform an action. Rather than use 'find',
# we will use regular expression (re) so we can ignore case.
#Most smartphones will have the first letter capitalised
if re.search('YARDIM', message, re.IGNORECASE):
        os.system("echo \"AC, KAPAT, LED, LEDKAPAT, 3G, 3GKAPAT, REBOOT, ADRES, WEBCAM, NGROK komutlarını kullanabilirsiniz.\" | gammu-smsd-inject TEXT " + telefon)
elif re.search('LEDKAPAT', message, re.IGNORECASE):
        GPIO.output(Role_Aydinlatma , GPIO.HIGH)
        os.system("echo \"Aydınlatma kapatıldı.\" | gammu-smsd-inject TEXT " + telefon)        
elif re.search('LED', message, re.IGNORECASE):
        GPIO.output(Role_Aydinlatma , GPIO.LOW)
        os.system("echo \"Aydınlatma acildı.\" | gammu-smsd-inject TEXT " + telefon)
elif  re.search('3GKAPAT', message, re.IGNORECASE):
        os.system("sudo sakis3g disconnect")
        os.system("echo \"internet bağlantısı kesildi..\" | gammu-smsd-inject TEXT " + telefon)
elif  re.search('REBOOT', message, re.IGNORECASE):
        os.system("echo \"Raspberry pi resetleniyor..\" | gammu-smsd-inject TEXT " + telefon)
        time.sleep(5)
        os.system("sudo reboot")
elif re.search('AC', message, re.IGNORECASE):
        GPIO.output(Role_Yazici , GPIO.LOW)
        os.system("echo \"3d yazıcı acildı.\" | gammu-smsd-inject TEXT " + telefon)
elif re.search('KAPAT', message, re.IGNORECASE):
        GPIO.output(Role_Yazici , GPIO.HIGH)
        os.system("echo \"3d yazıcı kapatıldı.\" | gammu-smsd-inject TEXT " + telefon)
elif  re.search('3G', message, re.IGNORECASE):
        os.system("sudo sakis3g connect APN=\"internet\"")
        os.system("echo \"internete bağlanıldı..\" | gammu-smsd-inject TEXT " + telefon)
elif  re.search('ADRES', message, re.IGNORECASE):
        ipadresi=ip_adresi_ppp0()
        mesaj="echo \""+ ipadresi + "\" | gammu-smsd-inject TEXT " + telefon
        os.system(mesaj)
elif  re.search('WEBCAM', message, re.IGNORECASE):
        os.system("sudo service webcamd restart")
        os.system("echo \"Webcam servisi resetlendi..\" | gammu-smsd-inject TEXT " + telefon)
elif  re.search('NGROK', message, re.IGNORECASE):
        ngrok=ngrok_adres()
        mesaj="echo \""+ ngrok + "\" | gammu-smsd-inject TEXT " + telefon
        os.system(mesaj)    
