#!/usr/bin/python3
#
# ijournally.py
#
# @author Francis Kessie
#
"""
A command line journalling application.

Store dates (as todays date), keyword to identify notes and notes 
taken. Retrieves the notes using the keywords or retrieve notess by 
searching for words contained within the notess. A log file is generated to 
track functionality. 

for usage: python3 snippets1.py -h

Sample usage:
     create ----------------------------------create a new database
     put Cairns "We did mountain climbing" ---store a txt with keyword Cairns
     get Cairns ------------------------------retrieve text stored under Cairns            
     catalog ---------------------------------search available keywords
     search "the boy--------------------------search text containing "the boy"
"""
import logging
import argparse
import sqlite3 as lite
import sys
import datetime

# Set the log output file, and the log level
# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to sqlite")
connection = lite.connect('ijournally.db')
logging.debug("Database connection established.")

def create():
    """create new data table or overwrite existing table and create new table 
    to a store data.
    """
    try:
       with connection as con:
         curs = con.cursor()
         curs.executescript("""create table snippets(keyword text primary key,                    
                    message text not null default '', date text)""");
    except lite.OperationalError:
         while True:
           message = "This will create new databse and delete existing data [y/n]: "
           inp = input(message)
           if inp.lower() in ['y', 'yes']:
               with connection as con:
                   curs.executescript("""DROP TABLE IF EXISTS snippets;
                     create table snippets(keyword text primary key,                    
                     message text not null default '', date text)""");
                   break  
           else:
               sys.exit() 
    return None

    
def put(name, snippet):
    """Store a snippet with an associated name"""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    date = datetime.date.today().strftime("%A %d. %B %Y")
    with connection as con:
        try:
            command = "insert into snippets values (?,?,?)"
            curs = con.cursor()
            curs.execute(command, (name, snippet, date))
        except lite.IntegrityError:            
            connection.rollback()
            
            command = "update snippets set message=?, date=? where keyword=?"
            curs.execute(command, (snippet,date, name,))
    logging.debug("Snippet stored successfully.")
    return name, snippet, date
    
def get(name):
    """Retrieve the snippet with a given name.
    prints a warning message if keyword not available
    """
    logging.info("retrieving a snippet {!r}".format(name))
    with connection as con:
        curs = con.cursor()
        curs.execute("select message, date from snippets where keyword=?", (name,))
        row = curs.fetchone()
    
    logging.debug("Snippet retrieved successfully.")
    
    # Print warning and exit if no snippet was found with that name.
    if not row:
        print("Keyword: {!r} not available".format(name))
        sys.exit()     
    return row

def catalog():
    """Retrieve all avaliable keywords from snippet table"""
    logging.info("retrieving all snippets") 
    with connection as con: 
        curs = con.cursor()
        command = "select keyword from snippets order by keyword"
        curs.execute(command)
        row = curs.fetchall()    
    return row
 
def search(string):
    """search for a string within the snippet messages and return snippets
    containing the string"""    
    logging.info("retrieving all snippets containing a given substring") 
    with connection as con: 
        curs = con.cursor()
        command = "select keyword, message from snippets where message like "+"'%"+string+"%'"  
        curs.execute(command)
        row = curs.fetchall()    
    return row 

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the create command
    logging.debug("Constructing create subparser")
    create_parser = subparsers.add_parser("create", help="create new or overwrite existing database")
    
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for the catalog function
    logging.debug("Constructing catalog subparser")
    catlog_parser = subparsers.add_parser("catalog", help="Available keywords")
    
    #Subparser for the search function
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve snippet containing a substring")
    search_parser.add_argument("string", help="The substring in the snippet")
        
    arguments = parser.parse_args(sys.argv[1:])
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "create":
       create()
       print("Created new table")
    if command == "put":
        name, snippet, date = put(**arguments)
        print("Stored: {!r} as: {!r} on: {!r}".format(snippet, name, date))
    elif command == "get":
        snippet, date = get(**arguments)        
        print("Retrieved snippet: {!r}".format(snippet))
        print("Date of entry: {!r}".format(date))
    elif command == "catalog":        
        keys = []
        keywordlist = catalog(**arguments)  
        for values in keywordlist:
            keys.append(",".join(values))
        print("Available keywords: {!r}".format(keys)) 
    elif command == "search":
        for name, snippet in search(**arguments):
            print("Keyword:{!r}  Snippet:{!r}".format(name, snippet))

if __name__ == "__main__":
    main()
