#!/usr/bin/env python3
# -*- coding: utf-8 -*-

global proxytype
proxytype = {}
from tqdm import tqdm
import os, requests, socket, socks, time, random, threading, sys, ssl, datetime, cfscrape, re
from time import sleep
global out_file
out_file = "proxy.txt"

def checking(lines, socks_type, ms):
    global proxytype
    global nums, proxies
    proxy = lines.strip().split(":")
    if len(proxy) != 2:
        proxies.remove(lines)
        return
    err = 0
    num = 0
    while True:
        if err == 3:
            proxies.remove(lines)
            break
        try:
            num += 1
            s = socks.socksocket()
            if num == 1:
                s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
                ptype = "4"
                proxytype[proxy[0]+":"+proxy[1]] = 4
            if num == 2:
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
                ptype = "5"
                proxytype[proxy[0]+":"+proxy[1]] = 5
            if num == 3:
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                ptype = "1"
                proxytype[proxy[0]+":"+proxy[1]] = 1
            s.settimeout(ms)
            s.connect((str("172.104.90.60"), int(80)))
            s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            s.close()
            break
        except:
            err += 1
    nums += 1


nums = 0


def check_socks(ms):
    global nums
    thread_list = []
    print("スレッドを開始中...")
    for lines in tqdm(list(proxies)):
        th = threading.Thread(target=checking, args=(lines, 1, ms,))
        th.start()
        thread_list.append(th)
        time.sleep(0.0001)
#        while len(threading.enumerate()) >= max_thread+1:time.sleep(1)
    print("完了\nプロキシの確認を完了中...")
    for th in tqdm(list(thread_list)):
        try:th.join()
        except:pass
    print("完了")
    print("書き込み中...",end='')
    ans = "y"
    if ans == "y" or ans == "":
        if "4" == "4":
            try:os.mkdir("check-results")
            except:pass
            with open("check-results/socks4.txt", 'wb') as fp:
                for lines in list(proxies):
                    if proxytype[lines.replace("\n","")] == 4:
                        fp.write(bytes(lines, encoding='utf8'))
            fp.close()
            with open("check-results/socks5.txt", 'wb') as fp:
                for lines in list(proxies):
                    if proxytype[lines.replace("\n","")] == 5:
                        fp.write(bytes(lines, encoding='utf8'))
            fp.close()
            with open("check-results/http.txt", 'wb') as fp:
                for lines in list(proxies):
                    if proxytype[lines.replace("\n","")] == 1:
                        fp.write(bytes(lines, encoding='utf8'))
            fp.close()
            with open("check-results/mix.txt", 'wb') as fp:
                for lines in list(proxies):
                    if proxytype[lines.replace("\n","")] == 1:out_type = "http"
                    if proxytype[lines.replace("\n","")] == 4:out_type = "socks4"
                    if proxytype[lines.replace("\n","")] == 5:out_type = "socks5"
                    fp.write(bytes(out_type+"://"+lines.replace("\n","")+"/\n", encoding='utf8'))
            fp.close()
    print("完了\ncheck-resultsフォルダー内の、http.txt socks4.txt socks5.txtに保存しました。")


def check_list(socks_file):
    temp = open(socks_file).readlines()
    temp_list = []
    print("処理中(1/2)")
    for i in tqdm(temp):
        if i not in temp_list:
            if ':' in i:
                temp_list.append(i)
    rfile = open(socks_file, "wb")
    print("処理中(2/2)")
    for i in tqdm(list(temp_list)):
        rfile.write(bytes(i, encoding='utf-8'))
    rfile.close()


def downloadsocks(choice):
    global out_file
    if "4" == "4":
        f = open(out_file, 'wb')
        try:
            r = requests.get("https://midokuriserver.com/proxytool/",timeout=500)
            f.write(r.content)
        except:
            pass


def proxydl(out_file, socks_type):
    global proxies, multiple, choice, data
    ms = 5
    if socks_type == 1:
        socktyper = "HTTP"
    if socks_type == 4:
        socktyper = "SOCKS4"
    if socks_type == 5:
        socktyper = "SOCKS5"

    print("プロキシをダウンロードしています...")
    start = time.time()
    downloadsocks(1)
    end = time.time() - start
    print(" 完了("+str(end)+"秒)")
    proxies = open(str(out_file)).readlines()
    check_list(out_file)
    check_socks(ms)

proxydl(out_file,1)
