import os.path
import re
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import nltk

class doc():
    pass

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
            print "********************"
            for rel in nltk.sem.extract_rels('PERSON' , 'LOCATION', doc, corpus='ieer', pattern=IN):
                filler_tokens = dict(nltk.pos_tag(nltk.word_tokenize(rel['filler'])))
                tmp = rel['subjtext'] + " is in " + rel['objtext']
                relations.append(tmp)
                    
        doc.text = tokenize(text)
        print doc.text
        extract_people_in_locations()
        
        self.render("home_post.html", text=text, entities=entities, relations=relations)
        
    def get(self):
        self.render("home_get.html")
        
handlers = [(r"/", MainHandler)]
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8003, help="run on the given port", type=int)
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    