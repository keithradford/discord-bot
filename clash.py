import requests
import os

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer ' + os.environ.get('CLASH_KEY')
}

class Clan:
    url = 'https://api.clashofclans.com/v1/clans/%23QOUUCYV2/'

    def get_members(self):
        response = requests.get(self.url + 'members', headers=headers)
        data = response.json()
        for user in data['items']:
            print(user['name'])

    def cwl_info(self):
        response = requests.get(self.url + 'currentwar/leaguegroup', headers=headers)
        data = response.json()
        if data['state'] == 'inWar':
            state = 'In War\n'
        to_ret = '```\n' + state + 'Season: ' + str(data['season']) + '\n\n' + 'Clans: '
        for clan in data['clans']:
            to_ret += '\n -' + clan['name']

        to_ret += '\n```'
        return to_ret

    def cwl_clan_info(self, name):
        response = requests.get(self.url + 'currentwar/leaguegroup', headers=headers)
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
        response = requests.get(self.url + 'members', headers=headers)
        data = response.json()
        for user in data['items']:
            if name == user['name']:
                to_ret = user['name'] + '\n' + user['role'] + '\n' + 'Trophies: ' + str(user['trophies']) + ',  Donated: ' + str(user['donations']) + ', Received: ' + str(user['donationsReceived'])
                return to_ret
        return 'User not found in clan.'
