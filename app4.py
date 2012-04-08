import os.path,  re
import tornado.web,  tornado.ioloop
from tornado.options import define, options
import nltk
from routes import handlers

# receive a port to listen to from an argument
# change this to pre-fork multiple instances on one port in the future?
define("port", default=8000, help="run on the given port", type=int)

class doc():
    pass

class SentimentHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("sentiment_post.html", )
        
    def get(self):
        self.render("sentiment_get.html")


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument("rawtext")
        relations = []
        entities = []
        tokens = []
        IN = re.compile(r'.*\bin\b')
        doc.headline = ['a']
        def tokenize(text):
            for sentence in nltk.sent_tokenize(text):
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
                    if hasattr(chunk, 'node'):
                        if chunk.node != 'GPE':
                            tmp_tree = nltk.Tree(chunk.node, [(' '.join(c[0] for c in chunk.leaves()))])
                        else:
                            tmp_tree = nltk.Tree('LOCATION', [(' '.join(c[0] for c in chunk.leaves()))])
                        tokens.append(tmp_tree)
                        entities.append(tmp_tree)
                    else:
                        tokens.append(chunk[0])
            return tokens
        
        def extract_people_in_locations():
            for rel in nltk.sem.extract_rels('PERSON' , 'LOCATION', doc, corpus='ieer', pattern=IN):
                filler_tokens = dict(nltk.pos_tag(nltk.word_tokenize(rel['filler'])))
                tmp = rel['subjtext'] + " is in " + rel['objtext']
                relations.append(tmp)
                    
        doc.text = tokenize(text)
        #print doc.text
        extract_people_in_locations()
        
        self.render("home_post.html", text=text, entities=entities, relations=relations)
        
    def get(self):
        self.render("home_get.html")
        
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))

handlers = [
            (r"/", MainHandler), 
            (r"/sentiment",  SentimentHandler), ]
            
application = tornado.web.Application(handlers, **settings)

    
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
