from flask import Flask, request
import requests,json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
url = "https://codex-api.herokuapp.com"
headers = {
  'Content-Type': 'application/json'
}

choice = False
languages = ["cpp", "py", "java", "go","cs", "js"]
option = 0
@app.route("/bot", methods=["POST"])
def bot():
    global choice, option
    usr_msg = request.values.get("Body",'')
    bot_response = MessagingResponse()
    msg = bot_response.message()
    # print(choice)
    # print(usr_msg)
    if choice == False and ("hello" in usr_msg.lower() or "hi" in usr_msg.lower()):
        msg.body("Hello there! Still I am in developing stage so still I can run code without input only. Press 1 to c/c++ code\nPress 2 to python code\nPress 3 to java code\nPress 4 to GoLang code\nPress 5 to c# code\nPress 6 to nodejs code")

    elif choice==False and usr_msg>='1' and usr_msg<='6':
        option = int(usr_msg)-1
        msg.body(f"I am waiting to get {languages[option]} code.")
        choice = True

    elif choice == True:
        payload = json.dumps({
            "code": usr_msg,
            "language": languages[option],
            "input": ""
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()["success"] == False:
            msg.body("Error! Please check the code again.")
        elif response.json()["success"] == True:
            msg.body(response.json()["output"])
        choice =False
    return str(bot_response)

if __name__ == "__main__":
    app.run(debug=True)