import os.path
import tornado.ioloop
import tornado.web
import nltk

class MainHandler(tornado.web.RequestHandler):
	def post(self):
		text = self.get_argument("rawtext")
		entities = []
		postags = nltk.pos_tag(nltk.word_tokenize(text))
		#print postags
		for chunk in nltk.ne_chunk(postags):
			if hasattr(chunk, 'node'):
				tmp_tree = nltk.Tree(chunk.node,  [(' '.join(c[0] for c in chunk.leaves()))])
				entities.append(tmp_tree)
		#print entities
		self.render("home_post.html", text=text, entities=entities)
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
