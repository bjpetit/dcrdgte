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
                # The msgNo parsing can chop off trailing chars. Doing my own parsing here.
                message_num = packet['raw'].split('{')[1]
                print(f'{message_num}')
                # This might be pretty close to correct for an ack
                AIS.sendall(f"DCDGTE>DCDGTE::{packet['from']:9}:ack{message_num}")

print("Setting login...")
AIS = aprslib.IS("N0CALL", port="14580", passwd="-1")
print("Logged in...")
AIS.set_filter("t/m")
print("Filter set...")
AIS.connect()
print("Connected...")
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=False)