import tornado.httpserver
import tornado.ioloop
import tornado.web
from tempfile import TemporaryFile
from SimpleCV import *
import threading
import os
from IPython.core.display import Javascript as JS
from IPython.core.display import display


class ImgHandler(tornado.web.RequestHandler):

    img = None
    def get(self,x=0):
        if(ImgHandler.img==None):
            return
        #print ImgHandler.img
        tempFile = TemporaryFile()
        ImgHandler.img.save(tempFile)
        tempFile.seek(0)
        lines = tempFile.readlines()
        #print len(lines)
        self.output = ''.join(lines)
        self.set_header("Cache-control", "no-cache")
        self.set_header("Content-Type","image/png")
        self.set_header("Content-Length",len(self.output))
        self.write(self.output)
        self.finish()
        
    @staticmethod
    def setImg(i):
        ImgHandler.img = i

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
        ImgHandler.setImg(i)
        s = """
            window.disp.stop()
            var img = window.disp.document.getElementById('id_img')
            img.src = "http://localhost:8000/%d.png";
            
        """ % id(i)
        display(JS(s))
        
        
