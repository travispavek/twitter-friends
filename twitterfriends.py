#!/usr/bin/env python

import argparse
import os

import twitter
import yaml


def load_config():
    conf_path = '%s/.twitterfriends.conf' % os.path.expanduser('~')

    try:
        return yaml.load(open(conf_path, 'r'))
    except IOError:
        raise RuntimeError('~/.twitterfriends.conf does not exist')


def verify_keys(config):
    keys = ['consumer_key',
            'consumer_secret',
            'access_token_key',
            'access_token_secret']

    for key in keys:
        if config['twitterfriends'].get(key) is None:
            raise RuntimeError("Please set '%s' in config file'" % (key))


def get_keys():
    config = load_config()
    verify_keys(config)
    return config['twitterfriends']


def is_rate_limited():
    return api.rate_limit.resources['friends']['/friends/list']['remaining'] == 0


def wait_for_rate_limit_resources():
    if is_rate_limited():
        print('Rate limited, waiting for resources to become available again')


def get_friends(user):
    return map(lambda f: f.screen_name,
               api.GetFriends(screen_name=user))


def get_common_friends(users):
    common_friends = None
    for user in users:
        friends = set(get_friends(user))
        if common_friends is None:
            common_friends = friends
        else:
            common_friends = common_friends & friends
    return common_friends


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--users',
                        help='comma separated list of users')

    args = parser.parse_args()
    api = twitter.Api(**get_keys())
    friends = get_common_friends(args.users.split(','))
    if len(friends) == 0:
        print('There are no friends in common')
    else:
        for friend in friends:
            print(friend)
