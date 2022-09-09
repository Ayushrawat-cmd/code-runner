from flask import Flask, request
import requests,json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
url = "https://codex-api.herokuapp.com"
headers = {
  'Content-Type': 'application/json'
}

choice = False
@app.route("/bot", methods=["POST"])
def bot():
    usr_msg = request.values.get("Body",'')
    bot_response = MessagingResponse()
    msg = bot_response.message()
    print(usr_msg)
    if choice == False and "hello" or "hi" in usr_msg.lower():
        msg.body("Hello there! Still I am in developing stage so still I can run only any c++ code here. Press 1 to send code")
    elif "1" in usr_msg:
        msg.body("I am waiting to get c++ code.")
        choice = True
    elif choice == True:
        usr_msg.replace('"', "'")
        # if "cin" in usr_msg:
        payload = json.dumps({
            "code": usr_msg,
            "language": "cpp",
            "input": ""
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()["success"] == False:
            msg.body("Error!Please check the code again.")
        elif response.json()["success"] == False:
            msg.body(response.json()["output"])
    return str(bot_response)

if __name__ == "__main__":
    app.run(debug=True)