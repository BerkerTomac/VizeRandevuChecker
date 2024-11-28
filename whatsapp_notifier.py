import pywhatkit
from datetime import datetime
from config import PHONE_NUMBER

def send_whatsapp_message(message):
    try:
        # Get current time
        now = datetime.now()
        
        # Send message via WhatsApp
        pywhatkit.sendwhatmsg_instantly(
            phone_no=PHONE_NUMBER,
            message=message,
            wait_time=15,  # Seconds to wait before sending message
            tab_close=False
        )
        print(f"WhatsApp message sent successfully at {now.strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}") 

        