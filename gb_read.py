import os           # used for screen clearing
import requests     # used for http requests to google

class Io:
    def __init__(self):
        # estalbish what will be shown initially, which is nothing.
        self.show = ""
        # establish a command variable.
        self.command = ""
        # establish a footer message.
        self.footer_message = ""

    def show_list(self, books):
        # clear the screen
        # Q is for Query list mode
        if self.show == "Q":
            if len(books.ql_books) == 0:
                if books.query == "":
                    self.print_commands('There are currently no results for a query.\n')
                else:
                    self.print_commands('No result was returned for the last query of: "' + books.query +'"\n')
            else:
                self.print_list('Results for query of: "' + books.query + '"', books.ql_books, books.columns)
                self.print_commands('To add an item from the query results to the reading list, enter the corresponding number, or...\n')

        # R is for Reading list mode
        elif self.show == "R":
            if len(books.rl_books) == 0:
                self.print_commands('There are currently no results for the reading list.\n')
            else:
                self.print_list('Viewing the reading list', books.rl_books, books.columns)
        else:
            # We'll end up at this introduction line, when show is nothing.  
            self.print_commands('Welcome to the books query/reading list app!\n')

    def input_command(self):
        # get input from the user
        self.command = input("Enter 'N' for a new query, 'Q' to view query results, 'R' to view reading list, or 'X' to Exit. ")

    def evaluate_command(self, books):
        # determine if a number value has been entered
        if self.command.isnumeric():
            # if Query list is currently being shown, we can accept a number selection, otherwise we'll reject it.
            if self.show == "Q":
                value = int(self.command)
                if value > 0 and value <=len(books.ql_books):
                    selection = books.ql_books[value-1]
                    if books.dict_in_list(books.rl_books, selection) == True:
                        self.footer_message = "NOTE: The selection is already in the reading list."
                    else:
                        books.rl_books.append(selection)
                        self.footer_message = "SUCCESS: The selection has been added to the reading list."
                else:
                    self.footer_message = "NOTE: The selection is not within the range of the query results."
            else:
                self.footer_message = "NOTE: A selection can only be accepted when viewing the query results."

        # N is for new query
        elif self.command.upper() == "N":
            os.system('clear')
            query = input('\nEnter a new search query: ')
            if query != "":
                books.google_api_query(query, 5)
                self.show = "Q"
            else:
                self.footer_message = "NOTE: Since no characters have been entered, a new query will not occur."

        # Q is for showing query list    
        elif self.command.upper() == "Q":
            self.show = self.command.upper()

        # R is for showing reading list
        elif self.command.upper() == "R":
            self.show = self.command.upper()

        # X is to exit the app
        elif self.command.upper() == "X":
            os.system('clear')
            self.footer_message = 'Goodbye!\n'

        # When any other input comes in
        else:
            self.footer_message = "NOTE: Currently, only the characters 'N', 'Q', 'R', 'X', or numeric values are supported for input."

    def print_footer_message_wait(self):
            if self.footer_message != "":
                print(f'\n{self.footer_message}\n')
                self.footer_message = ""
                input("Press enter to continue.")

    # this is a support function to eliminate redundancy. it simply prints out a string parameter followed by "Commands".
    def print_commands(self, messaging=""):
        print(f'{messaging}\nCommands:\n')

    # this is a support function to eliminate redundancy. it will print whichever data list that is passed to it.
    def print_list(self, description, data_list, columns):
        # determine appropriate column widths
        max_widths = {}
        for index in range(len(data_list)):
            for column in columns:
                if column not in max_widths:
                    max_widths[column] = len(column)
                data_length = len(self.ensure_string(data_list[index][column]))
                if max_widths[column] < data_length:
                    max_widths[column] = data_length
                    
        # build header line            
        header = "          "
        for column in columns:
            header = header + column.upper().ljust(max_widths[column] + 3,' ')

        # output description and header lines
        print(f'{description}\n')
        print(f'{header}\n')

        # build and output data lines
        for index in range(len(data_list)):
            line = f"{index+1}.)"
            line = line.ljust(10,' ')
            for column in columns:
                data = self.ensure_string(data_list[index][column])
                line = line + data.ljust(max_widths[column] + 3,' ')
            print(line)
        
        # output one final line feed
        print()

    # this is a support function to eliminate redundancy. it will ensure that a list or a string is returned as a string.
    def ensure_string(self, data):
        return (", ".join(data) if isinstance(data, list) else data)

class Books:
    def __init__(self, columns=['title','publisher','authors'], ql_books=[], rl_books=[], query = ""):
        # establishes the desired columns in an items list
        self.columns = columns
        # establishes the queried list of books
        self.ql_books = ql_books
        # establishes the reading list of books
        self.rl_books = rl_books
        # establishes an empty string for query
        self.query = query

    def google_api_query(self, query, max=5):
        self.query = query
        self.ql_books = []
        if self.query != "":
            # replace white space with the "+" for proper format
            response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={self.query.replace(" ", "+")}')
            if 'items' in response.json():
                if len(response.json()['items']) > 0:
                    for item in response.json()['items']:
                        # we'll filter out any item that doesn't contain the expected columns of information
                        columns_found = 0
                        for column in self.columns:
                            if column in item['volumeInfo']:
                                columns_found += 1
                        if len(self.columns) == columns_found:
                            book = {}
                            for column in self.columns:
                                book[column] = item['volumeInfo'][column]
                            if self.dict_in_list(self.ql_books, book) == False:
                                self.ql_books.append(book)
                            if len(self.ql_books) == max:
                                break

    # this is a support function to eliminate redundancy. # this function will be used to prevent duplicate insertions.
    def dict_in_list(self, dict_list, dict_to_find):
        for dict_item in dict_list:
            if str(dict_item) == str(dict_to_find):
                return True
        return False

# This is the main loop that will keep the application going.
# Note: During unit testing, it will be necessary to comment out the below lines:

# instantiate both required objects here
# books = Books()
# io = Io()

# # We'll loop until input becomes "X".
# while io.command.upper() != 'X':
#     os.system('clear')
#     io.show_list(books)
#     io.input_command()
#     io.evaluate_command(books)
#     io.print_footer_message_wait()