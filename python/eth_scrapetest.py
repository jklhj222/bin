#!/usr/bin/env python3
# https://morvanzhou.github.io/tutorials/data-manipulation/scraping/2-01-beautifulsoup-basic/
""" Created on Sun Aug 12 13:58:48 2018@author: jklhj """

from bs4 import BeautifulSoup
import requests
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('ETH Exchange Rate')
window.geometry('250x170')
window.configure(background='darkblue')


rate = tk.StringVar()
rate.set('original')

NTD = tk.StringVar()
NTD.set('original')

Diff = tk.StringVar()
Diff.set('original')

Time = tk.StringVar()
Time.set('original')

fontStyle = tkFont.Font(family="Lucida Grande", size=20)

l_rate = tk.Label(window, textvariable=rate, bg='darkblue', fg='white', font=fontStyle)
l_rate.pack()

l_NTD = tk.Label(window, textvariable=NTD, bg='darkblue', fg='white', font=fontStyle)
l_NTD.pack()

l_Diff = tk.Label(window, textvariable=Diff, bg='darkblue', fg='white', font=fontStyle)
l_Diff.pack()

l_Time = tk.Label(window, textvariable=Time, bg='darkblue', fg='white', font=fontStyle)
l_Time.pack()

tot_eth = 18.5891

value_list = [None] * 10

# if has Chinese, apply decode()


count = 0
tmp_eth_rate = 0
while True:
#    eth_page = requests.get('https://finance.yahoo.com/quote/ETH-USD').text
#    eth_page = requests.get('https://www.coingecko.com/zh-tw/%E6%95%B8%E5%AD%97%E8%B2%A8%E5%B9%A3/%E4%BB%A5%E5%A4%AA%E5%B9%A3').text

    eth_page = requests.get('https://www.coingecko.com/en/coins/ethereum').text
    usd_page = requests.get('https://rate.bot.com.tw/xrt?Lang=zh-TW').text

    eth_soup = BeautifulSoup(eth_page, 'lxml')
    usd_soup = BeautifulSoup(usd_page, 'lxml')

#    print(eth_soup.prettify())
    eth_price = eth_soup.find_all('span')
    for i in eth_price:
        if i.get('data-price-json') is not None:
            price_json = i.get('data-price-json')
            eth2twd = eval(price_json)['twd']
            break

        else:
            continue

    print()
#    print('eth_price', eth_price, len(eth_price))

#    print()

    time.sleep(1)

    eth_rate = int(eth2twd-75)
    tot_twd = int(eth_rate * tot_eth)

    print('eth2twd: ', eth2twd)
    print('eth_rate: ', eth_rate)
    print(value_list)
    print('count: ', count)

    if tmp_eth_rate != eth_rate:
        value_list[count] = (eth_rate, time.time())

        if count == 9:
            count = 0
        else:
            count += 1


        if value_list[1] is not None:
            if value_list[-1] is None:
                value_diff = eth_rate - value_list[0][0]
                time_diff = int(time.time() - value_list[0][1])
 
            else:
                value_diff = eth_rate - value_list[count][0]
                time_diff = int(time.time() - value_list[count][1])
 
        else:
            value_diff = 0 
            time_diff = 0
 

        tmp_eth_rate = eth_rate
 
        rate.set(f'Rate: {eth_rate:,}')
        NTD.set(f'NTD: {tot_twd:,}')
        Diff.set(f'Diff: {value_diff:,}')
        Time.set(f'Time Diff: {time_diff} s')
 
        window.update_idletasks()
    

