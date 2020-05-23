import os, sys
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import requests
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserKickedError
from telethon.tl.functions.channels import InviteToChannelRequest,JoinChannelRequest,LeaveChannelRequest
import configparser as c
import csv
import traceback
import random
import re
from os import remove
from sys import argv
from datetime import datetime
import pathlib as p

def dogrula():
#	try:
#		r=urlopen('https://github.com/ny4rlk0/x275/blob/master/run') #explained this on other file.
#		soup=BeautifulSoup(r,'html.parser')
#		x=soup.find(id='LC1')
#		t = x.get_text()
#		if int(t)==1:
 fl=p.Path("interface.exe")
 fl2=p.Path("add.py")
 fl3=p.Path("save.py")
 if fl.exists and fl2.exists and fl3.exists():
  kaydet() #Scripti başlat
 else:
  os._exit(1)
#		elif int(t)==0: #Scripti sil
#			os.remove("config.data")
#			os.remove("grup_uyeleri.csv")
#			os.remove("ekle.exe")
#			remove (argv[0])
#		else: #Scriptin çalışmasını durdur
#			os._exit(1)
#	except:
#	 os._exit(1)

def kaydet():
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
		os.system('cls')
		print("[!] Gereklilikler yuklu degil. !!\n")
		sys.exit(1)
	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(phone)
		client.sign_in(phone, input('[+] Telegramdan gelen kodu gir : '))
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
	all_participants= client.get_participants(target_group, aggressive=True)
	with open("grup_uyeleri.csv","w",encoding='UTF-8') as f:
		writer = csv.writer(f,delimiter=",",lineterminator="\n")
		writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
		for user in all_participants:
			accept=True
			try:
				lastDate=user.status.was_online
				ay_kontrolu= (datetime.now().month-lastDate.month)
				gun_kontrolu= (datetime.now().day-lastDate.day)
				if(ay_kontrolu>0 or gun_kontrolu>aktif_gun_sayisi or datetime.now().year!=lastDate.year):
					accept=False
			except:
				continue
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

dogrula()
