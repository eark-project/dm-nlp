# set NLTK_DATA for cluster nodes
from nltk import data
data.path.append('/opt/nltk_data')
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
from lxml import etree, objectify
# import uuid
# import httplib
# import base64
import sys
import os
import requests
import time


# use a different JRE: need Java 8 for this, Hadoop installation uses 7
# java_path = '/usr/local/java/jre1.8.0_73/bin/java'  # only for earkdev
# os.environ['JAVAHOME'] = java_path                  # only for earkdev
java_path = '/opt/jdk1.8.0_65/bin/java'     # cluster
os.environ['JAVAHOME'] = java_path          # cluster

# read all arguments
if sys.argv[1] == 'ger':
    nerModel = '/opt/anaconda-scripts/german.hgc_175m_600.crf.ser.gz'
elif sys.argv[1] == 'hun':
    nerModel = '/opt/anaconda-scripts/hungarian-gazettes-352.ser.gz'
# inputFile = sys.argv[2]
inputUrl = str(sys.argv[2])
stanfordJar = '/opt/anaconda-scripts/stanford-ner-3.5.2.jar'

# initialize the NER tagger
tagger = StanfordNERTagger(nerModel, stanfordJar,
                           encoding='utf-8',
                           java_options='-mx4096m')

# prepare XML structure
M = objectify.ElementMaker(annotate=False)
root = M.file({'FILE': 'placeholder for a name',
               'LABEL': 'NER results'})

# open input file
# with open(inputFile, 'r') as nerInput:
#     # first tokenize the input file
#     tokenized = []
#     for line in nerInput:
#         line = line.strip()
#         tokens = word_tokenize(line, language='german')
#         # tokens = word_tokenize(line)
#         for token in tokens:
#             tokenized.append(token + '\n')
#     position = 0
#
#     # second, tag the input file
#     for result in tagger.tag(tokenized):
#         position += 1
#         if result[1] != 'O':
#             # if not 'other', we want to store it
#             # print result
#             entity = M.entity({'position': position,
#                                'class': result[1],
#                                'entity': result[0]})
#             root.append(entity)
#         # root.append(result)

r = requests.get(inputUrl)  # works because input is in " "
time.sleep(1)
# print('STATUS CODE: %d' % r.status_code)
# print(r.json())
inputText = r.json()['response']['docs'][0]['content']
tokenized = []

# for line in inputText:
#     line = line.strip()
#     tokens = word_tokenize(line)
#     for token in tokens:
#         tokenized.append(token + '\n')
for token in word_tokenize(inputText):
    tokenized.append(token + '\n')
position = 0

for result in tagger.tag(tokenized):
    position += 1
    if result[1] != 'O':
        entity = M.entity({'position': position,
                           'class': result[1],
                           'entity': result[0]})
        root.append(entity)

# create an XML string:
xml = etree.tostring(root, encoding='UTF-8',
                     pretty_print=True,
                     xml_declaration=True)
# xml_id = uuid.uuid4().__str__()

print(xml)

# # ingest it into eXist:
# con = httplib.HTTP('earkdev.ait.ac.at')
# con.putrequest('PUT', '/exist/apps/eark/nlp/%s' % xml_id)
# con.putheader('Content-Type', 'application/xml')
# clen = len(xml)
# con.putheader('Content-Length', `clen`)
# con.putheader('Authorization', 'Basic %s' % base64.b64encode(
#     'nlp-user:earknlp'))
# con.endheaders()
# con.send(xml)
# errcode, errmsg, headers = con.getreply()
# if errcode != 200:
#     f = con.getfile()
#     with open('/home/janrn/ner/http.err', 'w') as errfile:
#         errfile.write(errmsg)
# else:
#     pass
