#!/usr/bin/env python3

import os
import sys

from xml.dom import minidom

# STRINGTABLE MERGER TOOL
# Author: KoffeinFlummi
# --------------------------
# Automatically merges all stringtable entries
# in the given language from the given dir.

def get_modules(projectpath):
  modules = []
  
  for i in os.listdir(projectpath):
    path = os.path.join(projectpath, i)
    if not os.path.isdir(path):
      continue
    if i[0] == ".":
      continue
    modules.append(i)

  return modules

def contains_language(key, language):
  """ Checks wether a given key contains a certain language. """
  for child in key.childNodes:
    try:
      assert(child.tagName == language)
      return True
    except:
      pass

  return False

def get_entry_by_id(keys, keyid):
  for key in keys:
    if key.getAttribute("ID") == keyid:
      return key

  return False

def replace_entries(oldpath, newpath, language):
  oldfile = minidom.parse(oldpath)
  newfile = minidom.parse(newpath)

  oldkeys = oldfile.getElementsByTagName("Key")
  newkeys = newfile.getElementsByTagName("Key")
  """
  for keys in oldkeys + newkeys:
    for child in keys.childNodes:
      if len(child.childNodes) == 0:
        keys.removeChild(child)
  """
  newkeys = list(filter(lambda x: contains_language(x, language), newkeys))

  for newkey in newkeys:
    keyid = newkey.getAttribute("ID")
    oldkey = get_entry_by_id(oldkeys, keyid)

    if not oldkey:
      continue

    newentry = newkey.getElementsByTagName(language)[0].firstChild

    try:
      oldentry = oldkey.getElementsByTagName(language)[0].firstChild
      oldentry.setWholeText(newentry.wholeText)
    except:
      oldentry = oldfile.createElement(language)
      oldentry.appendChild(oldfile.createTextNode(newentry.wholeText))
      oldkey.insertBefore(oldfile.createTextNode("\n      "), oldkey.lastChild)
      oldkey.insertBefore(oldentry, oldkey.lastChild)

  xmlstring = oldfile.toxml()
  if xmlstring[-1] != "\n":
    xmlstring += "\n"

  fhandle = open(oldpath, "w")
  fhandle.write(xmlstring)
  fhandle.close()

  return len(newkeys)

def main(sourcepath, language):
  scriptpath = os.path.realpath(__file__)
  projectpath = os.path.dirname(os.path.dirname(scriptpath))

  modules = get_modules(projectpath)
  modulecounter = 0
  keycounter = 0

  for module in modules:
    oldpath = os.path.join(projectpath, module, "stringtable.xml")
    newpath = os.path.join(sourcepath, module, "stringtable.xml")
    if not os.path.exists(newpath):
      newpath = os.path.join(sourcepath, module.lower(), "stringtable.xml")
    if not os.path.exists(newpath):
      continue

    keycounter += replace_entries(oldpath, newpath, language)
    modulecounter += 1

    print("# Merged %i entry/entries in %s" % (keycounter, module))

  print("")
  print("Merged %i entry/entries in %i modules" % (keycounter, modulecounter))

if __name__ == "__main__":
  try:
    sourcepath = os.path.normpath(os.path.join(os.getcwd(), sys.argv[1]))
    language = sys.argv[2]
  
    assert(os.path.exists(sourcepath))
  except:
    print("ERROR: Missing arguments of invalid path.")
    print("\nUsage:")
    print("[script] [path to new project] [language]")
    sys.exit(1)

  main(sourcepath, language)
