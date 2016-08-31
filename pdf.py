#!/usr/bin/env python

import logging
import shlex
import os
import subprocess
import tempfile


class File:

    def __init__(self, path, alt_path=None):
        self.path = path
        self.alt_path = alt_path

    def __run_cmd(self, cmd):
        logging.debug("Running: %s" % (cmd))
        stdout, stderr = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return stdout, stderr

    def to_image(self, path=None, size=None):
        if not path: path = self.path
        command = "convert -transparent-color white %s -append" % (path)
        if size:
            logging.warning("Resizing (%s) to %s" % (path, size))
            command += " -resize %s -gravity north -extent %s" % (size, size)
        command += " -"
        return self.__run_cmd(command)[0]

    def get_image_size(self, path=None):
        if not path: path = self.path
        command = "identify %s" % (path)
        return self.__run_cmd(command)[0].split()[2]

    def diff_gif(self):
        command = "convert -transparent-color white -depth 24 -quality 100 -delay 200 -loop 0 '%s' '%s' gif:-" % (self.path, self.alt_path)
        return self.__run_cmd(command)[0]

    def diff_pdf(self):
        if not self.alt_path:
            raise Exception("Unable to perform comparison since I don't have an alt_path to look for.")
        command = "compare '%s' '%s' -" % (self.path, self.alt_path)
        logging.warning("Comparing (%s) and (%s)." % (self.path, self.alt_path))
        stdout, stderr = self.__run_cmd(command)
        return stdout

    def diff_image(self):
        if not self.alt_path:
            raise Exception("Unable to perform comparison since I don't have an alt_path to look for.")

        original = tempfile.NamedTemporaryFile(delete=False)
        original.write(self.to_image(self.path))
        original.close()

        size = self.get_image_size(original.name)

        modified = tempfile.NamedTemporaryFile(delete=False)
        modified.write(self.to_image(self.alt_path, size))
        modified.close()

        #command = "compare -compose Src -quality 100 -transparent-color white '%s' '%s' png24:-" % (original.name, modified.name)
        command = "convert '%s' '%s' -colorspace Gray -compose difference -composite png24:-" % (original.name, modified.name)

        logging.warning("Comparing (%s) and (%s)." % (self.path, self.alt_path))
        stdout, stderr = self.__run_cmd(command)

        os.unlink(original.name)
        os.unlink(modified.name)

        return stdout

    def __repr__(self):
        return self.path
