from __future__ import print_function
import json
from twitter import *

config = {
"consumer_key":"<KEY>",
"consumer_secret":"<SECRET>",
"Owner":"<OWNER>",
"OwnerID":"<OWNER_ID>",
"access_key":"<ACCESS_KEY>",
"access_secret":"<ACCESS_SECRET>"
}

def build_speechlet_response(output, should_end_session):
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'shouldEndSession': should_end_session
	}


def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
	session_attributes = {}
	card_title = "Welcome"
	speech_output = "Welcome to twitter reader. I can tell you whats trending in twitter. Ask me whats trending now ?"
	reprompt_text = ""
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def handle_session_end_request():
	card_title = "Session Ended"
	speech_output = "Goodbye "
	should_end_session = True
	return build_response({}, build_speechlet_response(speech_output, should_end_session))



def say_good_bye(intent, session):
	session_attributes = {}
	reprompt_text = None
	card_title = "Session Ended"
	speech_output = "Goodbye"
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def read_trends_from_twitter_for_country(intent, session):
	session_attributes = {}
	reprompt_text = None
	
	location = intent['slots']['locatoinName']['value']
	if location.lower() == "singapore":
	    messages = twitter_helper_with_country("23424948")
	elif location.lower() == "us":
	    messages = twitter_helper_with_country("23424977")
	elif location.lower() == "united states":
	    messages = twitter_helper_with_country("23424977")
	elif location.lower() == "malaysia":
	    messages = twitter_helper_with_country("56013632")
	else:
	    messages = twitter_helper_with_country("23424948")
	speech_output = 'Here are the trending hash tags from {}....{}'.format(location, messages)
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def read_trends_from_twitter(intent, session):
	session_attributes = {}
	reprompt_text = None
	messages = twitter_helper()
	speech_output = 'Here are the following trending hash tags....{}'.format(messages)
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def twitter_helper():
    twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    # SINGAPORE "23424948"
    # US "23424977"
    # MLY 56013632
    results = twitter.trends.place(_id = 23424948)

    print ("Global Trends")
    response_string = ""
    for location in results:
        for trend in location["trends"]:
            print (" - %s" % trend["name"])
            response_string +=  "..." + trend["name"]
            
    return response_string

def twitter_helper_with_country(countryid):
    twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    # SINGAPORE "23424948"
    # US "23424977"
    # MLY 56013632
    results = twitter.trends.place(_id = countryid)

    print ("Global Trends")
    response_string = ""
    for location in results:
        for trend in location["trends"]:
            print (" - %s" % trend["name"])
            response_string +=  "..." + trend["name"]
            
    return response_string


# --------------- Specific Events ------------------

def on_intent(intent_request, session):
	print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	if intent_name == "AskTrendsIntent":
		return read_trends_from_twitter(intent, session)
	elif intent_name == "AskTrendsByLocationIntent":
		return read_trends_from_twitter_for_country(intent, session)
	elif intent_name == "GoodByeIntent":
		return say_good_bye(intent, session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")

# --------------- Generic Events ------------------

def on_session_started(session_started_request, session):
	print("on_session_started requestId=" + session_started_request['requestId']+ ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
	print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
	return get_welcome_response()
	
def on_session_ended(session_ended_request, session):
	print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
	print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']}, event['session'])
	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])
