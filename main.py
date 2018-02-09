import os
import sys
import argparse
import sqlite3
db_name = "soylent.db"

parser = argparse.ArgumentParser()
parser.add_argument("install", help="Install a repo. Usage: soylent install username/repo", type=str)
parser.parse_args()

if os.path.exists(db_name) == False:
    if os.access('.', os.W_OK):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE repos (name TEXT PRIMARY KEY, path TEXT NOT NULL, version TEXT NOT NULL)')
        conn.commit()
        conn.close()
    else:
        sys.exit("ERROR: Cannot write to db")

#def install(repo):
    
#def update(update):


#def uninstall(repo):

def parse_arguments():
    try:
        if args.install:
            print(args.install)
            #install(args.install)
    except NameError:
        sys.exit("Could not parse argument") 
parse_arguments()



