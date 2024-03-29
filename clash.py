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

# Clash of Clans API requires IP, so use Fixie as a proxy to make requests to the API while the bot is deployed on Heroku.
proxyDict = {
    "http"  : os.environ.get('FIXIE_URL', ''),
    "https" : os.environ.get('FIXIE_URL', '')
}

class Clan:
    '''
    Clan class offers methods to fetch data related to the clan.
    '''
    url = 'https://api.clashofclans.com/v1/'
    clan_url = 'https://api.clashofclans.com/v1/clans/%23QOUUCYV2/'

    def get_war(self):
        '''Returns data related to the clan's current war.'''

        response = requests.get(self.clan_url + 'currentwar', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = ''
        if data['state'] == 'notInWar':
            to_ret = 'The DMND Life is not in a war right now.'
        else:
            to_ret += '```\nThe DMND Life is in a war vs. ' + data['opponent']['name'] + '.\n\n' + 'The DMND Life: ' + str(data['clan']['stars']) + ' stars, ' + str(data['clan']['attacks']) + ' attacks\n' + data['opponent']['name'] + ': ' + str(data['opponent']['stars']) + ' stars, ' + str(data['opponent']['attacks']) + ' attacks\n```'

        return to_ret

    def get_members(self):
        '''Returns a list of members in the clan.'''

        response = requests.get(self.clan_url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = ''
        for user in data['items']:
           to_ret += '\n' + user['name']

        return to_ret

    def get_random_member(self):
        '''Returns the name of a random member in the clan'''

        response = requests.get(self.clan_url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        member = random.choice(data['items'])

        return member['name'] + ' is moist.'

    def cwl_info(self):
        '''Returns info related to the Clan War League'''

        group_response = requests.get(self.clan_url + 'currentwar/leaguegroup', headers=headers, proxies=proxyDict)
        group_data = group_response.json()

        if group_data['state'] == 'inWar':
            state = 'In War\n'
        to_ret = state + 'Season: ' + str(group_data['season']) + '\n\n' + 'Clans: '
        for clan in group_data['clans']:
            to_ret += '\n -' + clan['name']

        return to_ret

    def cwl_clan_info(self, name):
        '''Returns info related to a clan in tbe Clan War League'''

        name = name.lower()
        response = requests.get(self.clan_url + 'currentwar/leaguegroup', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = ''
        for clan in data['clans']:
            if clan['name'].lower() == name:
                to_ret += (clan['name'] + '\n' + 'Level:' + str(clan['clanLevel']) + '\n\nMembers:')
                for member in clan['members']:
                    to_ret += '\n -' + member['name'] + ': ' 'TH' + str(member['townHallLevel'])

                return to_ret

        return 'Clan not in CWL'

    def get_member(self, name):
        '''Returns info related to a member in the clan'''

        name = name.lower()
        response = requests.get(self.clan_url + 'members', headers=headers, proxies=proxyDict)
        data = response.json()
        to_ret = {}
        for user in data['items']:
            if name == user['name'].lower():
                to_ret['name'] = user['name'] + ' - ' + user['role']
                to_ret['message'] = '**Trophies: ' + str(user['trophies']) + ' | Donated: ' + str(user['donations']) + ' | Received: ' + str(user['donationsReceived']) + '**'
                to_ret['image'] = user['league']['iconUrls']['medium']
                return to_ret

        return 'User not found in clan.'

    def clan_info(self):
        '''Returns info related to the clan'''

        response = requests.get(self.clan_url, headers=headers, proxies=proxyDict)
        data = response.json()

        to_ret = {}
        to_ret['image'] = data['badgeUrls']['medium']
        to_ret['name'] = data['name']
        to_ret['desc'] = data['description']
        to_ret['league'] = data['warLeague']['name']
        to_ret['level'] = data['clanLevel']
        to_ret['members'] = data['members']
        to_ret['member_list'] = self.get_members()

        return to_ret
