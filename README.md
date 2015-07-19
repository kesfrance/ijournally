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
  
#####put
   The put option will store notes under keywords. The program will automatically add todays date to the date
   as the date of entry. Entering a new note with a preexisting key will update the note under the key and 
   also record current day of update as date of record.

#####get
   The get option will retrive notes using any of the keyword in the database.

#####search
    The search option can be used to retrieve notes by search for substring of text contained within notes.
    All notes with the substring searched will be retrieved. User can then use the keyword of the required 
    to select note required.
    
#####catalog
