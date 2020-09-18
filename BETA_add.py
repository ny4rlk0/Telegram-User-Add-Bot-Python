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
	nya = c.RawConfigParser() #Instance desu
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
		client.sign_in(p, input('[+] Enter the code sent from telegram : '))
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
	global max_user_to_add_x,max_user_to_add
	max_user_to_add=0
	max_user_to_add_x=0
	for user in users:
			try:
				if max_user_to_add==15:#intkissay:
					client(LeaveChannelRequest(channel=group_username))
					change_config()
					b()
				if mode == 1:
					if user['username'] == "":
						max_user_to_add_x+=1
						continue
					print (f"{p} Adding user {user['id']}")
					max_user_to_add+=1
					max_user_to_add_x+=1
					user_to_add = client.get_input_entity(user['username'])
				#elif mode == 2:
				#	user_to_add = InputPeerUser(user['id'], user['access_hash'])
				client(InviteToChannelRequest(target_group_entity,[user_to_add]))
				print(f"[+] Waiting random time {intbsk} - {intbsb} as seconds.")
				time.sleep(random.randrange(intbsk,intbsb))
			except:
				max_user_to_add-=1
				max_user_to_add_x+=1
				traceback.print_exc()
				print(f"[+] Waiting random time 11 - 23 as seconds.")
				time.sleep(random.randrange(11,23))
				continue
def change_config():#kickoff when you add 15 user to protecc ur acc's desu
	nya = c.RawConfigParser() #instance desu
	nya.read('degerler.veri') #read the file desu
	cfg = nya['veri'] ['config_no']
	satir_no = nya['veri'] ['satir_no']
	satir_no=int(satir_no) #convert to integer for math desu
	satir_no+=max_user_to_add_x#Lets save which line we left desu
	cfg_old=cfg#remember old cfg name incase i need to use desu
	cfg=cfg.split("g")#parse the text so we can up number by one desu
	cfg=cfg[1]#same desu
	cfg=cfg.split(".")#same desu
	cfg=int(cfg[0])#cfg number desu
	cfg+=1#change conf by adding  +1 number desu
	cfg=str(cfg)#change to string desu
	cfg=f"config{cfg}.data" #create new config name desu
	cp=c.RawConfigParser()
	cp.read('degerler.veri')
	cp.set('veri', 'config_no', cfg)
	cp.set('veri', 'satir_no', satir_no)
	setup = open('degerler.veri', 'w') #open the degerler.veri desu
	cp.write(setup) #write to degerler.veri desu
	setup.close() #close the file desu
	max_user_to_add=0 #reset users to add to zero desu
	max_user_to_add_x=0
b()
