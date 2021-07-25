#!/usr/bin/env python3
# -*- coding: utf-8 -*-

global proxytype
proxytype = {}
try:
    from tqdm import tqdm
    import os, requests, socket, socks, time, random, threading, sys, datetime, re
except:
    print("必要なモジュールがインストールされていません。\nなので今から勝手にインストールします")
    os.system("python3 -m pip install requests pysocks tqdm")
    os.system("python -m pip install requests pysocks tqdm")
    try:
        from tqdm import tqdm
        import os, requests, socket, socks, time, random, threading, sys, datetime, re
    except:
        print("はい、もうこの自動化されたスクリプトがやれるのはここまでです。\nもう無理なので手動でやってください！\nコマンド: pip3 install requests pysocks tqdm")

max_thread = int(input("最大スレッド数どうする?(おすすめは500、制限なくすには0): "))

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
    print("スレッドを開始中なう...")
    for lines in tqdm(list(proxies)):
        th = threading.Thread(target=checking, args=(lines, 1, ms,))
        th.start()
        thread_list.append(th)
        time.sleep(0.0001)
        while (len(threading.enumerate()) >= max_thread+1) and max_thread != 0:time.sleep(1)
    print("完了\nプロキシの確認を完了中なう...")
    for th in tqdm(list(thread_list)):
        try:th.join()
        except:pass
    print("完了")
    print("書き込み中なう...",end='')
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
    print("処理中なう(1/2)")
    for i in tqdm(temp):
        if i not in temp_list:
            if ':' in i:
                temp_list.append(i)
    rfile = open(socks_file, "wb")
    print("処理中なう(2/2)")
    for i in tqdm(list(temp_list)):
        rfile.write(bytes(i, encoding='utf-8'))
    rfile.close()


def downloadsocks():
    f = open("proxy.txt", 'wb')
    try:
        r = requests.get("https://midokuriserver.com/proxytool/",timeout=500)
        f.write(r.content)
    except:
        pass


def proxydl():
    global proxies, multiple, choice, data
    ms = int(input("タイムアウトの時間どうする?(おすすめは5秒): "))
    print("プロキシをダウンロードなう...")
    start = time.time()
    downloadsocks()
    end = time.time() - start
    print(" 完了("+str(end)+"秒)")
    proxies = open(str("proxy.txt")).readlines()
    check_list("proxy.txt")
    check_socks(ms)

proxydl()
