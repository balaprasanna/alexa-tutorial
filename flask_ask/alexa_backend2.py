from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('WelcomeIntent')
def welcome():
    speech_text = "Welcome to stackup.. This is python class...."
    return statement(speech_text).simple_card('Welcome', speech_text)

@ask.intent('GoodByeIntent')
def goodbye():
    speech_text = "Good Bye see you next time..."
    return statement(speech_text).simple_card('Bye', speech_text)


if __name__ == '__main__':
    app.run()