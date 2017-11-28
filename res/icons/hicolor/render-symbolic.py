#!/usr/bin/env python3

import os
import shutil
import sys

_resources = {}
_aliases = {}

def addResource(directory, name):
    if directory not in _resources:
        _resources[directory] = []
    _resources[directory].append(name)

def gtkEncodeSymbolicSvg(outdir, path, size):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    cmd = 'gtk-encode-symbolic-svg -o "%s" "%s" %dx%d' % (outdir, path, size, size)
    print(cmd)
    os.system(cmd)

def sort(l):
    l = list(l)
    l.sort()
    return l

# These just need to be aliased properly
try:
    for name in os.listdir('scalable/patterns'):
        _aliases[os.path.join('scalable/actions', name)] = os.path.join('scalable/patterns', name)
except:
    print("Patterns not found.")

# These need to be scaled as symbolic icons into
# 16 and their 2x and 3x counterparts
try:
    for dirname in ('actions',):
        for name in sort(os.listdir(os.path.join('scalable', dirname))):
            for size in (16, 32, 48, 64):
                outdir = '%dx%d/%s' % (size, size, dirname)
                path = os.path.join('scalable', dirname, name)
                gtkEncodeSymbolicSvg(outdir, path, size)
                symbolic_name = name[:-4] + '.symbolic.png'
                addResource(outdir, symbolic_name)
except:
    print("Actions not found.")

# We need larger versions for apps
try:
    for dirname in ('apps',):
        for name in sort(os.listdir(os.path.join('scalable', dirname))):
            for size in (16, 32, 48, 128, 256, 512):
                outdir = '%dx%d/%s' % (size, size, dirname)
                path = os.path.join('scalable', dirname, name)
                gtkEncodeSymbolicSvg(outdir, path, size)
                symbolic_name = name[:-4] + '.symbolic.png'
                addResource(outdir, symbolic_name)
except:
    print("Apps not found.")

# Now generate our updated .gresources.xml
with open("icons.gresource.xml", "w") as stream:
    stream.write('''<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <!-- This file is autogenerated. Do not edit this file. -->
  <gresource prefix="/org/fest-im/fest/icons">
''')
    for dirname, names in _resources.items():
        names.sort()
        for name in names:
            stream.write('    <file>%s/%s</file>\n' % (dirname, name))
    for alias in sort(_aliases.keys()):
        name = _aliases[alias]
        stream.write('    <file alias="%s">%s</file>\n' % (alias, name))
    stream.write('''  </gresource>
</gresources>
''')

