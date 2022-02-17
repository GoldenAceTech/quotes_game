# QUOTE SCRAPING GAME

This is a scrapy project that uses scrapy module.
It scrapes quotes and author informations from quotestoscrape.com and the scrape data are saved in the database using sqlite3. The data are then used to play a game where a quote is generated and a player is allowed three guesses for the correct name of the author.

# PROCESS_SCRAPE_DATA MODULE
Run this module to scrape the quotes and authors informations(name, birthday and place of birth) and save it in an sqlite3 database.
The module will create a database called quotes.db where quotes and author's informations are saved

RUN THE GAME MODULE TO START GAME
Users are allowed to guess 4 time the name of the person who made the quotes.
For each failed guess, user's are given hints the following hints:
- Birthdate and location of author
- The first letter of author first name
- The first letter of author last name
