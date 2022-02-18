import random
from db_method.db_config import Query_Db

class Quote_Game:
    __rows = list(range(1, 101))
    author: tuple[str] = None
    __correct_guesses = 0

    def __init__(self, db_name: str) -> None:
        """Initialise the game and get the database name to query quotes from

        Args:
            db_name (str): _description_
        """
        self.db_name = db_name

    def db_conn(self) -> Query_Db:
        """Gets a connection to the database

        Returns:
            Query_Db: Returns an instance of Query_DB to manage connections to query the database
        """
        return Query_Db(self.db_name)

    def query_db(self, query:str, param: tuple) -> list[tuple]:
        """Query the database and return the data

        Args:
            query (str): The sqlite query statement
            param (tuple): The sqlite parameter used as argument to query the database

        Returns:
            List[tuple[str]]: The query data
        """
        conn = self.db_conn()
        return conn.query(query, param)

    def get_author(self, name: str) -> str:
        """Query the database to get information of quote's author

        Args:
            name (str): The name of the author to search for
        Returns:
            str: The full name of author
        """
        query = "SELECT * FROM authors WHERE author is (?)"
        author_data = self.query_db(query, (name,))
        Quote_Game.author = author_data[0]
        return author_data[0][0]

    def get_rowid(self) -> int:
        """Generates a random rowid from a list of number to use for quote search

        Returns:
            int: A number used as the rowid 
        """
        rows = Quote_Game.__rows
        if rows:
            row_id = random.choice(rows)
            rows.remove(row_id)
            return row_id

    def get_quote(self) -> str:
        """Query the database to get a quote using rowid number
        Call the get_author() method to get the author information and use it to generate hints

        Returns:
            str: The quote string
        """
        row_id = self.get_rowid()
        if row_id:
            query = "SELECT * FROM quotes WHERE rowid is (?)"
            quote_data = self.query_db(query, (row_id,))
            quote = quote_data[0][0]
            self.get_author(quote_data[0][1])
            return quote
            
    def full_name_set(self) -> set:
        """Generate a set containing the author first and last name

        Returns:
            set: A set containg author's first name and last name
        """
        name_list = Quote_Game.author[0].casefold().replace('.', '').split()
        if len(name_list) > 2:
            return {name_list[0], name_list[-1]}
        return set(name for name in name_list)

    def first_hint(self) -> str:
        """Get a hint with the author birth information
        
        Returns:
            str: A string with the author's birth information
        """
        birthday = Quote_Game.author[1]
        place_of_birth = Quote_Game.author[2]
        return f"The author was born on {birthday} in {place_of_birth}."

    def second_hint(self) -> str:
        """Get a hint with the author first name
        
        Returns:
            str: A string with the first letter of author's first name
        """
        first_letter = Quote_Game.author[0][0]
        return f"The first letter of author's first name is {first_letter}"

    def third_hint(self) -> str:
        """Get a hint with the author last name
        
        Returns:
            str: A string with the first letter of author's last name
        """
        name_split = Quote_Game.author[0].split()
        first_letter = name_split[-1][0]
        return f"The first letter of author's last name is {first_letter}"

    def give_hints(self, user_guess: set, full_name: set) -> None:
        """Returns a hint for every failed guess up to three hints or
        returns a congratulatory message if user is right
        Args:
            user_guess (set): A set containg user guess
            full_name (set): A set contain the author first and last name
        """
        hints = {self.first_hint(), self.second_hint(), self.third_hint()}
        while user_guess != full_name:
            if not hints:
                print("You used up all tries, game over! \n")
                break
            print(f'HINT: {hints.pop()}\n')
            guess = input('Try again: ')
            user_guess = set(guess.replace('.', '').casefold().split())
        else:
            Quote_Game.__correct_guesses += 1
            print('You got it right, good job!\n')

    def __correct(self) -> None:
        """Tells the player the number of correct guesses after game is over
        """
        correct_guesses = Quote_Game.__correct_guesses
        print(f'You had {correct_guesses} correct guesses.\n')
        print('Thank you for playing!\n')

    def restart(self) -> None:
        """Restarts the game if teh user enters yes or 1 else ends the game
        """
        print('Will you like to play again?\n')
        play_again = input('Type yes or 1 to play or press any other key to quit: \n')
        if play_again.casefold() in {'yes', '1'}:
            self.play()
        else:
            self.__correct()

    def play(self) -> None:
        """Starts the quote game
        """
        quote = self.get_quote()
        if quote:
            print('Guess the name of the author of this quote, you have 4 tries...\n')
            full_name = self.full_name_set()
            print(f'The quote is: \n {quote}')
            name = input('Who is the author:  \n')
            guess_set = set(name.replace('.', '').casefold().split())
            self.give_hints(guess_set, full_name)        
            print(f"The author name is {Quote_Game.author[0].title()}")
            self.restart()
        else:
            print('That is all the quotes we got.\n')
            self.__correct()
    
if __name__ == '__main__':
    game = Quote_Game("quotes.db")
    game.play()