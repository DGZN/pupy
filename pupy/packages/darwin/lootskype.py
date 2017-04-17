import os
import fnmatch

def dump():
    home = os.path.expanduser("~")
    skype_dir = os.path.join(home, 'Library/Application Support/Skype')
    dbs = []
    for root, dirnames, filenames in os.walk(skype_dir):
        for filename in fnmatch.filter(filenames, 'main.db'):
            dbs.append(os.path.join(root, filename))

    return dbs
