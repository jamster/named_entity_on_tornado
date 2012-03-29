import os.path
import tornado.ioloop
import tornado.web
import nltk

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        entities = []
	text = "The members scattered for several months, but six months later the group was back for another try; the new lineup included McEuen, Hanna, Fadden, Thompson, and Jim Ibbotson (guitars, accordion, drums, percussion, piano, vocals). They returned to their record company with a demand for control over their recordings and the record company agreed. Bill McEuen became the group's producer as well as its manager. The first result of this new era in the Nitty Gritty Dirt Band's history was Uncle Charlie & His Dog Teddy, issued in 1970. Rooted tightly in their jug band sound, the album had a country feel but no trace of the vaudeville and novelty numbers that had appeared on their earlier records. The album yielded what is the group's best-known single, their cover of Jerry Jeff Walker's 'Mr. Bojangles,' and suddenly, the band had a following bigger than anything they'd known during their brief bout of success in 1967. Their next album, All The Good Times, released in early 1972, had an even more countrified feel."
	tokens = nltk.word_tokenize(text)
	postags = nltk.pos_tag(tokens)
	#print postags
        chunks = nltk.ne_chunk(postags)
	for chunk in chunks:
		if hasattr(chunk, 'node'):
			tmp_tree = nltk.Tree(chunk.node,  [(' '.join(c[0] for c in chunk.leaves()))])
			entities.append(tmp_tree)
	print entities
        self.render("home.html",
		 text=text,
                 entities=entities)                   

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
