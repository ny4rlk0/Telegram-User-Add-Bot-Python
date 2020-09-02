import os, sys, time, csv, traceback, random
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import AddContactRequest
from telethon.tl.functions.messages import GetDialogsRequest,AddChatUserRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserKickedError
from telethon.tl.functions.channels import InviteToChannelRequest,JoinChannelRequest,LeaveChannelRequest
import configparser as c
from itertools import islice

def b():
	nya = c.RawConfigParser() #Grup keylerini oku
	nya.read('degerler.veri')
	cfg = nya['veri'] ['config_no']
	satno = nya['veri'] ['satir_no']
	kissay = nya['veri'] ['kisi_sayisi']
	group_username = nya['veri'] ['kanal_grup_adi']
	ags = nya['veri'] ['aktif_gun_sayisi']
	bsk = nya['veri'] ['beklenicek_sure_kucuk']
	bsb = nya['veri'] ['beklenicek_sure_buyuk']
	intsatno = int(satno)
	intkissay = int(kissay)
	intags = int(ags)
	intbsk = int(bsk)
	intbsb = int(bsb)
	cpass = c.RawConfigParser()
	cpass.read(cfg)
	try:
		id = cpass['cred']['id']
		h = cpass['cred']['hash']
		p = cpass['cred']['phone']
		client = TelegramClient(p, id, h)
	except KeyError:
		os.system('cls')
		print("[!] Somethings wrong with api id password hash or phone!!\n")
		sys.exit(1)
	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(p)
		os.system('cls')
		client.sign_in(p, input('[+] Telegrama gelen kodu gir : '))
	client(JoinChannelRequest(channel=group_username))
	os.system('cls')
	users = []
	with open("users.nya","r", encoding='UTF-8') as fd:
		rows = csv.reader(fd,delimiter=",",lineterminator="\n")
		for row in islice(csv.reader(fd),intsatno,None):
			user = {}
			user['username'] = row[0]
			user['id'] = row[1]
			user['access_hash'] = row[2]
			user['name'] = row[3]
			users.append(user)
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
		print('['+str(i)+']' '-' +group.title)
		i+=1
	g_index=0
	target_group=groups[int(g_index)]
	target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
	mode=1
	max_user_to_add=0
	for user in users:
			try:
				if max_user_to_add==intkissay:
					client(LeaveChannelRequest(channel=group_username))
					os._exit(1)
				if mode == 1:
					if user['username'] == "":
						continue
					print (f"{p} Adding user {user['id']}")
					max_user_to_add+=1
					user_to_add = client.get_input_entity(user['username'])
				elif mode == 2:
					user_to_add = InputPeerUser(user['id'], user['access_hash'])
				client(InviteToChannelRequest(target_group_entity,[user_to_add]))
				print(f"[+] Waiting random time {intbsk} - {intbsb} as seconds.")
				time.sleep(random.randrange(intbsk,intbsb))
			except:
				max_user_to_add-=1
				traceback.print_exc()
				print(f"[+] Waiting random time 11 - 23 as seconds.")
				time.sleep(random.randrange(11,23))
				continue
b()
