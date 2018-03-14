from collections import defaultdict


class MockUserEventsDao(object):
    def __init__(self):
        self.events = defaultdict(list)

    def add_user_event(self, user, direction, message):
        self.events[user].append((direction, message))

    def get_user_events(self, user):
        return list(self.events[user])