#!/usr/bin/env python

import logging
import argparse
import sys
import os

import finder
import reporter
import diff


def print_help():
    print "Generates a 'diff' directory containing only the files which were modified."
    print "The rest of the changes is simply printed in ASCII."

if __name__ == '__main__':
    supported_formats = ['png', 'gif']

    log_format = '%(asctime)s::%(levelname)s::%(message)s'
    log_level = 'DEBUG'
    logging.basicConfig(format=log_format)
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))

    usage = "usage: %prog [ -v | -e <extension> | -f <filter> ] <old dir> <new dir>"
    parser = argparse.ArgumentParser(usage)
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("-e", "--extension", default='gif', help='The output format for the diffs (%s).' % (supported_formats))
    parser.add_argument("-f", "--filter", default='pdf', help='The files to look for.')
    parser.add_argument("old_dir", help="The directory considered old.")
    parser.add_argument("new_dir", help="The directory considered new.")

    args = parser.parse_args()

    if args.old_dir == None or args.new_dir == None:
        logging.critical("Invalid number of parameters, at least two directories are expected.")
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.old_dir):
        logging.critical("old_dir doesn't appear to be a valid directory (%s)." % (args.old_dir))
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.new_dir):
        logging.critical("new_dir doesn't appear to be a valid directory (%s)." % (args.old_dir))
        parser.print_help()
        sys.exit(1)

    if not args.extension in supported_formats:
        logging.critical("Incorrect format parameter provided. Expected: %s" % (supported_formats))
        parser.print_help()
        sys.exit(1)

    if not args.old_dir.endswith("/"):
        args.old_dir += "/"
    if not args.new_dir.endswith("/"):
        args.new_dir += "/"

    tree = finder.Tree(args.old_dir, args.new_dir, filter=args.filter, diff_obj=diff.PDF)
    logging.debug(tree)
    report = reporter.Generator(tree)
    report.generate(args.extension)
