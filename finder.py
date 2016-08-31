#!/usr/bin/env python

import os
import re
import subprocess
import hashlib
import pdf

def compare_sets(left, right):

    left = set(left)
    right = set(right)

    common = left.intersection(right)
    left = left.difference(right)
    right = right.difference(common)

    return common, left, right

def is_pdf(filename):
    with open(filename) as f:
        filetype = subprocess.Popen("/usr/bin/file -b --mime -", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE).communicate(f.read(1024))[0].strip()
        if filetype == "application/pdf; charset=binary": return True
        return False

def find_pdfs(rootdir):
    files_set = set()
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            relative_path = full_path.replace(rootdir, "", 1)
            if is_pdf(full_path):
                files_set.add(relative_path)

    return files_set

def digest(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def compare_pdf_dirs(left_dir, right_dir):
    left_pdfs = find_pdfs(left_dir)
    right_pdfs = find_pdfs(right_dir)

    common, left, right = compare_sets(left_pdfs, right_pdfs)

    modified = []
    unmodified = []
    deleted = []
    added = []

    for f in common:
        old_path = os.path.join(left_dir, f)
        new_path = os.path.join(right_dir, f)
        old = digest(old_path)
        new = digest(new_path)
        if digest(old_path) == digest(new_path):
            unmodified.append(pdf.File(old_path))
        else:
            modified.append(pdf.File(new_path, old_path))

    for f in left:
        deleted.append(pdf.File(os.path.join(left_dir, f)))

    for f in right:
        added.append(pdf.File(os.path.join(right_dir, f)))

    return {
        'unmodified': unmodified,
        'modified': modified,
        'deleted': deleted,
        'added': added,
    }
