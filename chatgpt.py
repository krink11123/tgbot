from openai import OpenAI
import json
import time
from telethon import TelegramClient, events
import os

global gpt_key
global prompt
global cashapp
global bitcoin
global litecoin
global ethereum
global api_id
global api_hash
global price



def load_config():
    global gpt_key
    global prompt
    global cashapp
    global bitcoin
    global litecoin
    global ethereum
    global api_id
    global api_hash
    global price
    with open("responderconfig.json", 'r') as f:
        data = json.load(f)
        gpt_key = data['gpt_key']
        prompt = data['prompt']
        cashapp = data['cashapp']
        bitcoin = data['bitcoin']
        litecoin = data['litecoin']
        ethereum = data['ethereum']
        api_id = data['api_id']
        api_hash = data['api_hash']
        price = data['price']

    prompt = prompt.replace("[chashapp]", cashapp).replace("[bitcoin]", bitcoin).replace("[litecoin]", litecoin).replace("[ethereum]", ethereum).replace("[price]", price)



def chat_with_gpt3(session, prompt, model="gpt-3.5-turbo-16k-0613", max_tokens=150):
    try:
        # Append the new user message to the existing session
        session.append({"role": "user", "content": prompt})
        
        # Generate a response based on the updated session
        response = api_client.chat.completions.create(
            model=model,
            messages=session,
            max_tokens=max_tokens
        )
        
        # Return the response and updated session
        return response['choices'][0]['message']['content'].strip(), session
    except Exception as e:
        return str(e), session

def get_session(user_id, username):
    with open("sessions.json", 'r') as f:
        data = json.load(f)
    user_found = False
    for session in data:
        if user_id == session['user_id']:
            return session['session_content'], True

    new_session = {
        "muted" : False,
        "username" : "",
        "user_id" : user_id,
        "session_content" : []
    }

    data.append(new_session)

    with open("sessions.json", 'w') as f:
        json.dump(data, f, indent=4) 


    return [{"role": "system", "content": "You are a helpful assistant."}], False

def save_session(user_id, sessiondata):
    with open("sessions.json", 'r') as f:
        data = json.load(f)
    for session in data:
        if user_id == session['user_id']:
            session['session_content'] = sessiondata

    with open("sessions.json", 'w') as f:
        json.dump(data, f, indent=4) 

def get_user_mute_status(user_id):
    with open("sessions.json", 'r') as f:
        data = json.load(f)

    for session in data:
        if str(session['user_id']) == str(user_id):
            return session['muted']
    return False


load_config()

api_key = gpt_key

api_client = OpenAI(
    api_key=api_key,
)

client = TelegramClient('auto_respoder', api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private and get_user_mute_status(event.sender_id) == False:
        #print(event.message.message)
        while True:
            sender_entity = await client.get_entity(sender_id)
            load_config()
            session, already_chatted = get_session(event.sender_id, sender_entity.first_name)
            print(already_chatted)
            if already_chatted == False:
                automated_response, session = chat_with_gpt3(session, f"{prompt} {event.message.message} .How much is vip whats in vip and how can i pay?")
            else:
                automated_response, session = chat_with_gpt3(session, f"Remember to not begin with hey, hi, hello or anything like that be straight forward and short. Also if someone says something like (cashapp, bitcoin, ethereum) give them the details to that payment methode. With all those instructions in min awnser the following question: {event.message.message}")
            if "Rate limit reached" not in automated_response:
                break
            else:
                print("TIMEOUT!!!")
                time.sleep(25)
        save_session(event.sender_id, session)
        await event.respond(automated_response)

with client:
    client.run_until_disconnected()






#openai.api_key = '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'
#
## Example of chatting with GPT-3
#user_input = "Who was adolg hitler"
#response = chat_with_gpt3(user_input)
#print("GPT-3:", response)
