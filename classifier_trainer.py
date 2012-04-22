# overfitting features when neutral is included.

import csv
import nltk

# this is not a script

# write list to csv (1 column of all features)
csv_writer = csv.writer(open("sentiment_features_1.csv", "wb"))
for r in word_features:
    csv_writer.writerow([r])
    
# write list to csv (1 row of all features)
csv_writer = csv.writer(open("sentiment_features_2.csv", "wb"))
csv_writer.writerow(word_features)

# using this to read csv
word_features_assembled = []
csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
for row in csv_reader:
    word_features_assembled.extend(row)

# read a csv to a list
word_features_assembled = []
csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
for row in csv_reader:
    word_features_assembled.append(row)
    
    
# to read positive and negative tweets from the csv
import os
os.chdir('/home/gavin/Documents/dev/python/ec2_tornado')
tweets = []
reader = csv.reader(open('full-corpus.csv'), delimiter=',')
for row in reader:
    tmp = nltk.word_tokenize(row[4])
    if (row[1] == 'positive' or row[1] == 'negative'):
        tweets.append([[word.lower() for word in tmp if len(word) >= 3],  row[1]])
        
# to read positive,neg and neutral tweets from the csv
for row in reader:
    tmp = nltk.word_tokenize(row[4])
    if (row[1] == 'positive' or row[1] == 'negative' or row[1] == 'neutral'):
        tweets.append([[word.lower() for word in tmp if len(word) >= 3],  row[1]])
    
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def get_words_in_tweets(tweets):
    all_words = []
    for (words,  sentiment) in tweets:
        all_words.extend(words)
    return all_words

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
tweet = ""
tweet_sentiment = classifier.classify(extract_features(tweet.split()))

neutral = [t for t in tweets if t[1] == 'neutral']
#neutral_training = neutral[:600]
negative = [t for t in tweets if t[1] == 'negative']
positive = [t for t in tweets if t[1] == 'positive']

import pickle
f = open('twitter_classifier_2.pickle', 'wb')
pickle.dump(classifier, f)
f.close()















