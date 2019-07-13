# -*- coding: UTF-8 -*-
import os, sys, time, re
import requests
import IP
import ip2loc

reload(sys)
sys.setdefaultencoding('utf8')

WhiteList = ["139.162.66.5","139.162.67.5","139.162.68.5","139.162.72.5","139.162.71.5"]
AllIP = []
IP_time = {'ip':time.time()}

def checkip(ip):

    URL = 'http://ip.taobao.com/service/getIpInfo.php'
    try:
        r = requests.get(URL, params=ip, timeout=3)
    except requests.RequestException as e:
        print(e)
    else:
        json_data = r.json()
    if json_data[u'code'] == 0:
        return json_data[u'data'][u'country'].encode('utf-8') + json_data[u'data'][u'area'].encode('utf-8') + json_data[u'data'][u'region'].encode('utf-8') + json_data[u'data'][u'city'].encode('utf-8') + '_' + json_data[u'data'][u'isp'].encode('utf-8') + '_'

    #  print '所在国家： ' + json_data[u'data'][u'country'].encode('utf-8')
    #  print '所在地区： ' + json_data[u'data'][u'area'].encode('utf-8')
    #  print '所在省份： ' + json_data[u'data'][u'region'].encode('utf-8')
    #  print '所在城市： ' + json_data[u'data'][u'city'].encode('utf-8')
    #  print '所属运营商：' + json_data[u'data'][u'isp'].encode('utf-8')
    else:
        return '查询失败'

def ConvertToUXTime(interval):

    if interval < 60:
        return str(int(interval))+"秒"
    elif interval < 3600:
        return str(int(interval/60))+"分"+str(int(interval)%60)+"秒"
    else:
        return str(int(interval/3600))+"时"+str(int(interval)%3600/60)+"分"+str(int(interval)%60)+"秒"


while True:

    currentIP = []
    OnlineIP = []
    OfflineIP = []

    OnlineInterval = []


    #print(time.asctime())

    time.sleep(4)
    netStatus = os.popen("netstat -nu | grep udp | awk '{print $5}'").readlines()
    #addr = requests.get(url="https://ip.cn/index.php?ip="+"183.220.155.47").json()
    #print(addr)
    for oneIP in netStatus:
        #print(oneIP)
        end = re.search(":",oneIP).start()
        IP = oneIP[0:end]
        #print(IP)
        #addr = os.popen("curl https://ip.cn/index.php?ip="+IP).read()
        #print(addr)

        #decline 127.*.*.*
        IPFirstNumberEnd = re.search("\.",IP).start()
        IPFirstNumber = IP[0:IPFirstNumberEnd]
        #print(IPFirstNumber)
        if IPFirstNumber == '127':
            continue
        

        currentIP.append(IP)

        #print(oneIP)

    for oneNewIP in currentIP:

        try:
            WhiteList.index(oneNewIP)
        except:
            pass
        else:
            continue

        try:
            AllIP.index(oneNewIP)
        except:
            OnlineIP.append(oneNewIP)
            AllIP.append(oneNewIP)
            IP_time[oneNewIP] = time.time()
        else:
            pass

    for oneOldIP in AllIP:

        try:
            WhiteList.index(oneOldIP)
        except:
            pass
        else:
            continue

        try:
            currentIP.index(oneOldIP)
        except:
            OfflineIP.append(oneOldIP)
            AllIP.remove(oneOldIP)
            OnlineInterval.append(time.time()-IP_time[oneOldIP])
            del IP_time[oneOldIP]
        else:
            pass

    
    title = ""
    output = ""

    for oneIP in OnlineIP:
        IPaddr = checkip({'ip': oneIP}) #str(ip2loc.find(oneIP))
        #IPaddr = IPaddr.replace("\t","")
        
        #IPaddr = IPaddr.replace("\t","")
        title +=  "新IP上线："+IPaddr+oneIP
        output += "新IP上线："+IPaddr+oneIP+"\n"
        #print("有新的IP上线："+oneIP)
    
    for oneIP,oneInterval in zip(OfflineIP,OnlineInterval):
        IPaddr = checkip({'ip': oneIP})#str(ip2loc.find(oneIP))
        #IPaddr = IPaddr.replace("\t","")
        title += "IP下线："+"「"+ConvertToUXTime(oneInterval)+"」"+IPaddr+oneIP
        output += "IP下线："+"「"+ConvertToUXTime(oneInterval)+"」"+IPaddr+oneIP+"\n"
        #print("检测到IP下线："+oneIP)
    
    if len(OnlineIP)!=0 or len(OfflineIP)!=0:
        output += "当前在线IP: "
        #print("当前在线IP:")
        for oneIP in currentIP:
            IPaddr = checkip({'ip': oneIP})#str(ip2loc.find(oneIP))
            #IPaddr = IPaddr.replace("\t","")
            output += IPaddr+oneIP+" "
            #print(oneIP)

        output += "\n------ "
        output += time.asctime()
        output += "\n"
        
        print(output)

        #os.system("rm /root/Documents/mail/IPChangeInform.txt")
        fp = open("/root/Documents/mail/IPChangeInform.txt","w")
        fp.write(output)
        #os.system("/root/Documents/mail/sendTxtTo_icloud.sh "+title+" \"/root/Documents/mail/IPChangeInform.txt\"")

        appendFp = open("/root/Documents/mail/IPChangeLog.txt","a")
        appendFp.write(output)
        

        fp.close()
        appendFp.close()

        
        os.system("/root/Documents/mail/NotificateTxtMe.sh "+title+" \"/root/Documents/mail/IPChangeInform.txt\" &")
        #os.system("/root/Documents/mail/sendTo_icloud.sh "+title+" "+output+" &")




