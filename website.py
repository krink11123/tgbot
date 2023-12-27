import json
from flask import Flask, render_template, request
import json
import os
import threading

def get_session_data():
    with open("sessions.json", "r") as f:
        return json.load(f)

def get_autoresponder_data():
    with open("responderconfig.json", "r") as f:
        return json.load(f)


def get_autoposterconfig():
    with open("autoposterconfig.json", "r") as f:
        return json.load(f)



app = Flask(__name__)

#request.form['submit']



def toggle_mute(user_id):
    with open("sessions.json", 'r') as f:
        data = json.load(f)

    for session in data:
        if str(session['user_id']) == user_id:
            if session['muted'] == False:
                session['muted'] = True
            else:
                session['muted'] = False
    with open("sessions.json", 'w') as f:
        json.dump(data, f, indent=4)

def save_autoresponder_data(gpt_key, prompt, price, cashapp, bitcoin, litecoin, ethereum):
    with open("responderconfig.json", "r") as f:
        data = json.load(f)
    print(data)
    data['gpt_key'] = gpt_key
    data['prompt'] = prompt
    data['price'] = price
    data['cashapp'] = cashapp
    data['bitcoin'] = bitcoin
    data['litecoin'] = litecoin
    data['ethereum'] = ethereum
    with open("responderconfig.json", "w") as f:
        json.dump(data, f, indent=4)

def save_autoposter_data(upload_every, custom_message, custom_message_frequency, custom_message2, custom_message2_frequency, channel):
    with open("autoposterconfig.json", "r") as f:
        data = json.load(f)
    print(data)
    data['upload_every'] = upload_every
    data['custom_message'] = custom_message
    data['custom_message_frequency'] = custom_message_frequency
    data['custom_message2'] = custom_message2
    data['custom_message2_frequency'] = custom_message2_frequency
    data['channel'] = channel
    with open("autoposterconfig.json", "w") as f:
        json.dump(data, f, indent=4)




UPLOAD_FOLDER = 'lilvideos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        print(request.form['submit'])
        if request.form['submit'] == "Upload":
            # Check if the POST request has file parts
            if 'file' not in request.files:
                return redirect(request.url)

            files = request.files.getlist('file')

            # Iterate over the uploaded files
            for file in files:
                # If the user does not select a file, the browser submits an empty file
                if file.filename == '':
                    continue

                # Check if the file is allowed (for example, only allow .txt files)
                # You can add more file extensions as needed
                if file:
                    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(filename)
            return 'Files uploaded successfully'
        else:
            save_autoposter_data(request.form['upload_every'],request.form['custom_message'],request.form['custom_message_frequency'],request.form['custom_message2'],request.form['custom_message2_frequency'],request.form['channel'])
            print("kkr")

    return render_template('upload.html', file_amount=len(os.listdir('liloutput')), data=get_autoposterconfig())


@app.route('/autorespondersettings', methods =["GET", "POST"])
def autorespondersettings():
    if request.method == "POST":
        save_autoresponder_data(request.form['gpt_key'],request.form['prompt'],request.form['price'],request.form['cashapp'],request.form['bitcoin'],request.form['litecoin'],request.form['ethereum'])
        print('aa')
    return render_template('autorespondersettings.html', data=get_autoresponder_data())


@app.route('/', methods =["GET", "POST"])
def display_accounts():
    if request.method == "POST":
        print(request.form['submit'])
        toggle_mute(str(request.form['submit']))
    session_data = get_session_data()
    return render_template('index.html', data=session_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')
