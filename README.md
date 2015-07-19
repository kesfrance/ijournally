# A command line journalling application. 
This is the portable version of the snippet app, built with Python, SQL and SQlite.

####Functionalities

1. Store dates, keyword identifiers/Title, snippets of notes via the command line 

2. Retrieve notes using keywords

3. Retrieve notes by searching substrings of text within notes

####Options

#####Create
  The create option will create a new database, but also overwrites any existing database. User is prompted with 
  a warning message before overwritting existing databse. 
     
     python3 ijournally.py create
     
#####put
   The put option will store notes under keywords. The program will automatically add todays date
   as the date of entry. Entering a new note with a pre-existing key will update the note under the key and 
   also record current day of update as date of record.
   
     python3 ijournally.py put Simon "We had a great time last night. Simon Jones came to over for a movie night"

#####get
   The get option will retrieve notes using any of the keyword in the database.
   
     python3 ijournally.py get Simon

#####search
   The search option can be used to retrieve notes by searching for substring of text contained within notes.
   All notes with the substring searched will be retrieved. User can then use the keyword the required note
   to select note required.
     
      python3 ijournally.py search "movie night"
    
#####catalog
   The catalog option will display a list of all available keywords in the journal.
   
     python3 ijournally.py catalog
