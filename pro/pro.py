#-*- coding: utf-8 -*-
#Copyrighted By SUSFRAN
#line://ti/p/~samurai.xx.
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


from linepy import *
import threading, time, sys
from humanfriendly import format_timespan, format_size, format_number, format_length
from manager import Manager
from loginqr.gen2 import login
cc = LINE(login(), appName="CHROMEOS\t2.1.4\tChrome_OS\t1")
mid = cc.profile.mid
admin = ["ua39ed072a0b4b0e68594bb9c74e8ed0d","u755e751c36bff4a7f21c84497b364b18"]
poll = OEPoll(cc)
manage = Manager(cc)
def Operate(op):
	if (op.type == 13 and mid in op.param3):
		if (len(cc.getGroup(op.param1).members) > 8):
			cc.acceptGroupInvitation(op.param1)
			cc.sendMentionV2(op.param1, "@! ขอบคุณที่เชิญเข้าคลับนะค๊า", [op.param2])
			if (op.param2 not in manage.user):
				manage.create_user(op.param2)
			manage.add_or_remove_ticket(op.param2, 0)
		else: return
	if (op.type == 19 and op.param3 in mid):
		if (op.param2 in manage.user):
			cc.sendMentionV2(op.param2, "@! คุณจะถูกลบตั๋ว 5 ใบเนื่องจากเตะบอทออกจากกลุ่ม", [op.param2])
			manage.add_or_remove_ticket(op.param2, -99999)
	if (op.type == 26):
		msg = op.message
		if (msg.contentType != 0): return
		to = msg.to if msg.toType != 0 else msg._from
		sender = msg._from
		mlow = msg.text.lower()
		isAuth = (sender in admin)
		if mlow.startswith("!"):
			if sender not in manage.user: manage.create_user(sender)
			if mlow == "!k":
				cc.sendMessage(to, "⊱•━━━━━.•°BOT°•.━━━━━•⊰\n\nพิมพ์ ! แล้วตามด้วยคำสั่งค๊า:\n- !k\n- !f (ดูตั๋วทั้งหมด)\n- !p (ข้อความ)\n- :ซื้อตั๋วได้จากแอคมิน\n\nคำสั่งสำหรับแอดมิน:\n!add\n\nติดต่อแอดมิน\n line://ti/p/~seou.k\n*กรุณาอย่าเตะบอทนะค๊า\n\n⊱•━━━━━.•°BOT°•.━━━━━•⊰")
			if mlow == "!f":
				name = cc.getContact(sender).displayName
				cc.sendMessage(to, f"ตั๋วของคุณคือ : {manage.user[sender]['ticket']}")
			if mlow.startswith("!add") and isAuth:
				day = msg.text.split(" ")[1]
				try: int(day)
				except: return False
				day = int(day)
				mention = [i["M"] for i in eval(msg.contentMetadata["MENTION"])["MENTIONEES"]]
				for m in mention:
					manage.create_user(m)
					manage.add_or_remove_ticket(m, day)
					cc.sendMentionV2(to, f"@! ถูกเพิ่ม จำนวน : {day} ใบ", [m])
			if mlow.startswith("!p"):
				text = msg.text.split("!p ")[1]
				groups = cc.getGroupIdsJoined()
				if not manage.user[sender]["ticket"] > 0:
					#if manage.user[sender]["paytime"] != None and manage.check_paid_promote(sender) != False: pass
					return cc.sendMessage(to, "คุณมีตั๋วไม่พอค๊าา กรุณาติดต่อแอดมิน\n http://line.me/ti/p/~seou.k")
				if manage.check_cooldown(sender) != False:
					return cc.sendMessage(to, f"คุณยังเหลือคูลดาวน์อีก {manage.check_cooldown(sender)} นาที")
				manage.add_or_remove_ticket(sender, -1)
				manage.promote(sender, text)
				cc.sendMessage(to, "โปรเสร็จแล้วทั้งหมด {} คลับ ".format(str(len(groups))))
				cc.sendMessage(to, f"ตั๋วของคุณเหลือ : {manage.user[sender]['ticket']} ใบค่ะ")
			if mlow.startswith(":exec\n") and isAuth:
				try: exec(msg.text.split(":exec\n")[1])
				except Exception as error: cc.sendMessage(to, str(error))
def run():
	while True:
		try: ops = poll.singleTrace(count=50)
		except EOFError: return
		except KeyboardInterrupt: sys.exit()
		try:
			for op in ops:
				poll.setRevision(op.revision)
				Operate(op)
		except Exception as e: print(e)
		except KeyboardInterrupt: sys.exit()
if __name__ == "__main__":
	run()
