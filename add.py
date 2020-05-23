import os, sys
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest,AddChatUserRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserKickedError
from telethon.tl.functions.channels import InviteToChannelRequest,JoinChannelRequest,LeaveChannelRequest
import configparser as c
import csv
import traceback
import random
from itertools import islice
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import requests
import re
from os import remove
from sys import argv
from datetime import datetime
import pathlib as p

def dogrula():
#	try:
#		r=urlopen('https://github.com/ny4rlk0/x275/blob/master/run') #Lil extra for protection remote wipe etc. removed since im sharing the source.
#		soup=BeautifulSoup(r,'html.parser')
#		x=soup.find(id='LC1')
#		t = x.get_text()
#		if int(t)==1:
 fl=p.Path("interface.pyw")
 fl2=p.Path("add.py")
 fl3=p.Path("save.py")
 if fl.exists and fl2.exists and fl3.exists():
  ekle() #Scripti başlat
 else:
  os._exit(1)
#		elif int(t)==0: #Scripti sil
#			os.remove("config.data")
#			os.remove("grup_uyeleri.csv")
#			os.remove("kaydet.exe")
#			remove (argv[0])
#		else: #Scriptin çalışmasını durdur
#			os._exit(1)
#	except:
#	 os._exit(1)

def ekle():
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
		api_id = cpass['cred']['id']
		api_hash = cpass['cred']['hash']
		phone = cpass['cred']['phone']
		client = TelegramClient(phone, api_id, api_hash)
	except KeyError:
		sys.exit(1)
	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(phone)
		os.system('cls')
		client.sign_in(phone, input('[+] Telegrama gelen kodu gir : '))
	client(JoinChannelRequest(channel=group_username))
	os.system('cls')
	users = []
	with open("grup_uyeleri.csv","r", encoding='UTF-8') as fd:
		rows = csv.reader(fd,delimiter=",",lineterminator="\n")
		for row in islice(csv.reader(fd),intsatno,None):
			user = {}
			user['username'] = row[0]
			user['id'] = int(row[1])
			user['access_hash'] = int(row[2])
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
				max_user_to_add+=1
				if max_user_to_add==intkissay:
					client(LeaveChannelRequest(channel=group_username))
					os._exit(1)
				print (phone+" Kullanici ekleniyor {}".format(user['id']))
				if mode == 1:
					if user['username'] == "":
						continue
					user_to_add = client.get_input_entity(user['username'])
				elif mode == 2:
					user_to_add = InputPeerUser(user['id'], user['access_hash'])
				else:
					sys.exit("[!] Gecersiz secenek secildi. Tekrar dene.")
				try:
					client(InviteToChannelRequest(target_group_entity,[user_to_add]))
					print("[+] Rastgele "+intbsk+" ila "+intbsb+" sn bekleniyor.")
					time.sleep(random.randrange(intbsk,intbsb))
				except:
					traceback.print_exc()
					print("[+] HATA Rastgele 11 ila 23 sn bekleniyor.")
					time.sleep(random.randrange(11,23))
					continue
			except PeerFloodError:
				print("[!] Telegrama fazla istek attigimiz icin hatayla karsilastik. Bot Durduruldu.")
				while(True):
					time.sleep(random.randrange(11,23))
			except UserPrivacyRestrictedError:
				print("[!] Kullanicinin gizlilik ayarlari yuzunden eklenemedi. Atlaniyor.")
				time.sleep(random.randrange(11,23))
				max_user_to_add-=1
			except UserNotMutualContactError:
				print("[!] User not mutual contact hatasi alindi. Devam ediliyor.")
				time.sleep(random.randrange(12,22))
				max_user_to_add-=1
			except UserKickedError:
				print("[!] Bu kullanici bu grupdan daha once atilmis. Atlaniyor.")
				time.sleep(random.randrange(9,21))
				max_user_to_add-=1
			except:
				traceback.print_exc()
				print("[!] Beklenmeyen Hata")
				time.sleep(random.randrange(14,25))
				max_user_to_add-=1
				continue
dogrula()
