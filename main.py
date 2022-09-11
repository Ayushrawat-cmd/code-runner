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
code = ""
@app.route("/bot", methods=["POST"])
def bot():
    global choice, option,code 
    usr_msg = request.values.get("Body",'')
    bot_response = MessagingResponse()
    msg = bot_response.message()
    # print(choice)
    # print(usr_msg)
    if choice == False:
        code = usr_msg
        msg.body("Hello there! Still I am in developing stage so still I can run code without input only.\nPress 1 to compile in c/c++ code\nPress 2 to to compile in python code\nPress 3 to to compile in java code\nPress 4 to to compile in GoLang code\nPress 5 to to compile in c# code\nPress 6 to to compile in nodejs code")
        choice = True
        
    elif choice == True and usr_msg>='1' and usr_msg<='6':
        option = int(usr_msg)-1
        payload = json.dumps({
            "code": code,
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
