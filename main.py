import json

import logging

import sys
from google.appengine.api import urlfetch
import webapp2

from treebot.bot import HarveyBot
from treebot.tree import TREE
from treebot.userevents import UserEventsDao

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


VERIFY_TOKEN = "CREATE_YOUR_OWN_RANDOM_VERIFY_TOKEN"


class MainPage(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        super(MainPage, self).__init__(request, response)
        logging.info("Initialising with new bot.")
        self.bot = HarveyBot(send_message, UserEventsDao(), TREE)

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        mode = self.request.get("hub.mode")
        if mode == "subscribe":
            challenge = self.request.get("hub.challenge")
            verify_token = self.request.get("hub.verify_token")
            if verify_token == VERIFY_TOKEN:
                self.response.write(challenge)
        else:
            self.response.write("Ok")

    def post(self):
        data = json.loads(self.request.body)
        logging.info("Got data: %r", data)
        # log(data)  # you may not want to log every incoming message in production, but it's good for testing

        if data["object"] == "page":

            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]

                    if messaging_event.get("message"):
                        # recipient_id = messaging_event["recipient"][
                        #     "id"]  # the recipient's ID, which should be your page's facebook ID
                        message = messaging_event['message']
                        if message.get('is_echo'):
                            logging.info("Ignoring echo event: " + message.get('text', ''))
                            continue
                        message_text = messaging_event['message'].get('text', '')
                        logging.info("Got a message: %s", message_text)
                        self.bot.handle(sender_id, message_text)

                    if messaging_event.get("delivery"):  # delivery confirmation
                        logging.info("Delivery")

                    if messaging_event.get("optin"):  # optin confirmation
                        logging.info("Opt-in")

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        payload = messaging_event['postback']['payload']
                        self.bot.handle(sender_id, payload)
                        logging.info("Post-back")


def get_postback_buttons_message(message_text, possible_answers):
    if possible_answers is not None and len(possible_answers) <= 3:
        buttons = []
        for answer in possible_answers:
            if len(answer) > 20:
                return None
            buttons.append({
                "type": "postback",
                "title": answer,
                "payload": answer,
            })
        return {
            "attachment": {
                "type":"template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": buttons,
                }
            }
        }
    return None


def send_message(recipient_id, message_text, possible_answers):
    logging.info("Sending message to %r: %s", recipient_id, message_text)
    headers = {
        "Content-Type": "application/json"
    }
    message = get_postback_buttons_message(message_text, possible_answers)
    if message is None:
        message = {"text": message_text}

    raw_data = {
        "recipient": {
            "id": recipient_id
        },
        "message": message
    }
    data = json.dumps(raw_data)
    r = urlfetch.fetch("https://graph.facebook.com/v2.6/me/messages?access_token=%s" % VERIFY_TOKEN,
                       method=urlfetch.POST, headers=headers, payload=data)
    if r.status_code != 200:
        logging.error("Error sending message: %r", r.status_code)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
