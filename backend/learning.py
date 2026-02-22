# learning.py

# simple in-memory learning store
user_preferences = {}


def add_feedback(user: str, category: str):

    if user not in user_preferences:
        user_preferences[user] = {}

    user_preferences[user][category] = (
        user_preferences[user].get(category, 0) + 1
    )


def get_user_bonus(user: str, category: str):

    prefs = user_preferences.get(user, {})
    return prefs.get(category, 0)