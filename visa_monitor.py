# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime, timedelta
import pywhatkit
import json
import os
from config import API_URL, PHONE_NUMBER, CHECK_INTERVAL, SOURCE_COUNTRY, MISSION_COUNTRY
import pyautogui

class VisaMonitor:
    def __init__(self):
        self.seen_appointments = self.load_seen_appointments()
        
    def load_seen_appointments(self):
        try:
            with open('seen_appointments.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()
            
    def save_seen_appointments(self):
        try:
            with open('seen_appointments.json', 'w') as f:
                json.dump(list(self.seen_appointments), f)
        except Exception as e:
            print(f"Görülen randevular kaydedilirken hata: {str(e)}")
            
    def send_whatsapp_message(self, message):
        try:
            now = datetime.now()
            pywhatkit.sendwhatmsg_instantly(
                PHONE_NUMBER, 
                message,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            # Mesajı otomatik gönder
            time.sleep(2)  # WhatsApp Web'in açılması için kısa bir bekleme
            pyautogui.press('enter')
            return True
        except Exception as e:
            print(f"WhatsApp mesaji gonderilirken hata: {str(e)}")
            return False
            
    def check_appointments(self):
        try:
            response = requests.get(API_URL)
            data = response.json()
            
            available_appointments = [
                appointment for appointment in data 
                if appointment["source_country"] == SOURCE_COUNTRY 
                and appointment["mission_country"] == MISSION_COUNTRY
                and appointment["appointment_date"] is not None
                and "Ankara" in appointment["center_name"]
            ]
            
            new_appointments_found = False
            today = datetime.now().date()
            
            for appointment in available_appointments:
                appointment_date = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d').date()
                
                if appointment_date > today:
                    appointment_id = f"{appointment['center_name']}_{appointment['appointment_date']}"
                    
                    if appointment_id not in self.seen_appointments:
                        message = (
                            "BOS VIZE BASVURU TARIHI BULUNDU!\n\n"
                            f"Merkez: {appointment['center_name']}\n"
                            f"Tarih: {appointment['appointment_date']}\n\n"
                            f"Link:\n{appointment['book_now_link']}"
                        )
                        
                        if self.send_whatsapp_message(message):
                            self.seen_appointments.add(appointment_id)
                            self.save_seen_appointments()
                            new_appointments_found = True
                            print(f"Yeni randevu bulundu: {appointment_id}")
            
            return new_appointments_found
            
        except Exception as e:
            print(f"Randevu kontrolunde hata: {str(e)}")
            return False
    
    def run(self):
        print(f"Program baslatildi. {len(self.seen_appointments)} onceki randevu yuklendi.")
        
        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Kontrol yapiliyor... {current_time}")
            
            try:
                if self.check_appointments():
                    print("Yeni randevu bulundu!")
                else:
                    print("Yeni randevu yok.")
            except Exception as e:
                print(f"Hata olustu: {str(e)}")
            
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor = VisaMonitor()
    monitor.run() 