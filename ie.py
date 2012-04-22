import nltk
import re

IN = re.compile(r'.*\bin\b')
term = ""

class doc():
    pass

doc.headline = ['not applicable']

source_text = """
Charles is living in North Dakota. Hubert is visiting in New York. 
George was born in Great Britain. Hubert is visiting in Mexico City. I like cheese.
"""
question = "Where was George Washington born?"

taggedtokens = nltk.pos_tag(nltk.word_tokenize(question))
taggedtokens = nltk.pos_tag(nltk.word_tokenize(source_text))

# need to join all c[] for c in chunk.leaves()
def process_source(text):
    tokens = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(source_text))):
        if hasattr(chunk, 'node'):
            if chunk.node != 'GPE':
                tmp_tree = nltk.Tree(chunk.node, [(' '.join(c[0] for c in chunk.leaves()))])
            else:
                tmp_tree = nltk.Tree('LOCATION', [(' '.join(c[0] for c in chunk.leaves()))])
            tokens.append(tmp_tree)
            #entities.append(tmp_tree)
        else:
            tokens.append(chunk[0])
    return tokens

# print NEs
[chunk for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(source_text)))]

term = 'in'
PATTERN = re.compile(r'.*\b%s\b.*' % term)
# inconsistent behavior
for rel in nltk.sem.extract_rels('PERSON', 'LOCATION', doc, corpus='ieer', pattern=IN):
    print rel
    
    
relations = []

# where was george washington born?
# extract_rels('PERSON' (george washington), 'LOCATION' 
# (where -> location), ..., pattern=PATTERN %s term

question = "Where was George Washington born?"

def extract_subjclass(question):
    # need to pull NE from question
    return answer_subjclass

def extract_objclass(question):
    # need to determine NE type from question (where -> location)
    # select obj NE type with shortest path to question focus word?
    return answer_objclass
    
def extract_answer_pattern(question):
    # need to complete TERM for regex
    # 'where was gw born' -> term = 'born'
    # also create synonyms of 'born'
    return answer_pattern

# person, location, organization
def extract():
    for rel in nltk.sem.extract_rels('PERSON', 'LOCATION', doc, corpus='ieer', pattern=IN):
        tmp = rel['subjtext'] + " is in " + rel['objtext']
        relations.append(tmp)
        print relations

def process_question(question):
    doc.text = process_source(source_text)
    answer_subjclass = extract_subjclass(question)
    answer_objclass = extract_objclass()
    answer_pattern = extract_answer_pattern()
    for rel in nltk.sem.extract_rels(subjclass=answer_subjclass, objclass=answer_objclass,  doc=doc,  corpus='ieer',  pattern=answer_pattern):
        print rel

doc.text = process_source(question)
extract()
