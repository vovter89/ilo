#this is program for iLO testing
import urllib
import ssl
import requests
import pandas
import time
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import webbrowser
from pymsgbox import *


# time.sleep(1)
# chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)
# webdriver.Chrome()
#webbrowser.get(chromepath).open_new_tab(each_url)


from tkinter import *
expression = ""

def checkstatement():
    ent_text = ip.get()
    if ent_text[0].isalpha():
        print(ent_text[0])
        file = open("ips.txt", 'w')
        file.write(ent_text)
        file.close()
        alert(text='Please Enter IP range like this:'+'\n'+"XXX.XXX.XXX.XXX-XXX", title='Please enter proper IP range', button='OK')
        return
    else:
        writetofile()
def writetofile():
    str1 = ip.get()
    dic={'.': ' ', '-': ' '}
    new_str = ''
    for x in str1:
        if x in dic:
            new_str += dic[x]
        else:
            new_str += x

    new_str = list(new_str.split())
    list_count = len(new_str)
    #print(list_count)
    if (list_count == 5):
        ip1 = int(new_str[0])
        ip2 = int(new_str[1])
        ip3 = int(new_str[2])
        ip4 = int(new_str[4])
        t = int(new_str[4])+1
        b = int(new_str[3])
        if ip1 in range (1,255):
            if ip2 in range (0,256):
                if ip3 in range (0,256):
                    if ip4 in range (0,256):
                        if b in range (0,256):
                            if (b < t):
                                line = ""
                                for b in range(b, t):
                                    line += new_str[0]+'.'+new_str[1]+'.'+new_str[2]+'.'+str(b)+'\n'
                                    file = open("ips.txt", 'w')
                                    file.write(line)
                                file.close()
                            else:
                                alert(text='Enter Proper IP range', title='Please enter proper IP range', button='OK')
                                return
                        else:
                            alert(text='Enter Proper IP range (0-254)', title='Please enter proper IP range', button='OK')
                            return
                    else:
                        alert(text='Enter Proper IP range (0-254)', title='Please enter proper IP range', button='OK')
                        return
                else:
                    alert(text='Enter Proper IP range (0-254)', title='Please enter proper IP range', button='OK')
                    return
            else:
                alert(text='Enter Proper IP range (0-254)', title='Please enter proper IP range', button='OK')
                return
        else:
            alert(text='Enter Proper IP range (0-254)', title='Please enter proper IP range', button='OK')
            return
    else:
        alert(text='Please Enter IP range like this:' + '\n' + "XXX.XXX.XXX.XXX-XXX", title='Please enter proper IP range', button='OK')
        return






def openbrowser():
    res_file = open("res.txt", 'w')
    res_file.write('Here are the results: '+'\n')
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    with open('ips.txt', 'r') as f:
        all_urls = f.read().split('\n')
        for each_url in all_urls:
            with requests.Session() as ses:
                ssl._create_default_https_context = ssl._create_unverified_context()
                url = ses.get(each_url) #headers=headers)
                print(url.text)
                login_data = {
                    'username': 'vovter',
                    'password': 'vova1989'
                }
                homepage = ses.post('https://'+each_url+'/submit/', data=login_data, headers=headers)
                time.sleep(2)
                bs_home = bs(homepage.content, 'html.parser')
                print(homepage.text)
                token1 = bs_home.find('div', attrs={'class': 'domainName'})['data-domain']
                token2 = bs_home.find('div', attrs={'class': 'domainName'})["data-sb"]
                res_file = open("res.txt", 'a')
                res_file.write('username: ' + token1 + "     website: " + token2+'\n')
                alert(text='Result SAVED', title='Success', button='OK')

    f.close()
    res_file.close()

def openips():
    with open('ips.txt', 'r') as f:
        all_urls = f.read().split('\n')
        for each_url in all_urls:
            webbrowser.open('https://'+each_url)
            time.sleep(1)
    f.close()




def clear():
    global expression
    expression = ""
    ip.set("")
    clear_ipfile()

def clear_ipfile():
    with open('ips.txt', 'w') as f:
        f.write('')
    f.close()


if __name__ == "__main__":
    gui = Tk()
    gui.configure(background="#7e97bf")
    gui.title("iLO Validator")
    gui.geometry("320x200+850+450")
    ip = StringVar()

    tk.Label(gui, text="Please Enter IP Range").grid(row=1, column=1, ipady = 6)
    expression_field = Entry(gui, textvariable=ip)
    expression_field.focus()
    expression_field.grid(row = 1, column=2, padx =5, pady =10, ipady = 9, ipadx = 50)
    ip.set('')

    button2 = Button(gui, text=' Write to file ', fg='black', bg='white', height=2, width=15, command=checkstatement)
    button2.grid(row=2, column=1)


    button3 = Button(gui, text=' Open IPs in browser ', fg='black', bg='white', height=2, width=15, command=openips)
    button3.grid(row=2, column=2)

    button1 = Button(gui, text = ' Verify iLO ', fg='black', bg='white', height=2, width=15, command= openbrowser)
    button1.grid(row=3, column=2)

    clear = Button(gui, text='Clear', fg='white', bg='blue', command=clear, height=2, width=15)
    clear.grid(row=4, column=2)
    gui.mainloop()
