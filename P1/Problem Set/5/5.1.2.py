import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Given the output of the mapper for this exercise, the reducer should PRINT 
    (not return) one line per UNIT along with the total number of ENTRIESn_hourly 
    over the course of May (which is the duration of our data), separated by a tab.
    An example output row from the reducer might look like this: 'R001\t500625.0'

    You can assume that the input to the reducer is sorted such that all rows
    corresponding to a particular UNIT are grouped together.

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    Note that, unlike print, logging.info will take only a single argument.
    So logging.info("my message") will work, but logging.info("my","message") will not.
    '''

    entries = 0
    old_key = None

    for line in sys.stdin:
        data = line.strip().split("\t")
        
        logging.info(data)

        if len(data) != 2:
            continue
        
        this_key, count = data
        if old_key and old_key != this_key:
            print "{0}\t{1}".format(old_key, entries)
            entries = 0

        old_key = this_key
        entries += float(count)

    print("{0}\t{1}".format(old_key, entries))
reducer()
