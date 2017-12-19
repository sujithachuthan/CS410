#Corpus Classification

from nltk.corpus.reader import CategorizedPlaintextCorpusReader


import sys

if(len(sys.argv) != 5):
    print ('Usage: Pass Arguments for Input PDF path, Category-File Mapping Path, Input Links File and Output Sub-Category Update File')
    sys.exit(1)

print ("Input PDFs File Path " + sys.argv[1])
print("Category File Name and Path " + sys.argv[2])
print ("Input Links File Name & Path is " + sys.argv[3])
print ("SubCategory Update File is " + sys.argv[4])

reader = CategorizedPlaintextCorpusReader(sys.argv[1], r'.*\.txt', cat_file=sys.argv[2], cat_delimiter='|')


# Access each file in the corpus.
#for infile in sorted(reader.fileids()):
#    print (infile) # The fileids of each file.
#    #file = reader.open(infile)
#    #print (file.read().strip()) # Prints the content of the file

#print(reader.fileids())

#print(reader.fileids(categories=['General']))
#print(reader.categories())

#print(reader.categories())


### Access the plaintext; outputs pure string/basestring.
#print (reader.raw().strip())

##print 
##
### Access paragraphs in the corpus. (list of list of list of strings)
### NOTE: NLTK automatically calls nltk.tokenize.sent_tokenize and 
###       nltk.tokenize.word_tokenize.
###
### Each element in the outermost list is a paragraph, and
### Each paragraph contains sentence(s), and
### Each sentence contains token(s)
#print (reader.paras())
##print
###
#### To access pargraphs of a specific fileid.
#print (reader.paras(reader.fileids()[0]))
###
#### Access sentences in the corpus. (list of list of strings)
#### NOTE: That the texts are flattened into sentences that contains tokens.
#print (reader.sents())
###print
###
#### To access sentences of a specific fileid.
#print (reader.sents(reader.fileids()[0]))
###
#### Access just tokens/words in the corpus. (list of strings)
#print (reader.words())
###
#### To access tokens of a specific fileid.
#print (reader.words(reader.fileids()[0]))
#
#print("Categories are \n")
#print(reader.categories())

import random
from textblob.classifiers import NaiveBayesClassifier
import string

random.seed(1)

from nltk import word_tokenize
#from nltk.stem.porter import PorterStemmer
#import re
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")

#Simple Tokenizer Function without Stemmer
#Stemmer is making words lowecase reducing accuracy
def tokenize(text):
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    
    word_tokens = word_tokenize(text)
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
        
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words :
            filtered_sentence.append(w)
    return filtered_sentence

#def tokenize(text):
#    min_length = 3
#    words = map(lambda word: word, word_tokenize(text));
#    words = [word for word in words
#                  if word not in cachedStopWords]
#    tokens =(list(map(lambda token: PorterStemmer().stem(token),
#                  words)));
#    p = re.compile('[a-zA-Z]+');
#    filtered_tokens = list(filter(lambda token:
#                  p.match(token) and len(token)>=min_length, tokens));
#        
#    return filtered_tokens

#Preparing a Tuple List of the Corpus Data based on
#Words In the corpus file and correspoindg category
data = [(list(tokenize(' '.join(reader.words(fileid)))), category)
              for category in reader.categories()
              for fileid in reader.fileids(category)]

#First preparing a train data set based on pre-identified features

featureListTrain = [ ('Natural Language Processing', 'General'),
                  ('Text Retrieval', 'General'),
                ('Text Access', 'General'),
                ('Information Retrieval', 'General'),
                ('NLP', 'General'),
                ('Content Analysis', 'General'),
                ('Vector', 'IR Models & Implementations'),
                ('Length', 'IR Models & Implementations'),
                ('Indexing', 'IR Models & Implementations'),
                ('Statistical', 'IR Models & Implementations'),
                ('Evaluation', 'IR Models- Evaluation,Ranking & Feedback'),
                ('Feedback', 'IR Models- Evaluation,Ranking & Feedback'),
                ('Ranking', 'IR Models- Evaluation,Ranking & Feedback'),
                ('Recommender', 'IR Models- Evaluation,Ranking & Feedback'),
                ('Filtering', 'IR Models- Evaluation,Ranking & Feedback'),
                ('Relations', 'Relationship Discovery'),
                ('Discovery', 'Relationship Discovery'),
                ('discovered', 'Relationship Discovery'),
                ('Syntagmatic', 'Relationship Discovery'),
                ('syntagmatic', 'Relationship Discovery'),
                ('paradigmatic', 'Relationship Discovery'),
                ('Entropy', 'Relationship Discovery'),
                ('distribution', 'Relationship Discovery'),
                ('collocations', 'Relationship Discovery'),
                ('Topic Models', 'Topic Models,Clustering & Categorization'),
                ('LDA', 'Topic Models,Clustering & Categorization'),
                ('PLSA', 'Topic Models,Clustering & Categorization'),
                ('Clustering', 'Topic Models,Clustering & Categorization'),
                ('Categorization', 'Topic Models,Clustering & Categorization'),
                ('Sentiment', 'Opinion Mining & Sentiment Analysis'),
                ('Latent', 'Opinion Mining & Sentiment Analysis'),
                ('Opinion', 'Opinion Mining & Sentiment Analysis'),
                ('Prediction', 'Contextual Text Mining'),
                ('Contextual', 'Contextual Text Mining'),
                ('CPLSA', 'Contextual Text Mining'),
                ('Mixture', 'Contextual Text Mining')
    ]

#First preparing a test data set based on pre-identified features
featureListTest = [ ('Natural Language Processing', 'General'),
                    ('Text Retrieval', 'General'),
                    ('Information Retrieval', 'General'),
                    ('Indexing', 'IR Models & Implementations'),
                    ('Statistical', 'IR Models & Implementations'),
                    ('Evaluation', 'IR Models- Evaluation,Ranking & Feedback'),
                    ('Feedback', 'IR Models- Evaluation,Ranking & Feedback'),
                    ('Ranking', 'IR Models- Evaluation,Ranking & Feedback'),
                    ('Relations', 'Relationship Discovery'),
                    ('Discovery', 'Relationship Discovery'),
                    ('distribution', 'Relationship Discovery'),
                    ('Syntagmatic', 'Relationship Discovery'),
                    ('syntagmatic', 'Relationship Discovery'),
                    ('Entropy', 'Relationship Discovery'),
                    ('Probabilities', 'Relationship Discovery'),
                    ('paradigmatic', 'Relationship Discovery'),
                    ('collocations', 'Relationship Discovery'),
                    ('Topic Models', 'Topic Models,Clustering & Categorization'),
                    ('LDA', 'Topic Models,Clustering & Categorization'),
                    ('PLSA', 'Topic Models,Clustering & Categorization'),
                    ('Clustering', 'Topic Models,Clustering & Categorization'),
                    ('Latent', 'Opinion Mining & Sentiment Analysis'),
                    ('Opinion', 'Opinion Mining & Sentiment Analysis'),
                    ('Prediction', 'Contextual Text Mining'),
                    ('Contextual', 'Contextual Text Mining')
            ]

#Instantiating the NB Classifier - Simple
classifier = NaiveBayesClassifier(featureListTrain)

#Random Shuffling of data for consistency
random.shuffle(data)

#print(str(data[0][1]).split('::'))

#Split Corpus data into train and test datasets
train, test = data[0:10], data[11:23]

#Update Classifier with new corpus data
classifier.update(train)

# Compute accuracy
accuracy = classifier.accuracy(featureListTest + test + data)
print("Accuracy: {0}".format(accuracy))


catList = []

# Loop through Corpus Data and Classify on entire dataset
# We do not have a large dataset and hence to get maximum categories classified
# the entire data is being considered
#If probablity of classification is at least 0.5 then capture the category
i = 0
while i < len(data):
    pdist = classifier.prob_classify(str(data[i][0]))
    #for category in reader.categories():   
    #print('%.4f %4f %4f %4f %4f %4f %4f' % (pdist.prob('General'),pdist.prob('IR Models & Implementations'),pdist.prob('IR Models- Evaluation,Ranking & Feedback'),pdist.prob('Relationship Discovery'), pdist.prob('Topic Models,Clustering & Categorization'),pdist.prob('Opinion Mining & Sentiment Analysis'), pdist.prob('Contextual Text Mining')))
    for category in reader.categories():
        if(pdist.prob(category) > 0.500000):
            #print(','.join(reader.fileids(str(data[i][1]))) + "::" + str(data[i][1]) + "::" + '%.4f' % (pdist.prob(str(data[i][1]))))
            catList.append(','.join(reader.fileids(category)) + "::" + category)
            #break
    i += 1
   
#Removing Duplicate entries from the captured list
uniqCatList = list(set(catList))
#print(uniqCatList)

#Opening The original Input Link File for Record ID
inputLink = open(sys.argv[3], 'rb')
inputLines = inputLink.readlines()

#Opening the Sub-Category Final Output file
subCatOut = open(sys.argv[4], 'w')

#Parallel Looping on Input Link File and Classified Category List
j = 0
while j < len(uniqCatList):
    fileids, subcategory = str(uniqCatList[j]).split('::')
    finalfileid = fileids.split(',')
    for inputLine in inputLines :
        recid, inpfileid, category, linkLine = inputLine.decode('utf-8').split("|")
        for fileidfin in finalfileid:
            if (fileidfin == inpfileid) :
                #print(recid + "::" + fileidfin + "::" + subcategory)
                subCatOut.write(recid + "|" + subcategory + "\n")
    j += 1
    
# Show most informative features
#classifier.show_informative_features()

inputLink.close()
subCatOut.close()
