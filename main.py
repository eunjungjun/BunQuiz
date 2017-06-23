import tornado.ioloop
import tornado.web
import random
import json

def getMax():
    with open('results.json') as data:
        buns = json.load(data)
    a = max(buns, key=buns.get)
    return a

def shuffle(d):
    d = list(d)
    random.shuffle(d)
    return d

def openJson(fl):
    with open(fl) as data:
        Qs = json.load(data)
    return Qs

class Application(tornado.web.RequestHandler):
    def get(self):
        self.render('application.html', shuffle=shuffle, openJson=openJson)
        
class Results(tornado.web.RequestHandler):
    def get(self):
        DICT = {}
        
        for i in range(7):
            choice = self.get_argument('{}'.format(i), '')
            DICT[choice] = DICT.get(choice, 0) + 1
        
        json.dump(DICT, open('results.json', 'w'))
        self.render('bun.html', getMax=getMax)

app = tornado.web.Application([
        (r"/", Application),
        (r"/results", Results),
        (r"/css1/(.*)", tornado.web.StaticFileHandler, {'path':'application.css'}),
        (r"/css2/(.*)", tornado.web.StaticFileHandler, {'path':'bun.css'})
        ],
        debug=True
    )

app.listen(5550)
tornado.ioloop.IOLoop.current().start()