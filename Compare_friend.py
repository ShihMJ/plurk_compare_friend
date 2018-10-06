from plurk_oauth import PlurkAPI
import re

import json

class Compare_list:
	def __init__(self, file_name, my_account):
		self.file_name = file_name
		self.my_account = my_account
		self.deleted_friend = []
		self.friend_list_now = []
		# replace them with your consumer key and secret
		CONSUMER_KEY = YOUR_CONSUMER_KEY
		CONSUMER_SECRET = YOUR_CONSUMER_SECRET
		self.plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)

	def open_file(self):
		FILE = open(self.file_name, 'r', encoding = 'utf-8')
		friend_list_str = FILE.read()
		temp = friend_list_str.split('\n')
		self.friend_list = []
		for s in temp :
			# separate to ID NICK_NAME DISPLAY_NAME. Do this in case that there is a space in DISPLAY_NAME
			s = s.split(' ', 2)
			self.friend_list.extend(s)

	def get_friend_now(self):
		self.open_file()
		self.my_info_json = self.plurk.callAPI('/APP/Profile/getPublicProfile', options = {'user_id' : self.my_account})
		if self.my_info_json :
			friends_count = self.my_info_json['friends_count']
			my_id = self.my_info_json['user_info']['uid']
			# getFriendsByOffset can only get 100 friends every time
			for offset in range(0, friends_count + 100, 100):
				my_friend = self.plurk.callAPI('/APP/FriendsFans/getFriendsByOffset', options={'user_id': my_id, 'offset' : offset, 'limit' : 100})
				for friend_json in my_friend:
					self.friend_list_now.append(str(friend_json['id']))
		
	def compare_friend(self):
		self.get_friend_now()
		if self.my_info_json :
			i = 0
			while True :
				# a deleted friend. get its NICK_NAME and DISPLAY_NAME
				if self.friend_list[i] not in self.friend_list_now :
					self.deleted_friend.append(self.friend_list[i + 1])
					self.deleted_friend.append(self.friend_list[i + 2])
				i += 3
				if i >= len(self.friend_list) :
					break
			if self.deleted_friend :
				i = 0
				while True :
					# join NICK_NAME and DISPLAY_NAME and separate them with '(', and then append a ')' to the end
					# NICK_NAME(DISPLAY_NAME)
					self.deleted_friend[i:i+2] = ['('.join(self.deleted_friend[i:i+2])]
					self.deleted_friend[i] += ')'
					i += 1
					if i >= len(self.deleted_friend) :
						break
			return True
		else :
			return False