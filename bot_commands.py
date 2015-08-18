"""Fun with Slackbots."""

import re
import os
import json
import requests
from random import randint

from bender.signals import event_received, message_received

WUNDERGROUND_API_KEY = os.environ['WUNDERGROUND_API_KEY']


def roll_die(sides):
    return randint(1, int(sides))

@event_received.connect
def echo(sender, **kwargs):
    """Logs events to the console."""
    print(kwargs['event']._raw)
    return True


@message_received.connect
def my_name(sender, **kwargs):
    """Responds to mentions of the bot's name."""
    try:
        event = kwargs['event']

        if re.search('deep thought', event.text, re.IGNORECASE):
            sender.slack_client.send_message('That\'s my name. :grin:', event.channel)
    except:
        pass


@message_received.connect
def spock(sender, **kwargs):
    """Mr. Spock"""
    try:
        event = kwargs['event']

        if re.search('spock', event.text, re.IGNORECASE):
            sender.slack_client.send_message('https://goo.gl/7wBOIB', event.channel)
    except:
        pass


@message_received.connect
def meaning_of_life(sender, **kwargs):
    """Explains the meaning of life."""
    try:
        event = kwargs['event']

        if re.search('meaning of life', event.text, re.IGNORECASE):
            sender.slack_client.send_message('42', event.channel)
    except:
        pass


@message_received.connect
def dice(sender, **kwargs):
    """Rolls a die."""
    try:
        event = kwargs['event']

        regex = re.compile('roll \(d(\d{1,4})\)')
        s = regex.search(event.text)
        if s is not None:
            sides = int(s.groups()[0])
            if sides > 1 and sides < 9999:
                output = 'I rolled a {}-sided die and got {}'.format(
                    str(sides),
                    str(roll_die(sides))
                )
                sender.slack_client.send_message(output, event.channel)
    except:
        print('exception on dice()')
        pass


@message_received.connect
def weather(sender, **kwargs):
    """Posts the weather report by zip code."""
    try:
        event = kwargs['event']

        regex = re.compile('weather\((\d{5})\)')
        w = regex.search(event.text)
        if w is not None:
            zipcode = w.groups()[0]
            q = 'http://api.wunderground.com/api/{key}/geolookup/q/{zipcode}.json'.format(
                key=WUNDERGROUND_API_KEY,
                zipcode=zipcode
            )
            res = json.loads(requests.get(q).text)
            weather_path = res['location']['requesturl'].split('/')
            state = weather_path[-2]
            city = weather_path[-1]
            weather_url = 'http://api.wunderground.com/api/{key}/forecast/q/{state}/{city}.json'.format(
                    key=WUNDERGROUND_API_KEY,
                    state=state,
                    city=city
            )
            weather_data = json.loads(requests.get(weather_url).text)
            # Uncomment the next line to view JSON
            # print(weather_data)
            forecast_title = weather_data['forecast']['txt_forecast']['forecastday'][0]['title']
            fcttext = weather_data['forecast']['txt_forecast']['forecastday'][0]['fcttext']
            forecast_icon = weather_data['forecast']['txt_forecast']['forecastday'][0]['icon_url']
            output = '*{}:* {} \n{}'.format(forecast_title, fcttext, forecast_icon)
            sender.slack_client.send_message(output, event.channel)
    except:
        pass

@message_received.connect
def some_message(sender, **kwargs):
    """Responds to mentions of keyboard cat."""
    try:
        event = kwargs['event']
        if 'keyboard cat' in event.text:
            sender.slack_client.send_message('https://youtu.be/J---aiyznGQ', event.channel)
    except:
        pass

@message_received.connect
def cowsay(sender, **kwargs):
    """Cowsay API integration."""
    try:
        event = kwargs['event']

        regex = re.compile('cowsay\((.*)\)')
        m = regex.search(event.text)
        if m is not None:
            text = m.groups()[0].replace(' ', '%20')
            q = 'http://cowsay.morecode.org/say?message={}&format=text'.format(text)
            output = requests.get(q).text
            sender.slack_client.send_message(output, event.channel)
    except:
        pass


@message_received.connect
def raise_hands(sender, **kwargs):
    """Responds to smiley faces."""
    try:
        event = kwargs['event']

        if ':simple_smile:' in event.text:
            sender.slack_client.send_message(':raised_hands:', event.channel)
    except:
        pass


@message_received.connect
def process_message(sender, **kwargs):
    """Sends commands to the command_router if prefixed with `!`."""
    try:
        event = kwargs['event']
        if event.text.startswith('!'):
            command_router(event.text[1:], sender, event.channel)

    except:
        pass

def zen(sender, channel):
    """Displays the Zen of Python."""
    try:
        the_zen_of_python = """The Zen of Python, by Tim Peters

        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        Special cases aren't special enough to break the rules.
        Although practicality beats purity.
        Errors should never pass silently.
        Unless explicitly silenced.
        In the face of ambiguity, refuse the temptation to guess.
        There should be one-- and preferably only one --obvious way to do it.
        Although that way may not be obvious at first unless you're Dutch.
        Now is better than never.
        Although never is often better than *right* now.
        If the implementation is hard to explain, it's a bad idea.
        If the implementation is easy to explain, it may be a good idea.
        Namespaces are one honking great idea -- let's do more of those!
        """
        sender.slack_client.send_message(the_zen_of_python, channel)
    except:
        pass

def command_router(command, sender, channel):
    """Routes commands."""
    commands = {
        'importthis': zen
    }

    command_fn = commands.get(command)
    if command_fn:
        command_fn(sender, channel)

