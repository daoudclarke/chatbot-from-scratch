import logging
from sys import maxint

DEFAULT = "Sorry, I didn't understand, shall we start again?"
DEFAULT_POSSIBLE_ANSWERS = ["yes", "no"]


def get_content_match(content, tree):
    matches = []
    for key in sorted(tree):
        if content.lower() in key.lower():
            matches.append(key)
    if len(matches) == 1:
        return matches[0]


class TreeBot(object):
    def __init__(self, send_callback, users_dao, tree):
        self.send_callback = send_callback
        self.users_dao = users_dao
        self.tree = tree

    def handle(self, user, message):
        self.users_dao.add_user_event(user, 'received', message)
        history = self.users_dao.get_user_events(user)
        tree = self.tree
        logging.debug("History items: %d", len(history))
        restarting = False
        nothing_sent = True
        response = DEFAULT
        possible_answers = DEFAULT_POSSIBLE_ANSWERS
        for direction, content in history:
            response = DEFAULT
            possible_answers = DEFAULT_POSSIBLE_ANSWERS
            if direction == 'received':
                key = get_content_match(content, tree)
                if nothing_sent:
                    response = tree['say']
                    possible_answers = tree['answers'].keys()
                elif key is not None:
                    tree = tree[key]
                    if 'say' in tree:
                        response = tree['say']
                        possible_answers = None
                        if 'answers' in tree:
                            possible_answers = tree['answers'].keys()
                    restarting = False
                elif restarting:
                    if content == 'yes':
                        tree = self.tree
                        response = tree['say']
                        possible_answers = tree['answers'].keys()
                        restarting = False
            elif direction == 'sent':
                nothing_sent = False
                if 'answers' in tree and direction == 'sent' and content == tree.get('say'):
                    tree = tree['answers']
                elif direction == 'sent' and content == DEFAULT:
                    restarting = True
            else:
                raise ValueError("Unexpected direction: " + direction)

        logging.debug("Responding: %s", response)

        self.send_callback(user, response, possible_answers)
        self.users_dao.add_user_event(user, 'sent', response)


def verify_tree(tree):
    if 'say' in tree:
        if 'answers' in tree:
            return verify_answers(tree['answers'])
    return None


def verify_answers(answers):
    problem = None
    for answer, tree in answers.items():
        if not isinstance(answer, basestring):
            return "Answer is not a string: " + repr(answer)
        problem = verify_tree(tree)
        if problem:
            break
    return problem

