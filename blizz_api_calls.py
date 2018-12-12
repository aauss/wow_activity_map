import json
import requests
import pickle

'''Blizzard API calls to retrieve realm names and timezone (US)/locale (EU) to later match the realm activity to
its correct location on the activity map'''

request = requests.get("https://us.api.blizzard.com/wow/realm/status?locale=en_US&access_token=\
                        US42MIyf36fGanr2BLbxvBmxxnbM5MB3Dy")
blizz_realms_us = json.loads(request.content.decode('utf-8'))
pickle.dump(blizz_realms_us, open('blizz_realms_us.p', 'wb'))


request2 = requests.get("https://eu.api.blizzard.com/wow/realm/status?access_token=US42MIyf36fGanr2BLbxvBmxxnbM5MB3Dy")
blizz_realms_eu = json.loads(request2.content.decode('utf-8'))
pickle.dump(blizz_realms_eu, open('blizz_realms_eu.p', 'wb'))
