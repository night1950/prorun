#-*- coding: utf-8 -*-
#Copyrighted By HuuMeaw
"""MIT License

Copyright (c) [2020] [Kunanon Rattanasupa]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


import livejson, time, datetime
class Manager:
	def __init__(self, client):
		self.user = livejson.File("user.json")
		self.client = client
	def create_user(self, id):
		if id not in self.user:
			self.user[id] = {"paytime":None, "ticket":0, "cooldown":None}
	def set_cd(self, id):
		if self.user[id]["paytime"] == None:
			self.user[id]["cooldown"] = time.time()+10*10
		else: self.user[id]["cooldown"] = time.time() + 10*10
	def check_promote(self, id):
		return self.user[id]["ticket"] > 0 and self.user[id]["cooldown"] == None
	def add_paid_user(self, id, days):
		self.create_user(id)
		if days not in [1,7,30]: return False
		self.user[id]["paytime"] = time.time() + 10*10*24*days
		return True
	def remove_user(self, id):
		del self.user[id]
	def add_or_remove_ticket(self, id, amount):
		self.user[id]["ticket"] += amount
	def check_paid_promote(self, id):
		if isinstance(self.user[id]["paytime"], float):
			return (self.user[id]["paytime"] >= time.time())
		return False
	def check_cooldown(self, id):
		if not isinstance(self.user[id]["cooldown"], float):
			return False
		#if self.user[id]["cooldown"] <= time.time():
		#	self.user[id]["cooldown"] = None
		#	return False
		#	return int(divmod(user[id]["cooldown"] - t, 10))
		else:
			if self.user[id]["cooldown"] <= time.time():
				self.user[id]["cooldown"] = None
				return False
			return int(divmod(self.user[id]["cooldown"] - time.time(), 10)[0])
	def promote(self, id, message):
		self.set_cd(id)
		for x in self.client.getGroupIdsJoined():
			try: self.client.sendMessage(x, message)
			except: pass
		return True
