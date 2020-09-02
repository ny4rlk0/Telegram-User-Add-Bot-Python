import os, sys, time, csv,traceback, random, re
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import AddContactRequest,GetContactsRequest
from telethon.tl.functions.messages import GetDialogsRequest,AddChatUserRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserKickedError
from telethon.tl.functions.channels import InviteToChannelRequest,JoinChannelRequest,LeaveChannelRequest
import configparser as c
from sys import argv
from datetime import datetime

def e():
	try:
		r = c.RawConfigParser() #Read Group Keys
		r.read('degerler.veri')
		cfg = r['veri'] ['config_no']
		group_username = r['veri'] ['kanal_grup_adi']
		ags = r['veri'] ['aktif_gun_sayisi']
		bsk = r['veri'] ['beklenicek_sure_kucuk']
		bsb = r['veri'] ['beklenicek_sure_buyuk']
		intags = int(ags)
		intbsk = int(bsk)
		intbsb = int(bsb)
		cpass = c.RawConfigParser()
		cpass.read(cfg)
	except:
		print("Something is wrong with degerler.veri!!")
	try:
		id = cpass['cred']['id']
		h = cpass['cred']['hash']
		p = cpass['cred']['phone']
		client = TelegramClient(p, id, h)
	except KeyError:
		print("[!] Api access id phone or hash is not correct!!\n")
		sys.exit(1)
	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(p)
		client.sign_in(p, input('[+] Enter code sent from telegram : '))
	client(JoinChannelRequest(channel=group_username))
	chats = []
	last_date = None
	chunk_size = 200
	groups=[]
	result = client(GetDialogsRequest(
				offset_date=last_date,
				offset_id=0,
				offset_peer=InputPeerEmpty(),
				limit=chunk_size,
				hash = 0
			))
	chats.extend(result.chats)
	for chat in chats:
		try:
			check=client.get_entity(group_username)
			if check.id==chat.id:
				groups.append(chat)
		except:
			continue
	i=0
	for group in groups:
		print('['+str(i)+']' '-'+ group.title)
		i+=1
	g_index =0
	aktif_gun_sayisi = intags
	target_group=groups[int(g_index)]
	all_participants=[]
	time.sleep(random.randrange(11,23))
	all_participants= client.get_participants(target_group)#patched because telegram seems to ban while using it! , aggressive=True)
	with open("users.nya","w",encoding='UTF-8') as f:
		writer = csv.writer(f,delimiter=",",lineterminator="\n")
		writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
		for user in all_participants:
			#contacts = client(GetContactsRequest(0))
			#client(AddChatUserRequest(chat_id=chat.id,user_id=user.id,fwd_limit=10))
			accept=True
			try:
				lastDate=user.status.was_online
				ay_kontrolu= (datetime.now().month-lastDate.month)
				gun_kontrolu= (datetime.now().day-lastDate.day)
				if(ay_kontrolu>0 or gun_kontrolu>aktif_gun_sayisi or datetime.now().year!=lastDate.year):
					accept=False
			except:
				pass
			if (accept):
				if user.username:
					username= user.username
				else:
					username= ""
				if user.first_name:
					first_name= user.first_name
				else:
					first_name= ""
				if user.last_name:
					last_name= user.last_name
				else:
					last_name= ""
				name= (first_name + ' ' + last_name).strip()
				writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
	client(LeaveChannelRequest(channel=group_username))
	os._exit(1)
e()