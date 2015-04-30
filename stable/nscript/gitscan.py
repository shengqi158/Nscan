'''
    Example of banner grabber for Nscan
'''
import socket
import Queue
import time
import logging
import urllib2
import urllib

def FetchGit(ip, port):
    try:
        header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',\
                    'Referer':'http://www.google.com/'}
        git_url  = '/.git/config'
        svn_url = '/.svn/entries'
        payloads = [git_url, svn_url]
        pathes = ['','/app','/api','/pay','/index','/download','/about','/faq', '/blog', '/contact','/openapi']
        for path in pathes:
            for payload in payloads:
                if port == 443:
                    url = 'https://' + ip + path + payload
                if port in (80, 8080):
                    url = 'http://' + ip + ":" + str(port)+ path + payload
                try:
                    data = urllib.urlencode({})
                    req = urllib2.Request(url, data, header)
                    response = urllib2.urlopen(req)
    #                page = response.read()

                    if response.getcode() == 200:
                        return url
                except urllib2.HTTPError, e:
                    pass
                except:
                    pass
    except:
        pass


    

def FetchBanner(ip, port):
	banner = None
	sock = socket.socket()
	sock.settimeout(5)
	try:
		sock.connect((ip, port))
		sock.send('GET\r\n\r\n')
		banner = sock.recv(65535)
		sock.close()
		banner = banner.replace('\r', '')
		banner = banner.replace('\n', ' ')
		banner = banner[:50]
	except:
		pass
	return banner


def run(queue, event):
    while True:
        if queue.empty() and event.isSet():
            break
        else:
            try:
                host = queue.get(False, 3)
                result = FetchGit(host[0], host[1])
                
                result = FetchGit(host[0], host[1])
                if result:
                    logging.info('git:%s:%s:%s' %(host[0], host[1], result))
            except Queue.Empty:
				pass
