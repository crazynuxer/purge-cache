#!/usr/bin/env python
import urlparse, sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
from requests import Request, Session
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('purge.conf')
servers = config.get('purge', 'server').split()



def GetPath(url	):
    if url.startswith('http'):
        domain = urlparse.urlparse(url).netloc
        path = urlparse.urlparse(url).path + "?" + urlparse.urlparse(url).query
	#print domain + ' ' + path + ' ' + urlparse.urlparse(url).query
	print domain + ' ' + path
    elif url.startswith('//'):
        url = "http:" + url
        domain = urlparse.urlparse(url).netloc
        path = urlparse.urlparse(url).path + "?" + urlparse.urlparse(url).query
	print domain + ' ' + path
    else:
        url = "http://" + url
        domain = urlparse.urlparse(url).netloc
        path = urlparse.urlparse(url).path + "?" + urlparse.urlparse(url).query
	print domain + ' ' + path
    return domain, path    

def Purge(host,domain,path):
    s = Session()
    req = Request('PURGE', "http://%s/purge/%s" % (host, path),headers={'Host': domain})
    prepped = req.prepare()

    # do something with prepped.body
    # do something with prepped.headers

    resp = s.send(prepped,timeout=5)

    print(resp.status_code)



class Bar(tornado.web.RequestHandler):
    def get(self):
        self.write('simple api')


class purge(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        url = self.get_argument("uri",None,)
        urlparse.urlparse(self.request.uri).query[4:]
        turl = GetPath(urlparse.urlparse(self.request.uri).query[4:])
        test = urlparse.urlparse(self.request.uri).query[4:]
        for server in servers:
            response = server + ' ' + turl[0] + ' ' + turl[1] + " </br>"
            self.write(response)
        self.finish()

application = tornado.web.Application([
    (r"/", Bar),
    (r"/purge", purge),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(1111)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()

