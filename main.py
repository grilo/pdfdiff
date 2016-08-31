#!/usr/bin/env python

import logging
import optparse
import sys
import os

import finder
import reporter


def print_help():
    print "Generates a 'diff' directory containing only the files which were modified."
    print "The rest of the changes is simply printed in ASCII."
    pass

if __name__ == '__main__':

    log_format = '%(asctime)s::%(levelname)s::%(message)s'
    log_level = 'DEBUG'
    logging.basicConfig(format=log_format)
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))


    usage = "usage: %prog <old dir> <new dir>"
    parser = optparse.OptionParser(usage)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        logging.critical("Invalid number of parameters, at least two directories are expected.")
        parser.print_help()
        sys.exit(1)

    for a in args:
        if not os.path.isdir(a):
            logging.critical("This parameter isn't a valid directory: %s" % (a))
            parser.print_help()
            sys.exit(1)

    if not args[0].endswith("/"):
        args[0] += "/"
    if not args[1].endswith("/"):
        args[1] += "/"

    results = finder.compare_pdf_dirs(args[0], args[1])

    reporter.generate_report(results)
