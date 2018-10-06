from plurk_oauth import PlurkAPI
from datetime import datetime
import json

class make_friend_file:
	def __init__(self, my_account):
		self.my_account = my_account
		self.friend_list_now = []
		self.my_info_json = {}
		# replace them with your consumer key and secret
		CONSUMER_KEY = YOUR_CONSUMER_KEY
		CONSUMER_SECRET = YOUR_CONSUMER_SECRET
		self.plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)

	def get_friend(self):
		self.my_info_json = self.plurk.callAPI('/APP/Profile/getPublicProfile', options = {'user_id' : self.my_account})
		if self.my_info_json :
			friends_count = self.my_info_json['friends_count']
			# uid instead of id, quite strange :p
			self.my_id = self.my_info_json['user_info']['uid']
			# getFriendsByOffset can only get 100 friends every time
			for offset in range(0, friends_count + 100, 100):
				my_friend = self.plurk.callAPI('/APP/FriendsFans/getFriendsByOffset', options={'user_id': self.my_id, 'offset' : offset, 'limit' : 100})
				for friend_json in my_friend:
					self.friend_list_now.append(str(friend_json['id']))
					self.friend_list_now.append(friend_json['nick_name'])
					self.friend_list_now.append(friend_json['display_name'])
			threelines = range(0, len(self.friend_list_now), 3)
			friend_list_str = ""
			for i, s in enumerate(self.friend_list_now) :
				if i in threelines :
					if friend_list_str :
						friend_list_str += '\n'
					# every line has format: ID NICK_NAME DISPLAY_NAME
					friend_list_str += " ".join(self.friend_list_now[i:i+3])
			today = datetime.today()
			FILE = open(str(self.my_account) + '_friend_list_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.txt'  , 'w+', encoding = 'utf-8')
			FILE.write(friend_list_str)