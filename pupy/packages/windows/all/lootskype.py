import os
import fnmatch


def dump():

    appdata = os.path.normpath(os.path.expandvars("%APPDATA%"))
    skype_dir = os.path.join(appdata, os.path.normpath('Skype'))
    files = []
    dbs = []
    for root, dirnames, filenames in os.walk(skype_dir):
        for filename in fnmatch.filter(filenames, 'main.db'):
            files.append(filename)
            dbs.append(os.path.join(root, filename))
    if dbs:
        return dbs
