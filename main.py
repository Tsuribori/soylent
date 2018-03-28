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
        c.execute('CREATE TABLE repos (name TEXT PRIMARY KEY, path TEXT NOT NULL, frozen INTEGER NOT NULL)')
        conn.commit()
        conn.close()
    else:
        sys.exit("ERROR: Cannot write to db")
def install(repo):
    command = "git clone https://github.com/" + repo
    if os.access(os.getcwd(), os.W_OK):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            repo_real = repo.split("/")
            path = os.getcwd() + "/" + repo_real[1]
        except IndexError:
            sys.exit("Repo name must be in format username/repo")
        try: 
            os.system(command) 
            if os.path.isdir(path):
                c.execute("INSERT INTO repos (name, path, frozen) VALUES ('{name}', '{path}', 0)".format(name=repo, path=path))  
                conn.commit()
                conn.close()
                sys.exit("Repo installed succesfully.")
            else:
                sys.exit("\nCould not install repo")
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
        try:
            command = "rm -R -f " + repo_path[0]
        except TypeError:
            sys.exit("Repo not installed")
        try:
            c.execute("DELETE FROM repos WHERE name = '{name}'".format(name=repo))
            conn.commit()
            conn.close()
            os.system(command)
            sys.exit("Repo uninstalled successfully")
        except sqlite3.IntegrityError:
            sys.exit("Error while deleting repo from database")
    
    else:
        sys.exit("Error: Cannot write into directory where " + repo + " resides.")

def update():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT path, name FROM repos WHERE frozen = 0")
    paths = c.fetchall()
    for i in paths:
        if os.access(os.getcwd(), os.W_OK):
            print("\n" + "Updating " + i[1])
            os.chdir(i[0])
            os.system("git pull origin master")
        else:
            print("Error: No write access for " + i[1])
    conn.close()

def freeze(repo):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT path, frozen FROM repos WHERE name = '{name}'".format(name=repo))
    path = c.fetchall()
    try:
        if path[0][0] and path[0][1] == 0:
            if c.execute("UPDATE repos SET frozen = 1 WHERE name = '{name}'".format(name=repo)):
                conn.commit()
                conn.close()
                print(repo + " frozen.")
        else:
            sys.exit("Repo already frozen.")
    except TypeError and IndexError:
        sys.exit("Repo not installed.")
 
def unfreeze(repo):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT path, frozen FROM repos WHERE name = '{name}'".format(name=repo))
    path = c.fetchall()
    try:
        if path[0][0] and path[0][1] == 1:
            if c.execute("UPDATE repos SET frozen = 0 WHERE name = '{name}'".format(name=repo)):
                conn.commit()
                conn.close()
                print(repo + " unfrozen.")
        else:
            sys.exit("Repo already unfrozen.")
    except TypeError and IndexError:
        sys.exit("Repo not installed.")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", help="Install a repo. Usage: soylent --install username/repo", type=str)
    parser.add_argument("--uninstall", help="Delete a repo. Usage soylent --uninstall username/repo", type=str)
    parser.add_argument("--update", help="Update all repos", action="store_true")
    parser.add_argument("--freeze", help="Freeze a repo", type=str)
    parser.add_argument("--unfreeze", help="Unfreeze a repo", type=str)
    args = parser.parse_args()
    
    if args.install: 
        install(args.install)
    elif args.uninstall:
        uninstall(args.uninstall)
    elif args.update:
        update()
    elif args.freeze:
        freeze(args.freeze)
    elif args.unfreeze:
        unfreeze(args.unfreeze)
    elif len(sys.argv) == 1:
        parser.print_help()
parse_arguments()



