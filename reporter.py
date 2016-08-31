#!/usr/bin/env python

import logging
import os


def generate_report(results, output='diff'):

    if not os.path.isdir(output):
        logging.warning("Directory (%s) doesn't exist. Creating..." % (output))
        os.makedirs(output)

    if len(results['unmodified']) == 0:
        print "No unmodified files."
    else:
        print "Unmodified files:"
        for f in results['unmodified']:
            print "\t == %s" % (f)

    if len(results['deleted']) == 0:
        print "No deleted files."
    else:
        print "Deleted files:"
        for f in results['deleted']:
            print "\t -- %s" % (f)

    if len(results['added']) == 0:
        print "No added files."
    else:
        print "Added files:"
        for f in results['added']:
            print "\t ++ %s" % (f)

    if len(results['modified']) == 0:
        print "No modified files."
    else:
        print "Modified files:"
        for f in results['modified']:
            print "\t != %s" % (f)

        for f in results['modified']:
            fullpath = os.path.join(output, f.path + ".png")
            basedir = os.path.dirname(fullpath)
            out = f.diff_image()
            if not os.path.isdir(basedir):
                os.makedirs(basedir)
            if os.path.isfile(fullpath):
                os.unlink(fullpath)
            with open(fullpath, 'wb') as diff_img:
                diff_img.write(out)
