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

class KnowetryHandler(tornado.web.RequestHandler):
    def post(self):
        question = [self.get_argument("pastequestion")]
        d = {}
        d['HUM'] = {
            'desc' : '"%s"\nDescribe this person\'s manners\ncomportment\nbearing\nvicissitudes\nSpare me no details.' % question[0],
            'gr' : '"%s"\nhe inquired.\n"I bet you would like me to tell you\nthe name of that group of people\nand make a pronouncement about\ntheir collective moral fiber,\nBut I am loath to make such a\ngeneralization."' % question[0],
            'ind' : '"%s"\nshe asked, her eyes smoldering\n"I bet you would like me to tell you\nthe name of that person," I said.\nBut I don\'t know. If I had to guess, maybe...\n...Gary?' % question[0], 
            'title' : '"%s"\nasked the new kid.\nI could tell he was a shark;\nhe\'s gunning for the job.\n"You want to know what that person\'s title is?"\nI asked. "He\'s the Vice President in Charge of Not Being a Snitch."' % question[0], 
        }
        d['LOC'] = {
            'city' : 'She was back from the farmer\'s market.\n"%s"\nshe muttered, and nonchalantly flicked\nthe last of her cigarette to the ground.\n"I bet you would like me to tell you\nthe name of that city, and whether it has\nany independent book stores," I said.' % question[0],
            'country' : '"%s"\nhe asked, as he crushed the solo cup.\n"Brosef, you know you\'re my best bud.\nI really wish I could tell you\nthe name of that country," I said.' % question[0], 
            'mount' : '"%s"\nhe wondered aloud.\n"It would be such an achievement\nto climb that mountain.\nI\'ll start training as soon as I finish\nplaying Angry Birds.' % question[0], 
            'other' : 'I have not written an other poem template yet', 
            'state' : '"%s"\nhe shrieked and shook me\nby the shoulders.\n"Sir, I don\'t know what state that is,\nand I\'m going to have to escort you out\nof the petting zoo," the attendant calmly replied.' % question[0], 
        }
        d['NUM'] = {
            'code' : '"%s"\nhe shrieked and shook me\nby the shoulders.\n"Sir, I don\'t know what the number is,\nand I\'m going to have to escort you out\nof the petting zoo," the attendant calmly replied.' % question[0],  
            'count' : 'I have not written a poem template for this yet',
            'date' : '"%s"\nshe asked.\nShe was missing the point,\nand it killed me.\n"I know this is not\nthe date you asked about, but\nit is more important.\nMy birthday is May 26th."' % question[0],
            'dist' : '"%s"\nwas all that was written\non the ransom note.\n"Nobody knows that distance!\nIt is unknowable!" he cried,\nripping the document into pieces.' % question[0], 
            'money' : '"%s"\nasked Kevin.\n"Now that I\'ve sold Instagram\nI can buy... at least four."' % question[0],
            'ord' : 'You asked about an order or ranking.Congratulations! These questions are under-represented in the training corpus.', 
            'other' : 'You asked about a number\nBut I do not have\na more specific category.\nTry this poem\nby William Wordswoth instead\n"And to the left, three yards beyond,\nYou see a little muddy pond\nOf water--never dry\nI measured it from side to side:\nTwas four feet long, and three feet wide"\nWilliam,\nNice job measuring.', 
            'perc' : '"%s"\nshe hissed.\nIt would take all of my wits\nto answer with the correct percentage\nand get out alive.'% question[0],  
            'period' : '"%s"\nhe demanded, panicking.\nI knew the duration\nof what he asked about.\nBut I had the upper hand now\nAnd I was not about to waste it\nwith the truth.' % question[0],
            'speed' : '"%s"\n"Let me tell you-\nAnd I don\'t tell this\nto just anyone ya know-\nthe speed is quite impressive."'% question[0],
            'temp' : '"\'%s\'you ask?\nI bet you would like\nfor me to tell you\nthat temperature.\nJust like if someone\nhad told me what temperature\nchicken needs to be cooked to\nall those party guests\nmight still be alive."' % question[0],
            'volsize' : 'It was 2032 when Clippy the Office Assistant\nbecame sentient.\n"%s"\nClippy swiftly destroyed\nall documents alluding to the correct size.\n"It looks like you\'re writing a letter," mocked the godless machine.' % question[0],  
            'weight' : '"%s"\nshe asked, her eyes smoldering\n"I bet you would like me to tell you\nthat weight," I said.\nBut I don\'t know. If I had to guess, about...\n...14?' % question[0],  
        }
        d['ABBR'] = {
            'abb' : 'I have not written an abbr poem template yet', 
            'exp' : '"%s"\nhe screamed down from the rafters.\n"Calm down! You can find the meanings\nof abbreviations and acronyms\non Wikipedia!" said the bowling alley\'s patrons.' % question[0], 
        }
        d['ENTY'] = {
            'animal' : '"%s"\nshe asked, her eyes ablaze\n"I bet you would like me to tell you\nthe name of that animal, and whether\nit is edible," I said.\n"But like many of nature\'s secrets,\nit is unknowable to man."' % question[0], 
            'body' : 'I have not written a body poem template yet',
            'color' : 'I have not written a color poem template yet', 
            'cremat' : '"%s"\nIt sounds like you\'re interested\nin some sort of creative or cultural material.\nLet me recommend Michael Bay\'s seminal 2011 piece\n"Transformers: Dark of the Moon."' % question[0],
            'currency' : '"\'%s\'\nDamnit Daniel, you know this.\nYou\'ve been preparing for years for this.\nJust say the right currency,\nand maybe people will forgive you, finally,\nfor what happened that day at the go-cart track."' % question[0],
            'dismed' : '"%s"\naOne need not worry\nabout diseases and medicines\nThrough poetry\nthe soul is immutable.' % question[0],
            'event' : '"%s"\n"Uh dude, I don\'t know what you are\nreferring to. But let me tell you\nabout one historical event\nthat I do know about:\nLAST NIGHT!!!!!\nBro, it was sick.\nWe played pong at Goodfellow\'s\nIt was Will\'s birthday.\nWe made Dave do all these shots\nand he threw up on this one girl."' % question[0],
            'food' : 'I have not written a food poem template yet', 
            'instru' : 'I have not written an isntru poem template yet', 
            'lang' : 'I have not written a lang poem template yet', 
            'letter' : 'I have not written a letter poem template yet', 
            'other' : 'I have not written an other poem template yet', 
            'plant' : 'Plants\nand trees\nand shrubberies\nand salad\nand such',
            'product' : '"%s"\nI do not know what that product is\nbecause it is not\nin my copy of SkyMall.' % question[0],
            'religion' : 'I have not written a religion poem template yet', 
            'sport' : '"%s"\n"Uh, I\'m not sure which one that is,\nbut I like sports too.\nI\'ll grab my Dale Earnhardt Sr. tank top\nand we can get some Bud Light with Lime\nand watch the race."' % question[0],
            'substance' : 'I have not written a substance poem template yet', 
            'symbol' : 'I have not written a symbol poem template yet', 
            'techmeth' : "This is the technology, methods and procedures class. Frankly, it is so overfit that it is unlikely anyone will encounter it.",
            'termeq' : '"%s"\nAre you looking for a synonym\nor a coordinate term?\n"These distinctions are important!"\nthe linguist screams.' % question[0],
            'veh' : '"%s"\nI don\'t know, but\nvehicles make me think about how\nEvery night in my dreams\nI see you, I feel you\nThat is how I know you, go on\nNear, far, wherever you are\nI believe that the heart does go on\nOnce more you open the door\nAnd you\'re here in my heart\nAnd my heart will go on and on.' % question[0],
            'word' : 'I have not written a word poem template yet', 
        }
        d['DESC'] = {
            'def' : '"%s"\n"How can I tell you what that means\nwhen I can\'t even tell you\nwhat it means\nTO BE."\nreplied young, angsty Gavin.' % question[0], 
            'desc' : '"%s"\nMy father nervously replied:\n"Well, it\'s a little like,\nuh, it\'s kind of like,\nsort of, you know,\nWhen the nice man at the aquarium\nthrows all the food into the big tank."' % question[0],
            'manner' : '"%s"\nshe asked, struggling to maintain\na semblance of control.\nShe pronounced the words\nwith surgical precision\nas she demanded, unyieldingly,\na description of the manner or process.' % question[0],
            'reason' : '"%s"\nthe student asked.\n"Why, my silly boy,"\nhe drawled,\n"nobody knows\nthe reason, because\nit is not in the Bible."' % question[0], 
        }
        expanded_types = dict(
            HUM='Human', 
            LOC='Location', 
            NUM='Number', 
            ABBR='Abbreviation', 
            DESC='Description', 
            ENTY='Entity', 
            desc='Description', 
            gr='Organization or group of people', 
            ind='Individual person', 
            title='Title', 
            city='City',
            country='Country', 
            state='Geo-political state', 
            mount='Mountain range', 
            other='Other', 
            code='Code', 
            count='Count or quantity', 
            date='Date', 
            dist='Distance', 
            money='Money', 
            ord='Order or rank', 
            perc='Percentage', 
            period='Period or duration', 
            speed='Speed', 
            temp='Temperature', 
            volsize='Volume or size', 
            weight='Weight', 
            abb='Abbreviation', 
            exp='Expansion of an abbreviation', 
            manner='Manner or way', 
            reason='Reason or cause', 
            animal='Animal', 
            body='Body or organ', 
            color='color', 
            cremat='Creative or cultural material', 
            currency='Currency', 
            dismed='Disease or Medicine', 
            event='Event', 
            food='Food', 
            instru='Instrument', 
            lang='Language', 
            letter='Alphabet letter', 
            plant='Plant', 
            product='Product', 
            religion='Religion', 
            sport='Sport', 
            substance='Material or substance', 
            symbol='Symbol', 
            techmeth='Technological method', 
            termeq='Equivalent term',
            veh='Vehicle', 
            word='Word', 
        )
        expanded_types['def'] = 'Definition'

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
            
            #os.chdir('/home/gavin/Documents/dev/ie/corpora/data/fine/')
            os.chdir('/home/ubuntu/www/static/pickles')
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
        
        self.render("knowetry_post.html", 
                    question=question[0], 
                    poem=d[coarse_category][answer_type_fine],  
                    answer_type_coarse=expanded_types[coarse_category],  
                    answer_type_fine=expanded_types[answer_type_fine], )
                    
    def get(self):
        self.render("knowetry_get.html")
        
class HowItWorksHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("howitworks_get.html")
        
class QuestionAnswerHandler(tornado.web.RequestHandler):
    def post(self):
        expanded_types = dict(
            HUM='Human', 
            LOC='Location', 
            NUM='Number', 
            ABBR='Abbreviation', 
            DESC='Description', 
            ENTY='Entity', 
            desc='Description', 
            gr='Organization or group of people', 
            ind='Individual person', 
            title='Title', 
            city='City',
            country='Country', 
            state='Geo-political state', 
            mount='Mountain range', 
            other='Other', 
            code='Code', 
            count='Count or quantity', 
            date='Date', 
            money='Money', 
            ord='Order or rank', 
            perc='Percentage', 
            period='Period or duration', 
            speed='Speed', 
            temp='Temperature', 
            volsize='Volume or size', 
            weight='Weight', 
            abb='Abbreviation', 
            exp='Expansion of an abbreviation', 
            manner='Manner or way', 
            reason='Reason or cause', 
            animal='Animal', 
            body='Body or organ', 
            color='color', 
            cremat='Creative or cultural material', 
            currency='Currency', 
            dismed='Disease or Medicine', 
            event='Event', 
            food='Food', 
            instru='Instrument', 
            lang='Language', 
            letter='Alphabet letter', 
            plant='Plant', 
            product='Product', 
            religion='Religion', 
            sport='Sport', 
            substance='Material or substance', 
            symbol='Symbol', 
            techmeth='Technological method', 
            termeq='Equivalent term',
            veh='Vehicle', 
            word='Word', 
        )
        expanded_types['def'] = 'Definition'

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
            
            #os.chdir('/home/gavin/Documents/dev/ie/corpora/data/fine/')
            os.chdir('/home/ubuntu/www/static/pickles')
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
                    question=question[0],  
                    answer_type_coarse=expanded_types[coarse_category],  
                    answer_type_fine=expanded_types[answer_type_fine], )
                    
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
            (r"/questionansweranalysis",  QuestionAnswerHandler),
            (r"/knowetry", KnowetryHandler),
            (r"/howdoesitwork",  HowItWorksHandler), 
            ]
            
settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8000, help="run on the given port", type=int)
    
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
