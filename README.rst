A Slackbot for the Code Self Study Chatroom
===========================================

This code runs the *Deep Thought* bot in the Code Self Study chatroom. If you want to add functionality, fork this repo, edit the commands.py file and make a pull request on the :code:`dev` branch.

Installation
------------

Make a Python 2.7 virtualenv

Install the requirements into your virtualenv with :code:`pip install -r requirements.txt`

Create environment variables:

* :code:`$ export SLACK_API_TOKEN="your-bot-token"`
* :code:`$ export WUNDERGROUND_API_KEY="your-api-token"`

Run the bot with :code:`python run.py`

Contributing
------------

If you want to add commands to the bot, fork the :code:`dev` branch, edit the :code:`commands.py` file and make a pull request.


