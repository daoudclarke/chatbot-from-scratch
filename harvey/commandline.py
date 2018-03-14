import yaml

from harvey.bot import verify_tree, HarveyBot
from harvey.tree import TREE
from harvey.mockuserevents import MockUserEventsDao


def callback(user, message, possible_answers):
    if possible_answers:
        print message, "(%s)" % ', '.join(possible_answers) if possible_answers is not None else ''
    else:
        print message


def run():
    verify_tree(TREE)
    bot = HarveyBot(callback, MockUserEventsDao(), TREE)

    while True:
        value = raw_input('> ')
        bot.handle(1, value)


if __name__ == "__main__":
    run()
