tokens = []
for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(source_text))):


# need to join all c[] for c in chunk.leaves()
tokens = []
for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(source_text))):
    print chunk
    if hasattr(chunk, 'node'):
        print chunk.leaves()
        if chunk.node != 'GPE':
            tmp_tree = nltk.Tree(chunk.node, [(' '.join(c[0] for c in chunk.leaves()))])
        else:
            tmp_tree = nltk.Tree('LOCATION', [(' '.join(c[0] for c in chunk.leaves()))])
        tokens.append(tmp_tree)
    else:
        tokens.append(chunk[0])
