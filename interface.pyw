from tkinter import *
import configparser as c
import os
import sys
import pathlib as p
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import requests
import traceback
import random
import re
from os import remove
from sys import argv
from datetime import datetime
import pathlib as p

window = Tk()
window.title("Telegram Tool @nyarlko")
window.configure(background="black")

durum = "Beklemede"
def gruba_ekle():
	tekrar()
	durum="Adding to group channel"
	Label (window, text="Durum: "+durum+"." ,bg="black",fg="white",font="none 12 bold") .grid(row=8,column=0,sticky=W)
	os.system('start add')

def dosya_kaydet():
	tekrar()
	durum="Saving the file"
	Label (window, text="Durum: "+durum+"." ,bg="black",fg="white",font="none 12 bold") .grid(row=8,column=0,sticky=W)
	os.system('start save')

def tekrar():
	i=t.get() #Configno
	i1=t1.get() #Satirno
	i2=t2.get() #Eklenicek_kisi_sayisi
	i3=t3.get() #Grup_Kanal_Adi
	i4=t4.get() #Kullanici_Aktif_Gun_Sayisi
	i5=t5.get() #Beklenicek_Sure_Kucuk
	i6=t6.get() #Beklenicek_Sure_Buyuk
	cp = c.RawConfigParser()
	cp.add_section('veri')
	cno =str(i) #Configno
	cp.set('veri', 'config_no', cno)
	sno =str(i1) #Satirno
	cp.set('veri', 'satir_no', sno)
	kno =str(i2) #Eklenicek_kisi_sayisi
	cp.set('veri', 'kisi_sayisi', kno)
	kadi =str(i3) #Grup_Kanal_Adi
	cp.set('veri', 'kanal_grup_adi', kadi)
	ags =str(i4) #Kullanici_Aktif_Gun_Sayisi
	cp.set('veri', 'aktif_gun_sayisi', ags)
	bsk =str(i5) #Beklenicek_Sure_Kucuk
	cp.set('veri', 'beklenicek_sure_kucuk', bsk)
	bsb =str(i6) #Beklenicek_Sure_Buyuk
	cp.set('veri', 'beklenicek_sure_buyuk', bsb)
	setup = open('degerler.veri', 'w')
	cp.write(setup)
	setup.close()

#ConfigBox
Label (window, text="Config name:" ,bg="black",fg="white",font="none 12 bold") .grid(row=0,column=0,sticky=W)
t=Entry(window,width=20,bg="white")
t.insert(0, "config1.data")
t.grid(row=0,column=1,sticky=W)
#SatirBox
Label (window, text="Line to start:" ,bg="black",fg="white",font="none 12 bold") .grid(row=1,column=0,sticky=W)
t1=Entry(window,width=20,bg="white")
t1.insert(0, "1")
t1.grid(row=1,column=1,sticky=W)
#KisiBox
Label (window, text="How many to add:" ,bg="black",fg="white",font="none 12 bold") .grid(row=2,column=0,sticky=W)
t2=Entry(window,width=20,bg="white")
t2.insert(0, "15")
t2.grid(row=2,column=1,sticky=W)
#GrupKanalAdiBox
Label (window, text="Group/Channel username:" ,bg="black",fg="white",font="none 12 bold") .grid(row=3,column=0,sticky=W)
t3=Entry(window,width=20,bg="white")
t3.insert(0, "animenx")
t3.grid(row=3,column=1,sticky=W)
#AktifgunsayisiBox
Label (window, text="Active day number(max 28):" ,bg="black",fg="white",font="none 12 bold") .grid(row=4,column=0,sticky=W)
t4=Entry(window,width=20,bg="white")
t4.insert(0, "3")
t4.grid(row=4,column=1,sticky=W)
#BeklenicekZamanBox
Label (window, text="Time to wait (small):" ,bg="black",fg="white",font="none 12 bold") .grid(row=5,column=0,sticky=W)
t5=Entry(window,width=20,bg="white")
t5.insert(0, "31")
t5.grid(row=5,column=1,sticky=W)
#BeklenicekZaman2Box
Label (window, text="Time to wait (Big):" ,bg="black",fg="white",font="none 12 bold") .grid(row=6,column=0,sticky=W)
t6=Entry(window,width=20,bg="white")
t6.insert(0, "83")
t6.grid(row=6,column=1,sticky=W)

#GrubaEkleButton
Button(window,text="Add",width=12,font="none 12 bold",command=gruba_ekle) .grid(row=7,column=0,sticky=W)
#DosyaKaydetButton
Button(window,text="Save",width=12,font="none 12 bold",command=dosya_kaydet) .grid(row=7,column=1,sticky=W)
#Durum
Label (window, text="Status: "+durum+"." ,bg="black",fg="white",font="none 12 bold") .grid(row=8,column=0,sticky=W)
#Run the main loop
window.mainloop()
