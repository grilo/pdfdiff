#!/usr/bin/env python

import logging
import os
import re
import subprocess
import hashlib


class Tree:

    def __init__(self, left_dir, right_dir, filter, diff_obj):
        self.left_dir = left_dir
        self.right_dir = right_dir
        self.filter = filter
        self.diff_obj = diff_obj
        self.modified = []
        self.unmodified = []
        self.deleted = []
        self.added = []

        self.compute()

    def _find(self, rootdir):
        files_set = set()
        for (dirpath, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                relative_path = full_path.replace(rootdir, "", 1)
                if full_path.endswith(self.filter):
                    files_set.add(relative_path)
        return files_set

    def _digest(self, filename):
        with open(filename, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def _compare(self, left, right):

        left = set(left)
        right = set(right)

        common = left.intersection(right)
        left = left.difference(right)
        right = right.difference(common)

        return common, left, right

    def compute(self):

        left_pdfs = self._find(self.left_dir)
        right_pdfs = self._find(self.right_dir)

        common, left, right = self._compare(left_pdfs, right_pdfs)

        for f in common:
            old_path = os.path.join(self.left_dir, f)
            new_path = os.path.join(self.right_dir, f)
            if self._digest(old_path) == self._digest(new_path):
                self.unmodified.append(self.diff_obj(f, self.left_dir, self.right_dir))
            else:
                self.modified.append(self.diff_obj(f, self.left_dir, self.right_dir))

        for f in left:
            self.deleted.append(self.diff_obj(f, self.left_dir, self.right_dir))

        for f in right:
            self.added.append(self.diff_obj(f, self.left_dir, self.right_dir))

    def __repr__(self):
        return """
        Unmodified: %s
        Deleted: %s
        Added: %s
        Modified: %s
        """ % (self.unmodified, self.deleted, self.added, self.modified)
