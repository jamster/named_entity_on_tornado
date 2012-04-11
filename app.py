import os.path, re,  csv
import tornado.web, tornado.ioloop
from tornado.options import define, options
import nltk.probability,  nltk.classify,  nltk.tokenize,  nltk.chunk,  nltk.tree,  nltk.sem.relextract
import pickle


class doc():
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home_get.html")

class SentimentAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        # load classifier
        f = open('/home/ubuntu/www/twitter_classifier_1.pickle')
        classifier = pickle.load(f)
        f.close()
        
        # load features
        word_features = []
        csv_reader = csv.reader(open("/home/ubuntu/www/sentiment_features_1_1.csv","rb"))
        for row in csv_reader:
            word_features.extend(row)
                
        # extract features from input tweet
        def extract_features(document):
            document_words = set(document)
            features = {}
            for word in word_features:
                features['contains(%s)' % word] = (word in document_words)
            return features
        
        # evaluate a tweet
        tweet = self.get_argument("tweet")
        tweet_sentiment = classifier.classify(extract_features(tweet.split()))
        self.render("sentiment_post.html", tweet=tweet,  tweet_sentiment=tweet_sentiment)
        
    def get(self):
        self.render("sentiment_get.html")
        

class EntityRelationExtractorHandler(tornado.web.RequestHandler):
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
        
        self.render("extractor_post.html", text=text, entities=entities, relations=relations)
        
    def get(self):
        self.render("extractor_get.html")
        
handlers = [
            (r"/", MainHandler), 
            (r"/extractor",  EntityRelationExtractorHandler), 
            (r"/sentiment",  SentimentAnalysisHandler), ]
            
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8000, help="run on the given port", type=int)
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
