#!/usr/bin/env python
# ScanT3r Web application Security Scanner - By : Khaled Nassar @knassar702
__author__ = 'Khaled Nassar'
__version__ = '0.1'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'

import time,sys,os,logging,re,threading
from core.scanner import *
from core.colors import *
from core.requester import *
from optparse import OptionParser
from queue import Queue

q = Queue()

def post_data(params):
    if params:
        prePostData = params.split("&")
        postData = {}
        for d in prePostData:
            p = d.split("=", 1)
            postData[p[0]] = p[1]
        return postData
    return {}

def getargs():
	global url,froms,data,rfile,r,cookie,thr,timeo,date,encoded
	r=False
	helper=("""
Options:
  -h, --help          |    show this help menu
  -u URL, --url=URL   |    Target URL (e.g."http://www.target.com/vuln.php?id=1")
  --data=DATA         |    Data string to be sent through POST (e.g. "id=1")
  --list=FILE         |    Get All Urls from List..
  --threads=THR       |    Max number of concurrent HTTP(s) requests (default 10)
  --timeout=time      |    Seconds to wait before timeout connection
  --cookies=COK       |    HTTP Cookie header value (e.g. "PHPSESSID=a8d127e..")
  --encode=1          |    How Many encode the payload
		""")
	optp = OptionParser(add_help_option=False)
	optp.add_option("-u","--url",dest="url",help='Target URL (e.g. "http://www.target.com/vuln.php?id=1")')
	optp.add_option("--data",dest="data",help='Data string to be sent through POST (e.g. "id=1")')
	optp.add_option("-h","--help",dest="help",action='store_true',help="Show Help Menu")
	optp.add_option("--list",dest="rfile",help="Get All Urls from file ..")
	optp.add_option("--threads",type='int',dest="thread",help='Thread number ..(DEF : 10)')
	optp.add_option("--timeout",type='int',dest="timeo",help="Set Timeout")
	optp.add_option("--cookies",dest='cookie',help='Add cookie in Request')
	optp.add_option("--encode",type="int",dest="encoded",help='How Many encode the payload')
	opts, args = optp.parse_args()
	if opts.thread:
		thr = opts.thread
	else:
		thr = 10
	if opts.url:
		url=opts.url
	if opts.url == None and opts.rfile != None:
		rfile=str(opts.rfile)
		r=True
		url = 'File'
	if opts.encoded:
		encoded = opts.encoded
	else:
		encoded = 1
	if opts.data:
		date = opts.data
		date = post_data(date)
	else:
		date = None
	if opts.timeo:
		timeo = opts.timeo
	else:
		timeo = None
	if opts.help:
		print(helper)
		exit()
	if opts.url != None and opts.rfile != None:
		print (bad+" You Can't Start ScanT3r With List and url option ")
		sys.exit()
	if opts.cookie:
		cookie=str(opts.cookie)
		cookie=post_data(cookie)
	else:
		cookie=None
	if opts.url == None and opts.rfile == None and opts.help == None:
		optp.error('missing a mandatory option (--url,--cookies,--data,--list,--encode) Use -h for help ..!')
		exit()
def logo():
	l=(f'''{red}{bold}
\t   _____                ___________     
\t  / ___/_________ _____/_  __/__  /_____
\t  \__ \/ ___/ __ `/ __ \/ /   /_ </ ___/
\t ___/ / /__/ /_/ / / / / /  ___/ / /    
\t/____/\___/\__,_/_/ /_/_/  /____/_/
\t
\t{yellow}# Coded By : Khaled Nassar @knassar702
{end}
''')
	print (l)
	time.sleep(1)
def start(url,cookie,timeo,date):
	global rfile,no
	if r==True:
		try:
			rfile=open(rfile,'r')
		except:
			print(f"{bad} Error ..!")
			exit()
		for url in rfile:
			url=url.strip()
			if url.startswith('http://') or url.startswith('https://'):
				no = False
			else:
				no = False
				url='http://'+url
			if '?' in url or '*' in url:
				no = False
			else:
				print(f"{bad} No parameters :v ..")
				no = True
			if no == False:
				v.xss(url,cookie,timeo,encoded)
				v.sqli(url,cookie,timeo,encoded)
				v.osinj(url,cookie,timeo,date,encoded)
				v.ssti(url,cookie,timeo,date,encoded)
	else:
		if date:
			v.xss_post(url,cookie,timeo,date)
			v.sqli_post(url,cookie,timeo,date)
			v.osinj_post(url,cookie,timeo,date)
			v.ssti_post(url,cookie,timeo,date)
		else:
			v.sqli(url,cookie,timeo,encoded)
			v.xss(url,cookie,timeo,encoded)
			v.osinj(url,cookie,timeo,encoded)
			v.ssti(url,cookie,timeo,encoded)
def threader():
	while True:
		item = q.get()
		start(item,cookie,timeo,date)
		q.task_done()
if __name__ == "__main__":
	try:
		logo()
		v=from_url_get()
		getargs()
		con(url)
		if r == True or date != None:
			pass
		else:
			if url.startswith('http://') or url.startswith('https://'):
				pass
			else:
				url='http://'+url
			if '?' in url or '*' in url or date != None:
				pass
			else:
				print(f"{bad} Please Add parameters in url ..")
				exit()
		for i in range(thr):
			t1 = threading.Thread(target=threader)
			t1.daemon = True
			t1.start()
		q.put(url)
		q.join()
	except KeyboardInterrupt:
		print(f'\n{bad} Good Bye :)\n')
		exit()