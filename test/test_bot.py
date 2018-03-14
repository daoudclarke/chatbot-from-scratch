from treebot.bot import TreeBot, verify_tree
from treebot.mockuserevents import MockUserEventsDao

Q1 = 'Hello. How long do you need to stay in the UK?'
TREE = {
    'say': Q1,
    'answers': {
        '6 months or more': {
            'say': 'Other visa'
        },
        'less than 6 months': {
            'say': 'Visitor visa'
        }
    }
}


def test_simple_response():
    responses = []
    bot = TreeBot(lambda user, message, possible_answers: responses.append((user, message)), MockUserEventsDao(), TREE)
    user_id = 1
    bot.handle(user_id, "Hello")
    assert responses == [(1, Q1)]
    bot.handle(user_id, '6 months or more')
    assert responses == [(1, Q1), (1, 'Other visa')]


def test_partial_match():
    responses = []
    bot = TreeBot(lambda user, message, possible_answers: responses.append((user, message)), MockUserEventsDao(), TREE)
    user_id = 1
    bot.handle(user_id, "Hello")
    assert responses == [(1, Q1)]
    bot.handle(user_id, 'Less')
    assert responses == [(1, Q1), (1, 'Visitor visa')]


def test_verify_tree():
    result = verify_tree(TREE)
    assert result is None
