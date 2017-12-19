#NER Tagging - Created on Thu Nov 30 09:59:55 2017

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

import sys

#print(len(sys.argv))

if(len(sys.argv) != 4):
    print ('Usage: Pass Arguments for Input Links File, Stanford Tagger Root Dir and Output Schema File')
    sys.exit(1)



print ("Input Links File Name & Path is " + sys.argv[1])
print ("Stanford Root Directory is " + sys.argv[2])
print ("Schema File Name & Path is " + sys.argv[3])

#Convert Stanford Tags to BIO/IOB Tags

def stTagToBIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O": #O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O": # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag: # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag

    return bio_tagged_sent

#Convert Stanford Tag Output to NLTK Tree Output for easier processing
def stTagToTree(ne_tagged_sent):
    bio_tagged_sent = stTagToBIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree

# 3-CLass Algorithm - english.all.3class.distsim.crf.ser.gz
# 7-CLass Algorithm - english.muc.7class.distsim.crf.ser.gz
# 4-Class Algorithm - english.conll.4class.distsim.crf.ser.gz

st7 = StanfordNERTagger(sys.argv[2] + '\\classifiers\\english.muc.7class.distsim.crf.ser.gz',
					      sys.argv[2] + '\\stanford-ner.jar',
					      encoding='utf-8')

st4 = StanfordNERTagger(sys.argv[2] + '\\classifiers\\english.conll.4class.distsim.crf.ser.gz',
					      sys.argv[2] + '\\stanford-ner.jar',
					      encoding='utf-8')


#Open Original Input Link File
inputLink = open(sys.argv[1], 'rb')
inputLines = inputLink.readlines()

#Open Output Schema File For Solr
schemafile = open(sys.argv[3], 'w')

# We are using a combination of 4-Class and 7-Class NER
# Tagging Model to get maximum schema elements for solr indexing
#Capture Person and Dates returned by the NER Tagger

for inputLine in inputLines :
    recid, fileid, category, linkLine = inputLine.decode('utf-8').split("|")
    print(category, linkLine)
    ner_tokenized_text = word_tokenize(linkLine)
    ner_classified_text7 = st7.tag(ner_tokenized_text)
    ner_classified_text4 = st4.tag(ner_tokenized_text)
    #print(classified_text)
    ner_tree7 = stTagToTree(ner_classified_text7)
    ner_tree4 = stTagToTree(ner_classified_text4)
    
    #print (ne_tree7)
    #print (ne_tree4)
    
    ne_in_sent = []
    personcnt = 0
    
    for subtree in ner_tree4:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            #ne_in_sent.append((ne_string, ne_label))
            if(ne_label == 'PERSON') :
                ne_in_sent.append(ne_string)
                #personcnt += 1
    
    #print (personcnt)
    
#    if(personcnt < 5 and personcnt != 4) :
#        i = 5-personcnt
#    elif (personcnt == 4):
#        i = 5 - personcnt
#    elif(personcnt == 5):
#        i = 0
    
    #print(i)
#    
#    for x in range(0, i):
#        ne_in_sent.append("NA")

    str2 = '#'.join(ne_in_sent)
    print(str2)
    ne_in_sent = []
    for subtree in ner_tree7:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            #ne_in_sent.append((ne_string, ne_label))
            if(ne_label == 'DATE') :
                ne_in_sent.append(ne_string)
    
    ne_in_sent.append(category)
    #print (ne_in_sent)
    
    str1 = '|'.join(ne_in_sent)
    #print(str1)
    
    str3 = str2 + "|" + str1
    print("String 3 IS " + str3)
    
    data = linkLine.split("Reflink:")
    strrest = ""
    for temp in data:
        strrest = temp.rstrip()
    
    schemafile.write(recid + "|" + str3 + "|" + strrest + "\n")
   

schemafile.close()
         
inputLink.close()