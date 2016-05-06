"""This class implements Named Entity Recognition (NER) as a MapReduce Job.
It uses NLTK to perform the actual NER through the Stanford NER.

"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
# from datetime import datetime
from lxml import etree, objectify
import uuid
import os
import httplib
import base64

# use a different JRE: need 8 for this, Hadoop installation currently requires 7
java_path = "/usr/local/java/jre1.8.0_73/bin/java"  # only for earkdev
os.environ['JAVAHOME'] = java_path                  # only for earkdev

M = objectify.ElementMaker(annotate=False)

class MRNamedEntityRecognition(MRJob):
    def init_ner_mapper(self):
        # load the StanfordNER Tagger
        # model_ger = "/opt/Projects/nlp/stanford-ner-2015-04-20/classifiers" \
        #             "/german/german.hgc_175m_600.crf.ser.gz"
        # stanford_jar = "/opt/Projects/nlp/stanford-ner-2015-04-20/stanford" \
        #                "-ner.jar"
        model_ger = "/home/janrn/ner/german.hgc_175m_600.crf.ser.gz"   # earkdev
        stanford_jar = "/home/janrn/ner/stanford-ner.jar"              # earkdev

        self.tagger = StanfordNERTagger(model_ger, stanford_jar,
                                        encoding="utf-8",
                                        java_options='-mx4096m',
                                        )
        # timestamp
        # yield "TIME INIT", datetime.utcnow().__str__()

    def ner_mapper(self, _, mapper_input):
        # TODO: read from Lily, not local filesystem
        # with open("/opt/Projects/EARK/dm-nlp/entities/%s" % mapper_input) as \
        #         file_in:
        with open(mapper_input) as file_in:     # earkdev
            tokenized = []
            for line in file_in:
                line = line.strip().decode("utf-8")
                tokens = word_tokenize(line, language="german")  # TODO: use
                # nltk.tokenize.stanford module?
                for token in tokens:
                    tokenized.append(token + "\n")
            position = 0
            for result in self.tagger.tag(tokenized):
                position += 1
                if result[1] != "O":
                    # use source (input) file as key, values are NER results
                    yield mapper_input, {"position": position,
                                         "class": result[1],
                                         "entity": result[0]}

    def ner_reducer(self, key, values):
        # TODO: this currently creates one XML "file" per input line. Keep it
        #  like this, or combine it?
        if key:
            root = M.file({'FILE': key,
                           'LABEL': 'NER results'})
            for val in values:
                # print v.encode("utf-8")
                entity = M.entity(val)
                root.append(entity)

        # create an XML string:
        xml = etree.tostring(root, encoding='UTF-8',
                             pretty_print=True,
                             xml_declaration=True)
        xml_id = uuid.uuid4().__str__()

        # ingest it into eXist:
        con = httplib.HTTP('earkdev.ait.ac.at')
        con.putrequest('PUT', '/exist/apps/eark/nlp/%s' % xml_id)
        con.putheader('Content-Type', 'application/xml')
        clen = len(xml)
        con.putheader('Content-Length', `clen`)
        con.putheader('Authorization', 'Basic %s' % base64.b64encode(
            'nlp-user:earknlp'))
        con.endheaders()
        con.send(xml)
        errcode, errmsg, headers = con.getreply()
        if errcode != 200:
            f = con.getfile()
            with open('/home/janrn/ner/http.err', 'w') as errfile:
                errfile.write(errmsg)
        else:
            pass

        # output: file id
        yield "NER_RESULT", xml_id

    # additional processing steps:
    # calculate tf-idf score after ner_reducer finished? - need whole corpus
    # for it, so it needs to be before the XML step?
    # geocoding?

    def steps(self):
        return [MRStep(mapper_init=self.init_ner_mapper,
                       mapper=self.ner_mapper,
                       reducer=self.ner_reducer)]


if __name__ == '__main__':
    MRNamedEntityRecognition.run()
