Software documentation for CS410 Fall 2017 Final Project
Project Title -  Information Extraction form MCSDS lecture material & Implementation of Search Engine. 

This project aims at capturing additional references & readings mentioned in the MSDS coursera course material
using python nltk modules and implementing a vertical search engine using Solr for easy reference and analysis.

->The main technology stacks used are listed below.
Python & NLTK Packages
The Python distribution used is WinPython3530Qt5 on 64bit.
Stanford NER - v3.8.0 - 2017-06-09 https://nlp.stanford.edu/software/CRF-NER.shtml#Download
Python NLTK version 3..2.5  package which is included in WinPython3530Qt5 64bit  distribution.
Additional NLTK packages – Averaged Perceptron Tagger ,Punkt Tokenizer Models,Stopwords Corpus 
pdfminer3k https://pypi.python.org/pypi/pdfminer3k/

->Solr & Banana Dashboards.
Solr version 6.5.1 is used for this project & Banana dashboard 1.6.7 is used as front end for search and analysing
data stored in solr.

->Development IDE used is Spyder 3.1.2 supplied along with WinPython3530Qt5 64bit.
Make sure JAVA_HOME is set to the appropriate jdk environment

->About the program ner_tagger.py
This program uses stanford ner entity extractor libraries to extract Person and Year from each of the reference links provided in the input file.Here we are using a combination of 4-Class and 7-Class NER Tagging Model to get maximum schema elements for solr indexing.
This program will call the stanford tagger (java libraries) and hence will take time to complete.The output of this program is a delimiter "|" separated file with data that confirms to the Solr Schema defined.This file is further indexed into solr using curl command.Below captured are the input argument and output argument for the program ner_tagger.py.The input for this file is a “|” separated .txt file which captures the following details (refer to the below image for sample).This input file is created manually by extracting the additional readings recommendations from each topic in the cs410 lecture pdf’s.(1)ID-For the mandatory define Solr document ID. This is also used later for atomic updates further during the second index run.(2)File name where the addition reading material was observed. Note that this field has a .txt mentioned as the file name only because this same input file is used during the next phase of the classification program (will be clear in the coming slides).(3)main_category of this link/additional references and is classified manually.(4)This is the main additional reference material found in the respective course lecture slides . The NER tagger uses this to derive the Author & Year attributes.Input to the program is the file with links and ID and the root to the stanford ner installs.e.g. C:\\CS410\\finalproject\\input_links_with_cats_and_ids.txt C:\\CS410\\finalproject\\stanford-ner-2017-06-09 e.g Output from the program is C:\CS410\finalproject\firsttoindex.txt.All the above three arguments are provided to the program ner_tagger.py.

->Indexing Data into Solr.
The above output can be indexed into solr using curl command and 've used cygwin for the same.Since the output file contains the multivalued field author appropriate commands need to be used for indexing.
e.g. $curl 'http://localhost:8983/solr/cs410/update?commit=true&separator=%7C&f.author.split=true&f.author.separator=%23' --data-binary @Firsttoindex.txt -H 'Content-type:application/csv' For more details refer solr csv index handler in the solr product manuals.

->About the program raw_corpus_creation.py
The field sub_category is derived by implementing the NB classifier and this programs is a prestep.This program generates the
raw corpus text data from the course pdf's so that the classification program can use this data.PDF Miner3k libr.aries are
is used to scan for all the PDFs where the strings “Suggested Reading” or “Additional Reading "occurs and for such Lecture slides all the contents are read and written into respective text file in the output directory.Input argument to the program is e.g. location C:\\CS410\\finalproject\\coursepdfs .The course pdfs considered are uploaded into the core repository.

->About the the program corpus_classify.py
This program takes the respective inputs (arguments) and the contents extracted to classify the files & thus the links/additional reading materials into pre-defined category.Simple NB for multiclass classification is used and the categorized corpus is created based on category/file id mapping.Initial / Pre-Defined Features for Test and Train Hardcoded as a List of Tuples and Naive Bayes Classifier is used on Pre-Defined Feature Train List of Tuples.Further Classifier is updated with Train data information for increasing training accuracy and accuracy is calculated.Looping thorough each dataset in the corpusprobability of a category based on entire corpus dataset is calculated.Only category that had a probability of more than 50% is considered.Cross-Referenced ROW ID's from the Original input links file and created a final sub-category file adding Row ID and Derived Category for updating into solr.

->Input arguments are detailed below.
1)Location / Path to Directory where Input Coursera PDFs are stored – First Argument e.g “C:\\CS410\\finalproject\\coursepdfs”
2)Path to File (along with File Name) containing Category and Input File ID (Text File from Raw Corpus) Mapping delimited using “|” – Second Argument.e.g “C:\\CS410\\finalproject\\cats2.txt”
3)Path to File (along with File Name) containing details of Reference Links along with Primary Categories and Record ID delimited using “|"– Third Argument
4)Path To Output file where final Derived Sub-Category will be written along with Record ID – Fourth Argument e.g "C:\\CS410\\finalproject\\secondtoindex.txt" Examples of the input and output files and available in the code repository.

->Updating Solr Index for the value sub_category.
From the above classification program we get the values of sub_category for the respective ID(same as solr document ID).This is used for atomic updates into Solr by converting the output into a json format, the solr admin tool document submit is used for these index update. e.g {"id":"1012","sub_category":{"set":"IR Models- Evaluation,Ranking & Feedback"}}
The file secondtoindex_json uploaded into the repository captures these details.

->Banana Dashboards
Pls refer to the documentation for details on the install of banana webapp into solr. Once installed you can point to the appropriate Solr collection and create a non-time series dashboard that will facilitate search and faceted data analysis.Usecases implemented as part of the this project include keyword search for the additional reading references and analysis (facets) regarding the author and year of publication.e.g The preconfigured cs410 dashboard definition example is provided in the code repository which can be loaded to explore more.









