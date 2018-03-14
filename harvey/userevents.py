from google.appengine.ext import ndb

import logging


class UserEvent(ndb.Model):
    user = ndb.StringProperty()
    direction = ndb.StringProperty()
    message = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class UserEventsDao(object):
    def add_user_event(self, user, direction, message):
        event = UserEvent()
        event.user = user
        event.direction = direction
        event.message = message
        logging.info("Adding event: %r", event)
        event.put()

    def get_user_events(self, user):
        events = UserEvent.query(UserEvent.user == user)
        # events = list(events)
        # print "Events", events
        sorted_events = sorted(events, key=lambda x: x.date)
        return [(event.direction, event.message) for event in sorted_events]
