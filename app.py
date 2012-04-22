import os.path, re,  csv,  pickle
import tornado.web, tornado.ioloop
from tornado.options import define, options
import nltk.probability,  nltk.classify,  nltk.tokenize,  nltk.chunk,  nltk.tree,  nltk.sem.relextract
import pickle

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm.sparse import LinearSVC
from sklearn.pipeline import Pipeline

class doc():
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home_get.html")
        
class QuestionAnswerHandler(tornado.web.RequestHandler):
    def post(self):
        question = [self.get_argument("pastequestion")]
        #os.chdir('/home/gavin/Documents/dev/python/ec2_tornado/static/pickles')
        os.chdir('/home/ubuntu/www/static/pickles')
        categories = ['HUM', 'LOC', 'NUM', 'ENTY', 'DESC', 'ABBR']
        fine_categories = dict(HUM=['desc',  'gr',  'ind',  'title'], 
                               LOC=['city',  'country',  'mount',  'other',  'state'], 
                               NUM=['code',  'count',  'date',  'dist',  'money', 'ord',  'other',  'perc',  'period', 
                      'speed',  'temp',  'volsize',  'weight'], 
                                ABBR=['abb',  'exp'], 
                                DESC=['def' , 'desc',  'manner',  'reason'], 
                                ENTY=['animal', 'body',  'color',  'cremat',  'currency',  'dismed',  'event',  'food',  'instru',  
            'lang', 'letter',  'other',  'plant',  'product',  'religion',  'sport',  'substance',  'symbol', 
            'techmeth',  'termeq',  'veh',  'word']
            )
        # open train_coarse pickle
        data_pickle = open('pickle_training_coarse.pkl', 'rb')
        train_coarse = pickle.load(data_pickle)
        data_pickle.close()
        # open text_clf pickle
        training_pickle = open('pickle_clf_coarse.pkl', 'rb')
        text_clf = pickle.load(training_pickle)
        training_pickle.close()

        #def coarse_classify(questions):
        predicted = text_clf.predict(question)
        for doc, category in zip(question, predicted):
            coarse_category = train_coarse.target_names[category]
            print '%r => %s' % (doc, coarse_category)
            
            categories = fine_categories[coarse_category]
            print categories
            
            os.chdir('/home/gavin/Documents/dev/ie/corpora/data/fine/')
            # open fine data pickle
            print 'opening data pickle: ' + 'pickle_training_%s.pkl' % coarse_category
            data_pickle = open('pickle_training_%s.pkl' % coarse_category,  'rb')
            train_data= pickle.load(data_pickle)
            data_pickle.close()
            
            # open text_clf pickle
            print 'opening training pickle: ' + 'pickle_clf_%s.pkl' % coarse_category
            training_pickle = open('pickle_clf_%s.pkl' % coarse_category, 'rb')
            text_clf_fine = pickle.load(training_pickle)
            training_pickle.close()
            
            # fine prediction
            print 'prediction for: ' + doc
            fine_predicted = text_clf_fine.predict(question)
            print train_data.target_names[fine_predicted[0]]
            answer_type_fine = train_data.target_names[fine_predicted[0]]
        
        self.render("question_analysis_post.html", 
                    question=question,  
                    answer_type_coarse=coarse_category,  
                    answer_type_fine=answer_type_fine, )
                    
    def get(self):
        self.render("question_analysis_get.html")

class SingleTweetAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        # load classifier
        f = open('/home/ubuntu/www/twitter_classifier_1.pickle')
        #f = open('twitter_classifier_1.pickle')
        classifier = pickle.load(f)
        f.close()
        
        # load features
        word_features = []
        csv_reader = csv.reader(open("/home/ubuntu/www/sentiment_features_1_1.csv","rb"))
        #csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
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
        tweet = self.get_argument("pastetweet")
        tweet_sentiment = classifier.classify(extract_features(tweet.split()))
        self.render("sentiment_singletweet_post.html", tweet=tweet,  tweet_sentiment=tweet_sentiment)
        
    def get(self):
        self.render("sentiment_get.html")
        
class TopicAnalysisHandler(tornado.web.RequestHandler):
    def post(self):
        import twitter
        api = twitter.Api(consumer_key='nmnjwvk2sVD6xQBVaMKzg',
consumer_secret='mWIam6qsGVoiFfh9MGTUboA8G1EyRk8IFUvmzSWMunk', access_token_key='14103281-uirUc767UEjO6pSToRqbvi6byNJKGppVqaf3BJv0k', access_token_secret='WwtwNwDyjnDeGlaPnokWxChR4rIocA5RQI5xIlAOM')

        # load classifier
        f = open('/home/ubuntu/www/twitter_classifier_1.pickle')
        #f = open('twitter_classifier_1.pickle')
        classifier = pickle.load(f)
        f.close()
        
        # load features
        word_features = []
        csv_reader = csv.reader(open("/home/ubuntu/www/sentiment_features_1_1.csv","rb"))
        #csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
        for row in csv_reader:
            word_features.extend(row)
        
        # gather tweets and extract status text
        rawtweets = api.GetSearch(term=self.get_argument("tweettopic"))
        tweets = []
        for tweet in rawtweets:
            tweets.append(tweet.text)
        
        # extract features from input tweet
        def extract_features(document):
            document_words = set(document)
            features = {}
            for word in word_features:
                features['contains(%s)' % word] = (word in document_words)
            return features
        
        # evaluate tweets
        tweet_sentiments = []
        for tweet in tweets:
            tweet_sentiments.append(classifier.classify(extract_features(tweet.split())))
        tweets_and_sentiments = zip(tweets,  tweet_sentiments)
            
        self.render("gather_tweets_post.html", topic=self.get_argument("tweettopic"), tweets_and_sentiments=tweets_and_sentiments)
        
    def get(self):
        self.redirect("/singletweetanalysis")
        

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
            (r"/tweetanalysis",  SingleTweetAnalysisHandler), 
            (r"/gathertweetsanalysis",  TopicAnalysisHandler), 
            (r"/questionansweranalysis",  QuestionAnswerHandler)]
            
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8000, help="run on the given port", type=int)
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
