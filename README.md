# garbage-collection-calendar

 - Basierend auf Daten der Bremer Stadtreinigung 
    - http://213.168.213.236/bremereb/bify/index.jsp

## How to run
 - Prerequisite: Python 3.7 installed
 - run `pip install -r Requirements.txt`
 - run script with `python garbage-calendar-cli.py Testweg 777`
 - if street name contains spaces, use quotes, like: `python garbage-calendar-cli.py "Am Brill" 1`
 - it is also possible to specify the range of years for which the calendar entries should be gathered: 
 `python garbage-calendar-cli.py Testweg 777 -start 2018 -end 2020`
 - The iCal file will be stored in the ics-data/ folder


## About the Project
 - The Code consists of 4 main components:
    - CLI
	- get_html.py: downloads the html file
	- garbageWebsiteParser.oy: parse html
	- iCalExport.py: create ics file
