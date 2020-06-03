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

    def get_member(self, name):
        response = requests.get(self.url + 'members', headers=headers)
        data = response.json()
        for user in data['items']:
            if name == user['name']:
                to_ret = user['name'] + '\n' + user['role'] + '\n' + 'Trophies: ' + str(user['trophies']) + ',  Donated: ' + str(user['donations']) + ', Received: ' + str(user['donationsReceived'])
                return to_ret
        return 'User not found in clan.'
