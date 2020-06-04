'''
clash.py
Performs HTTP requests to the Clash of Clans API to fetch clan and user data.
Formats data into strings to be sent as messages by the Discord bot.
'''

import requests
import random
import os

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer ' + os.environ.get('CLASH_KEY')
}

# Clash of Clans API requires IP so use Fixie as a proxy to
# make requests to the API while the bot is deployed on Heroku.
proxyDict = {
    "http"  : os.environ.get('FIXIE_URL', ''),
    "https" : os.environ.get('FIXIE_URL', '')
}

class Clan:
    '''
    Clan class offers methods to fetch data related to the clan.
    '''
    url = 'https://api.clashofclans.com/v1/clans/%23QOUUCYV2/'

    def get_war(self):
        response = requests.get(self.url + 'currentwar', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = ''
        if data['state'] == 'notInWar':
            to_ret = 'The DMND Life is not in a war right now.'
        else:
            to_ret += '```\nThe DMND Life is in a war vs. ' + data['opponent']['name'] + '.\n\n' + 'The DMND Life: ' + data['clan']['stars'] + ' stars, ' + data['clan']['attacks'] + 'attacks\n' + data['opponent']['name'] + ': ' + data['opponent']['stars'] + ' stars, ' + data['opponent']['attacks'] + 'attacks\n```'
        return to_ret

    def get_members(self):
        '''Returns a list of members in the clan.'''
        response = requests.get(self.url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = ''
        for user in data['items']:
           to_ret += '\n' + ['name']
        return to_ret

    def get_random_member(self):
        '''Returns the name of a random member in the clan'''
        response = requests.get(self.url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        member = random.choice(data['items'])
        return member['name'] + ' is moist.'

    def cwl_info(self):
        '''Returns info related to the Clan War League'''
        response = requests.get(self.url + 'currentwar/leaguegroup', headers=headers, proxies=proxyDict)
        data = response.json()
        if data['state'] == 'inWar':
            state = 'In War\n'
        to_ret = '```\n' + state + 'Season: ' + str(data['season']) + '\n\n' + 'Clans: '
        for clan in data['clans']:
            to_ret += '\n -' + clan['name']

        to_ret += '\n```'
        return to_ret

    def cwl_clan_info(self, name):
        '''Returns info related to a clan in tbe Clan War League'''
        response = requests.get(self.url + 'currentwar/leaguegroup', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = '```\n'
        for clan in data['clans']:
            if clan['name'] == name:
                to_ret += (name + '\n' + 'Level:' + str(clan['clanLevel']) + '\n\nMembers:')
                for member in clan['members']:
                    to_ret += '\n -' + member['name'] + ': ' 'TH' + str(member['townHallLevel'])
                to_ret += '\n```'
                return to_ret
        return 'Clan not in CWL'

    def get_member(self, name):
        '''Returns info related to a member in the clan'''
        response = requests.get(self.url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        for user in data['items']:
            if name == user['name']:
                to_ret = user['name'] + '\n' + user['role'] + '\n' + 'Trophies: ' + str(user['trophies']) + ',  Donated: ' + str(user['donations']) + ', Received: ' + str(user['donationsReceived'])
                return to_ret
        return 'User not found in clan.'
