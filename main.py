#!/usr/bin/python3
import os
import subprocess
import sys
import argparse
import sqlite3
db_name = os.path.dirname(os.path.realpath(__file__)) + "/soylent.db"
if os.path.exists(db_name) == False:
    if os.access(os.path.dirname(os.path.realpath(__file__)), os.W_OK):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE repos (name TEXT PRIMARY KEY, path TEXT NOT NULL)')
        conn.commit()
        conn.close()
    else:
        sys.exit("ERROR: Cannot write to db")
def install(repo):
    command = "git clone https://github.com/" + repo
    if os.access(os.getcwd(), os.W_OK):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        repo_real = repo.split("/")
        path = os.getcwd() + "/" + repo_real[1]
        try: 
            c.execute("INSERT INTO repos (name, path) VALUES ('{name}', '{path}')".format(name=repo, path=path))  
            conn.commit()
            conn.close()
            os.system(command)
        except sqlite3.IntegrityError:
             sys.exit("Repo already installed")
    else:
        sys.exit("Error: Cannot write into directory")
def uninstall(repo):
    if os.access(os.getcwd(), os.W_OK):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT path FROM repos WHERE name = '{name}'".format(name=repo))
        repo_path = c.fetchone()
        command = "rm -R -f " + repo_path[0]
        try:
            c.execute("DELETE FROM repos WHERE name = '{name}'".format(name=repo))
            conn.commit()
            conn.close()
            os.system(command)
            sys.exit("Repo uninstalled successfully")
        except sqlite3.IntegrityError:
            sys.exit("Error while deleting repo from database")
    sys.exit("Error: Cannot write into directory")
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", help="Install a repo. Usage: soylent --install username/repo", type=str)
    parser.add_argument("--uninstall", help="Delete a repo. Usage soylent --uninstall username/repo", type=str)
    args = parser.parse_args()
    
    if args.install: 
        install(args.install)
    elif args.uninstall:
        uninstall(args.uninstall)

parse_arguments()



