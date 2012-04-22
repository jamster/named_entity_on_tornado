import nltk
import re

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'why', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

class doc():
    pass
    
doc.headline = ['not applicable']

IN = re.compile(r'.*\bin\b')
# any relation unless it contains a period
ANY = re.compile(r'(?!\.)')


source_text = """
Charles is living in North Dakota. Hubert is visiting in New York. 
John Doe works at Microsoft. Samuel Jones is friends with Mike Austin. Intel, Inc. is located in southern Canada.
George was born in Great Britain. Hubert is visiting in Mexico City. I like cheese. 
Bob Smith is going to Europe. Bob Smith.  Europe.
"""

def process_source(source_text):
    tokens = []
    for sentence in nltk.sent_tokenize(source_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
            print chunk
            if hasattr(chunk, 'node'):
                if chunk.node != 'GPE':
                    tmp_tree = nltk.Tree(chunk.node, [(' '.join(c[0] for c in chunk.leaves()))])
                else:
                    #print chunk.leaves()
                    tmp_tree = nltk.Tree('LOCATION', [(' '.join(c[0] for c in chunk.leaves()))])
                tokens.append(tmp_tree)
            else:
                tokens.append(chunk[0])
    return tokens
    
def process_source(source_text):
    tokens = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(source_text))):
        print chunk
        if hasattr(chunk, 'node'):
            if chunk.node != 'GPE':
                tmp_tree = nltk.Tree(chunk.node, [(' '.join(c[0] for c in chunk.leaves()))])
            else:
                #print chunk.leaves()
                tmp_tree = nltk.Tree('LOCATION', [(' '.join(c[0] for c in chunk.leaves()))])
            tokens.append(tmp_tree)
        else:
            tokens.append(chunk[0])
    return tokens
    
relations = []

def extract():
    #relations = []
    relation_phrases = []
    for rel in nltk.sem.extract_rels('PERSON', 'LOCATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('PERSON', 'ORGANIZATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('PERSON', 'PERSON', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)   
    for rel in nltk.sem.extract_rels('ORGANIZATION', 'LOCATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('ORGANIZATION', 'PERSON', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('ORGANIZATION', 'ORGANIZATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('LOCATION', 'PERSON', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('LOCATION', 'ORGANIZATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for rel in nltk.sem.extract_rels('LOCATION', 'LOCATION', doc, corpus='ieer', pattern=ANY):
        tmp = rel['subjtext'] + ' ' + rel['filler'] + ' ' + rel['objtext']
        relations.append(rel)
        relation_phrases.append(tmp)
    for relation_phrase in relation_phrases:
        print relation_phrase
    return relation_phrases
    
doc.text = process_source(source_text)
relation_phrases = extract()



question = "What did Washington preside over?"
question_tokens_filtered = [token for token in nltk.word_tokenize(question) if not token in stop_words]

phrase_tokens_filtered = []

for relation_phrase in relation_phrases:
    phrase_tokens_filtered = [token for token in nltk.word_tokenize(relation_phrase) if not token in stop_words]
    common_tokens = [token for token in question_tokens_filtered if token in phrase_tokens_filtered]
    print common_tokens

        

        
# for q word, if in relation phrase add point to relation phrase
# for word in q, get lemmas. if lemma in relation phrase, add .5 to relation phrase
# for word in q, get hypernyms. if hypernym lemmas in relation phrase add .25 to relation phrase
# relation phrase with the highest score wins

# chunk and remove stopwords
tagged_question  = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(question)))

filtered_words = [w for w in word_list if not w in stopwords.words('english')]




source_text = """
Florida Senator Marco Rubio is indisputably one of the brightest stars of the Republican firmament– a young, Tea Party-backed Senator with a compelling life story and the sort of rhetorical skills that get him compared to the last young sensation our upper congressional chamber gave us, President Barack Obama. He is eloquent in both the our nation’s major languages, reasonable enough to denounce his side’s more entertaining loons, and, with more experience, potentially unstoppable as a presidential contender. So why do Republicans want to irreparably destroy his career by associating him with jelly-spined bore Mitt Romney? 

RELATED: Watch Sen. Marco Rubio Save Nancy Reagan From Falling After Losing Her Balance

Unfortunately for Sen. Rubio, his charm, eloquence, and actual ability on the job (he just returned from the Summit of the Americas, the only Senator invited by the President) have caught the attention of this generation’s convictionless Massachusetts Scrooge McDuck, Mitt Romney. Or at least it has caught the attention of everyone who wants to see Romney win the presidency. Sen. Rubio has been contemplated as a potential vice presidential running mate since his election, but it was only until recently that the clamor rose to deafening levels.

On his end, Sen. Rubio has said no. He said no, thank you, to the idea of being Vice President. He said no to Soledad O’Brien. He said no to Juan Williams. He said no to George Stephanopoulos. He said no to the Washington Ideas Forum. He said no to CNN en Español’s Ismael Cala (in Spanish this time). He will probably say no tomorrow to Candy Crowley.

So those of us who wish to seem him evolve as a legislator before growing into a respected, gray-haired public figure should feel relatively safe. Except even he can’t contain how cool it would be to be a heartbeat away from the most powerful job in the world forever. “When I’m Vice President, Rubio told a crowd this week, before catching himself and erupting into laughter. He claims he was trying to say anything can happen as he evolves as a Senator, but this was the perfect tease for those who hope to see the 2012 Republican ticket enjoy a modicum of personality, and the speculation erupted once more. This time, even perennial phantom candidate Jeb Bush came out of the shadows to suggest to Romney that Sen. Rubio was the perfect candidate. The only two Republicans who seem to object to this idea that Rubio would be the perfect counterweight to Romney– the Oscar to Romney’s Felix– are Ann Coulter and Marco Rubio, and even Rubio faltered.

Ann Coulter has her reasons to object to the choice. For one, she is not exactly shy about her undying ideological love of New Jersey Governor Chris Christie. She has also said the choice, if exclusively based on his ethnicity, would be “pandering,” and expressed worry that he was too young and unvetted before the national media. “When you run as a Republican for President or Vice President, the non-Fox media is going to go after you like gangbusters and it’s good to have somebody who is tested,” she told O’Reilly a few weeks ago.

Her bias for Fox aside, the wisdom of that statement cannot be overstated. Sen. Rubio is young, charismatic, likeable– the only person in America that can legitimately talk about communism without turning it into a complete joke (sorry, Allen West). His DREAM Act proposals are moderate and empathetic towards immigrants and exiles alike. His comments on abortion can move almost anyone to tears. But none of this has anything to do with his past, with his viability before a media that has already questioned his personal childhood narrative and tried to brand him a Mormon, as if that were some sort of liability. He may prove resilient, but resilience takes time to build, and Marco Rubio is, in political years, a toddler.

What Coulter let escape from her assessment is that the potential liability of bringing Rubio onto the ticket for Romney cuts both ways (perhaps she would have been more open to admitting this in the days when she preached unity behind Christie, else “we’ll end up with Romney and we will lose).” Rubio is bright, charismatic, passionate, and, from all appearances, honest. In other words, Rubio is everything that Mitt Romney is not, and associating with Romney puts everything there is to like about Rubio in doubt. If Marco Rubio is so charismatic, what is he doing as subordinate to a guy who can’t even properly compliment a cookie? If he is so steadfast in his beliefs, why do Republicans think he should be second fiddle to the Father of Romneycare (and by proxy, grandfather of Obamacare, a program he disowns)?

Republicans will poo-poo this train of thought, however, because they are banking on Romney to win. A quick look at the polls shows that there is no reason not to doubt the possibility of Romney winning. But winning won’t erase any of these problems with Romney’s resume. In fact, given the compromises heads of state must often make, being president will likely enhance the reputation Romney has for having no true convictions or passions aside from power. Even if Romney does end up rehabilitating his conservative street cred, he would still end up being the least exciting presidential personality since Millard Fillmore– once again, the antithesis of everything that makes Rubio a compelling leader. Running with four years of being second in command to the guy who can’t even commit on the idea that these pancakes are delicious is serious baggage compared to the possibility of a Romney-free Republican Presidential candidate Marco Rubio in 2016– the Senator potentially behind making the DREAM Act work and, given the increasingly rapid dissolution of the regime in his parents’ home country, possibly one of the most influential figures in the rehabilitation of the Cuban state. 2016 is a long time away, and many great things can happen in Sen. Rubio’s career, none of which are possible while holding a job the current incumbent admits he does absolutely nothing in.

Mitt Romney has a chance of being President, as does Marco Rubio. But their chances are deadlocked in a zero sum game– they have nothing to gain from each other, and everything to lose. And Republicans can’t afford to drown their brightest talent in their murkiest mediocrity.
"""
    
    
    
    
    
    
    
    
    
    
    
