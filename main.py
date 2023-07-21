import aprslib
import logging
import requests
import json

webhook = "WEBHOOK_URL_HERE"
def send_discord_message(webhook_url, sender, message):
    payload = {
        "username": sender,
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print("Failed to send Discord message:", response.text)

def callback(packet):
    if "addresse" in packet:
        if "DCDGTE" in packet['addresse']:
            print(packet)
            send_discord_message(webhook, "DCDGTE", f"{packet['from']} : {packet['message_text'].replace('DCDGTE','')}")
            if "msgNo" in packet:
                print("Sending ack")
                AIS.sendall(f"DCDGTE>DCDGTE::{packet['from']}   :ack{packet['msgNo']}")

print("Setting login...")
AIS = aprslib.IS("WG0A-8", passwd="")
print("Logged in...")
# AIS.set_filter("t/m")
print("Filter set...")
AIS.connect()
print("Connected...")
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=False)