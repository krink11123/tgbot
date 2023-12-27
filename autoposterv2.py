import threading
import time
import json
import os
import random
from telethon import TelegramClient, sync


# Define a global variable
timer = 0
upload_message = 0
upload_message2 = 0

# Function to increment the global variable
def increment_global_variable():
    global timer
    while True:
        timer += 1
        time.sleep(1)

increment_thread = threading.Thread(target=increment_global_variable)


current_directory = os.getcwd()
lildirectory_path = f'{current_directory}/liloutput'


increment_thread.start()

def get_autoposterconfig():
    with open("autoposterconfig.json", "r") as f:
        return json.load(f)


def get_folder_status():
    with open("fileexchangeconfig.json", "r") as f:
        return json.load(f)['currently_busy']

lastupload = 0

api_id = '20001746'
api_hash = 'ad25ff9fc57305256ab13ea27c611424'


def test():
    files = 0
    global upload_message
    global upload_message2
    folderstatus = True
    while folderstatus == True:
        folderstatus = get_folder_status()
        time.sleep(1)
    for filename in os.listdir(lildirectory_path):
        file_path = os.path.join(lildirectory_path, filename)
        if os.path.isfile(file_path):
            files+=1
    if files == 0:
        return
    filename = os.listdir(lildirectory_path)[random.randint(0, files)-1]
    file_path = os.path.join(lildirectory_path, filename)
    data = get_autoposterconfig()
    if os.path.isfile(file_path):
        try:
            with TelegramClient('session_name', api_id, api_hash) as client:
                client.start()
                client.send_file(data['channel'], file_path)
                upload_message +=1
                upload_message2 +=1
                if upload_message > int(data['custom_message_frequency']):
                    upload_message = 0
                    client.send_message(data['channel'], data['custom_message'])
                if upload_message2 > int(data['custom_message2_frequency']):
                    upload_message2 = 0
                    client.send_message(data['channel'], data['custom_message2'])
            os.remove(file_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")


    print(files)



while True:
    data = get_autoposterconfig()
    if int(data["upload_every"]) < timer-lastupload:
        lastupload = timer
        test()
        print("yessir")
    time.sleep(1)