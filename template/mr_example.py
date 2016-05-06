"""Example structure of Python mrjob usage.
"""

from mrjob.job import MRJob

# in case you need JRE 8, uncomment this
# java_path = "/usr/local/java/jre1.8.0_73/bin/java"  # only for earkdev
# os.environ['JAVAHOME'] = java_path                  # only for earkdev


class MRExample(MRJob):

    def mapper(self, _, mapper_input):
        # mapper_input is one line from the input file
        yield key, value

    def reducer(self, key, values):
        # input is already grouped by keys
        # output of this can be anything you want - will be in the terminal
        yield key, value

    # if you need more reducers/combiners etc:
    # https://pythonhosted.org/mrjob/guides/writing-mrjobs.html#defining-steps

if __name__ == '__main__':
    MRExample.run()
