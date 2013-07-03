import tornado.httpserver
import tornado.ioloop
import tornado.web
from tempfile import TemporaryFile
from SimpleCV import *
import threading
import os
from IPython.core.display import Javascript as JS
from IPython.core.display import display

img = None
class ImgHandler(tornado.web.RequestHandler):


    def get(self,x=0):
        if(img==None):
            return
        #print ImgHandler.img
        tempFile = TemporaryFile()
        img.save(tempFile)
        tempFile.seek(0)
        lines = tempFile.readlines()
        #print len(lines)
        self.output = ''.join(lines)
        self.set_header("Cache-control", "no-cache")
        self.set_header("Content-Type","image/png")
        self.set_header("Content-Length",len(self.output))
        self.write(self.output)
        self.finish()

handlers = [
(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'files'}),
(r"/(.*)",ImgHandler)
]
settings = dict(cookie_secret=os.urandom(1024))
app = tornado.web.Application(handlers,**settings)
app.listen(8000)


#ImgHandler.img = Image('lenna')
#tornado.ioloop.IOLoop.instance().start()
threading.Thread(target=tornado.ioloop.IOLoop.instance().start).start()
print "hello"

class DisplayNB:
    num = 0
    def __init__(self,w,h):
        
        raw_lines = open('image.html').readlines()
        lines = [line.replace('\n','') for line in raw_lines]
        template = ''.join(lines)
        
        self.startStr = """
        window.disp = window.open('','','width=%d,height=%d')
        window.disp.document.write('%s')
        """ % (w,h,template)
        
        display(JS(self.startStr))
        

    def showImg(self,i):
        global img
        img = i
        s = """
            window.disp.stop()
            var img = window.disp.document.getElementById('id_img')
            img.src = "http://localhost:8000/%d.png";
            
        """ % id(img)
        display(JS(s))
        
        
