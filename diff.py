#!/usr/bin/env python

import logging
import shlex
import os
import subprocess

import tempfile


class File(object):

    def __init__(self, path, left, right):
        self.path = path
        self.left = left
        self.right = right
        self.left_path = os.path.join(self.left, self.path)
        self.right_path = os.path.join(self.right, self.path)

    def _run_cmd(self, cmd):
        logging.debug("Running: %s" % (cmd))
        stdout, stderr = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return stdout, stderr

    def __repr__(self):
        return self.path


class PDF(File):

    def __init__(self, path, left, right):
        super(PDF, self).__init__(path, left, right)

    def _get_image_size(self, path=None):
        if not path: path = self.left_path
        command = "identify %s" % (path)
        return self._run_cmd(command)[0].split()[2]

    def to_image(self, path=None, size=None):
        if not path: path = self.left_path
        command = "convert -transparent-color white %s -append" % (path)
        if size:
            logging.warning("Resizing (%s) to %s" % (path, size))
            command += " -resize %s -gravity north -extent %s" % (size, size)
        command += " -"
        return self._run_cmd(command)[0]

    def to_gif(self):
        command = "convert -transparent-color white -depth 24 -quality 100 -delay 200 -loop 0 '%s' '%s' gif:-" % (self.left_path, self.right_path)
        return self._run_cmd(command)[0]

    def to_pdf(self):
        command = "compare '%s' '%s' -" % (self.left_path, self.right_path)
        logging.warning("Comparing (%s) and (%s)." % (self.left_path, self.right_path))
        stdout, stderr = self._run_cmd(command)
        return stdout

    def to_png(self):
        original = tempfile.NamedTemporaryFile(delete=False)
        original.write(self.to_image(self.left_path))
        original.close()

        size = self.get_image_size(original.name)

        modified = tempfile.NamedTemporaryFile(delete=False)
        modified.write(self.to_image(self.right_path, size))
        modified.close()

        #command = "compare -compose Src -quality 100 -transparent-color white '%s' '%s' png24:-" % (original.name, modified.name)
        command = "convert '%s' '%s' -colorspace Gray -compose difference -composite png24:-" % (original.name, modified.name)

        logging.warning("Comparing (%s) and (%s)." % (self.left_path, self.right_path))
        stdout, stderr = self.__run_cmd(command)

        os.unlink(original.name)
        os.unlink(modified.name)

        return stdout

    def write(self, filename, extension='pdf'):
        if os.path.isdir(filename):
            filename = os.path.join(filename, self.path + "." + extension)
        basedir = os.path.dirname(filename)
        if not os.path.isdir(basedir):
            os.makedirs(basedir)

        out = None
        if extension == 'gif':
            out = self.to_gif()
        elif extension == 'png':
            out = self.to_png()
        elif extension == 'pdf':
            with open(self.left_path, 'r') as f:
                out = f.read()

        with open(filename, 'wb') as f:
            logging.debug("Writing file to: %s" % (filename))
            f.write(out)

    def __repr__(self):
        return self.path
