#!/usr/bin/python

import sys
import subprocess
# import os

try:
    from sklearn.externals import joblib
except:
    e = sys.exc_info()[0]
    sys.exit(e)

'''
This script takes the input from sys.argv and performs text categorization.
IMPORTANT: Since anaconda is a requirement to use this, this code is written
in Python 3 syntax.
'''

class TextClassifier(object):
    def __init__(self, model):
        # TODO: maybe load the categories dynamically from an external file? -> third/fourth cmd line parameter?
        self.categories = ['AutoMobil', 'Bildung', 'Etat', 'Familie', 'Finanzen', 'Gesundheit', 'Greenlife',
                           'Immobilien', 'Inland', 'International', 'Karriere', 'Kultur', 'Lifestyle', 'Meinung',
                           'Panorama', 'Politik', 'Reise', 'Sport', 'Stil', 'Technik', 'Web', 'Wirtschaft', 'Wissenschaft']
        try:
            self.clf = joblib.load(model)
        except:
            e = sys.exc_info()[0]
            print('[ERROR]\tError when loading model: %s' % e)
            sys.exit('[ERROR] Error when loading model: %s' % e)

    def categorize(self, tmpFile):
        try:
            cat = subprocess.Popen(['hadoop', 'fs', '-cat', tmpFile],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            text = ''
            for line in cat.stdout:
                text += line.decode('utf-8')

            # confidence = self.clf.decision_function(text)
            # cat.stdout.close()

            # with open(tmpFile, 'r') as clfInput:
            #     confidence = self.clf.decision_function(clfInput.readlines())
        except:
            e = sys.exc_info()[0]
            print('[ERROR]\tException when trying to get the confidence ratings: %s' % e)
            sys.exit('[ERROR] Exception when trying to get the confidence ratings: %s' % e)

        # try:
        #     result = confidence[0].tolist()
        #
        #     # get category with highest confidence rating
        #     max_value = float(max(result))
        #     max_value_index = result.index(max_value)
        #
        #     # get second highest confidence rating
        #     result[max_value_index] = -2
        #     second_value = float(max(result))
        #     second_value_index = result.index(second_value)
        #
        #     # print '---------- File: %s' % text
        #     # print 'Highest confidence: %f for category <%s>.' % (max_value, categories[max_value_index])
        #     # print 'Second highest confidence: %f for category <%s>.' % (second_value, categories[second_value_index])
        #
        #     primary = self.categories[max_value_index]
        #     secondary = self.categories[second_value_index]
        # except:
        #     e = sys.exc_info()[0]
        #     sys.exit('[ERROR] Computing confidence rating failed: %s' % e)
        primary = 'primary'
        secondary = 'secondary'

        return primary, secondary


if __name__ == '__main__':
    try:
        # only two arguments on the cluster (no input_id)
        model = sys.argv[1]
        # input_id = sys.argv[2]
        # input_file = sys.argv[3]
        input_file = sys.argv[2]
    except:
        e = sys.exc_info()[0]
        print('[ERROR]\tWrong input format: %s' % e)
        sys.exit('[ERROR] Wrong input format: %s' % e)

    # currently not needed, files are created by the Mapper
    # try:
    #     # create a temporary file to feed to the classifier; will be deleted afterwards
    #     # (needed because the classifier always goes one level "below" input: string -> words, file -> file content)
    #     tmpId = uuid.uuid4().__str__()
    #     with open('/tmp/%s' % tmpId, 'w') as tmp:
    #         tmp.write(input_text)
    # except Exception, e:
    #     sys.exit('[ERROR] Failed to create the tmp file: %s' % e)

    classifier = TextClassifier(model)

    # classify the input - should be text only
    # TODO: discuss input format
    try:
        # primary, secondary = classifier.categorize('/tmp/clfin/%s' % input_file)
        primary, secondary = classifier.categorize(input_file)
        print('%s\t%s, %s' % ('categories', primary, secondary))
        # print('test\t%s' % input_file)
        # delete the tmp file as it is no longer needed
        # os.remove('/tmp/clfin/%s' % input_file)
    except:
        e = sys.exc_info()[0]
        print('[ERROR]\tError when calling the classifier with input: %s' % e)
        sys.exit('Error when calling the classifier with input: %s' % e)