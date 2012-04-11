import csv

# write list to csv (1 column of all features)
csv_writer = csv.writer(open("sentiment_features_1.csv", "wb"))
for r in word_features:
    csv_writer.writerow([r])
    
# write list to csv (1 row of all features)
csv_writer = csv.writer(open("sentiment_features_1_1.csv", "wb"))
csv_writer.writerow(word_features)

# using this
word_features_assembled = []
csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
for row in csv_reader:
    word_features_assembled.extend(row)

# read a csv to a list
word_features_assembled = []
csv_reader = csv.reader(open("sentiment_features_1_1.csv","rb"))
for row in csv_reader:
    word_features_assembled.append(row)
    
    
            #
        tweets = []
        reader = csv.reader(open('full-corpus.csv'), delimiter=',')
        for row in reader:
            tmp = nltk.word_tokenize(row[4])
            if (row[1] == 'positive' or row[1] == 'negative'):
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
