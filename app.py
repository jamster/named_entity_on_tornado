import os.path, re
import tornado.web, tornado.ioloop
from tornado.options import define, options
import nltk.probability,  nltk.classify,  nltk.tokenize,  nltk.chunk,  nltk.tree,  nltk.sem.relextract

class doc():
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home_get.html")

class SentimentAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]
        neg_tweets = [('I do not like this car', 'negative'),
                      ('This view is horrible', 'negative'),
                      ('I feel tired this morning', 'negative'),
                      ('I am not looking forward to the concert', 'negative'),
                      ('He is my enemy', 'negative')]

        tweets = []
        for (words,  sentiment) in pos_tweets + neg_tweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
            tweets.append((words_filtered,  sentiment))
            
        test_tweets = [
            (['feel', 'happy', 'this', 'morning'], 'positive'),
            (['larry', 'friend'], 'positive'),
            (['not', 'like', 'that', 'man'], 'negative'),
            (['house', 'not', 'great'], 'negative'),
            (['your', 'song', 'annoying'], 'negative')]

        def get_words_in_tweets(tweets):
            all_words = []
            for (words,  sentiment) in tweets:
                all_words.extend(words)
            return all_words

        def get_word_features(wordlist):
            wordlist = nltk.FreqDist(wordlist)
            word_features = wordlist.keys()
            return word_features
            
        def extract_features(document):
            document_words = set(document)
            features = {}
            for word in word_features:
                features['contains(%s)' % word] = (word in document_words)
            return features
                
        word_features = get_word_features(get_words_in_tweets(tweets))

        training_set = nltk.classify.apply_features(extract_features, tweets)
        classifier = nltk.NaiveBayesClassifier.train(training_set)

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

    
