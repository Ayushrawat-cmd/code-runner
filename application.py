from flask import Flask, request
import requests,json
from twilio.twiml.messaging_response import MessagingResponse

application = Flask(__name__)
url = "https://codex-api.herokuapp.com"
headers = {
  'Content-Type': 'application/json'
}

run = False
languages = ["cpp", "py", "java", "go","cs", "js"]
option = 0
code = ""
input_ = ""
input_run = False
@application.route("/bot", methods=["POST"])
def bot():
    global run, option,code,input_,input_run
    usr_msg = request.values.get("Body",'')
    bot_response = MessagingResponse()
    msg = bot_response.message()
    if run == True :
        if input_run == True:
            if usr_msg != "N/A":
                input_ = usr_msg
            msg.body("Hello there! Still I am in developing stage.\nPress 1 to compile in c/c++ code\nPress 2 to compile in python code\nPress 3 to compile in java code\nPress 4 to compile in GoLang code\nPress 5 to compile in c# code\nPress 6 to compile in nodejs code")
            input_run = False
        elif input_run ==False and usr_msg>='1' and usr_msg<='6':
            option = int(usr_msg)-1
            # print(code)
            payload = json.dumps({
                "code": code,
                "language": languages[option],
                "input": input_
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.json()["success"] == False:
                msg.body("Error! Please check the code again.")
            elif response.json()["success"] == True:
                msg.body(response.json()["output"])
            run =False
        else:
            msg.body("Wrong choice! Please type correct choice.")

    elif run == False:
        msg.body("Send your input if you have any. If no pleas type (N/A).")
        code = usr_msg
        run = True
        input_run = True
    else:
        msg.body("Please send code again.")
        run = False
    
    return str(bot_response)

if __name__ == "__main__":
    application.run(debug=True)
