import os.path
import re
import tornado.ioloop
import tornado.web
import nltk

class doc():
	pass    
      
class MainHandler(tornado.web.RequestHandler):
	def post(self):
		text = self.get_argument("rawtext")
        entities = []
        relations = []
#postags = nltk.pos_tag(nltk.word_tokenize(text))
        IN = re.compile (r'.*\bin\b')

        doc.headline = ['a']

		# for chunk in nltk.ne_chunk(postags):
		# 	if hasattr(chunk, 'node'):
		# 		tmp_tree = nltk.Tree(chunk.node,  [(' '.join(c[0] for c in chunk.leaves()))])
		# 		entities.append(tmp_tree)
            
        def tokenize_text_and_tag_named_entities(text):
            tokens = []
            for sentence in nltk.sent_tokenize(text):
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
                    if hasattr(chunk,  'node'):
                        if chunk.node != 'GPE':
                            tmp_tree = nltk.Tree(chunk.node,  [(' '.join(c[0] for c in chunk.leaves()))])
                        else:
                            tmp_tree = nltk.Tree('LOCATION',  [(' '.join(c[0] for c in chunk.leaves()))])
                        tokens.append(tmp_tree)
                    else:
                        tokens.append(chunk[0])
            return tokens

        doc.text = tokenize_text_and_tag_named_entities(text)
        print doc.text
        extract_people_in_locations()

        self.render("home_post.html", text=text, entities=entities, relations=relations)

	def get(self):
		self.render("home_get.html")

handlers = [
    (r"/", MainHandler),
]

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
)         

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()