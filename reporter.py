#!/usr/bin/env python

import logging
import os
import time


class Generator:

    def __init__(self, tree, output_dir='delta'):
        self.tree = tree
        self.output_dir = output_dir

        if not os.path.isdir(self.output_dir):
            logging.warning("Directory (%s) doesn't exist. Creating..." % (self.output_dir))
            os.makedirs(self.output_dir)

    def generate(self, extension='gif'):
        logging.info("Generating report on directory (%s)." % (self.output_dir))
        string = []
        string.append("Report for CMS PDF differences (%s)." % (time.strftime("%c")))

        if len(self.tree.unmodified) == 0:
            string.append("No unmodified files.")
        else:
            string.append("Unmodified files:")
            for f in self.tree.unmodified:
                string.append("\t == %s" % (f))

        if len(self.tree.deleted) == 0:
            string.append("No deleted files.")
        else:
            string.append("Deleted files:")
            for f in self.tree.deleted:
                string.append("\t -- %s" % (f))

        if len(self.tree.added) == 0:
            string.append("No added files.")
        else:
            string.append("Added files:")
            for f in self.tree.added:
                string.append("\t ++ %s" % (f))

        if len(self.tree.modified) == 0:
            string.append("No modified files.")
        else:
            string.append("Modified files:")
            for f in self.tree.modified:
                string.append("\t != %s" % (f))

            for f in self.tree.modified:
                f.write(self.output_dir, extension='gif')
        with open(os.path.join(self.output_dir, "summary.txt"), 'w') as summary:
            summary.write("\n".join(string))
