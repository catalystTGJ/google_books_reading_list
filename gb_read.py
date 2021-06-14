import os           # used for screen clearing
import requests     # used for http requests to google

class Io(object):
    def input_commands():
        return input("Enter 'N' for a new query, 'Q' to view query results, 'R' to view reading list, or 'X' to Exit. ")

    def input_query():
        os.system('clear')
        return input('Enter a new search query: ')

    def print_commands(messaging=""):
        print(f'{messaging}\nCommands:\n')

    def print_list(description, data_list, columns):
        # determine appropriate column widths
        max_widths = {}
        for index in range(len(data_list)):
            for column in columns:
                data_length = len(Io.ensure_string(data_list[index][column]))
                if column in max_widths:
                    if max_widths[column] < data_length:
                        max_widths[column] = data_length
                else:
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
                data = Io.ensure_string(data_list[index][column])
                line = line + data.ljust(max_widths[column] + 3,' ')
            print(line)
        
        # output one final line feed
        print()

    def ensure_string(data):
        return (", ".join(data) if isinstance(data, list) else data)

class Books(object):
    def query(query, columns, max=5):
        books = []
        if query != "":
            # replace white space with the "+" for proper format
            query = query.replace(" ", "+")
            response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
            if 'items' in response.json():
                if len(response.json()['items']) > 0:
                    for item in response.json()['items']:
                        # we'll filter out any item that doesn't contain the expected columns of information
                        columns_found = 0
                        for column in columns:
                            if column in item['volumeInfo']:
                                columns_found += 1
                        if len(columns) == columns_found:
                            book = {}
                            for column in columns:
                                book[column] = item['volumeInfo'][column]
                            if Books.dict_in_list(books, book) == False:
                                books.append(book)
                            if len(books) == max:
                                break
        return books

    # this function will be used to prevent duplicate insertions
    def dict_in_list(dict_list, dict_to_find):
        for dict_item in dict_list:
            if str(dict_item) == str(dict_to_find):
                return True
        return False


# establishes the desired columns in an items list
columns = ['title','publisher','authors']
# establishes the queried list of books
ql_books = []
# establishes the reading list of books
rl_books = []
# estalbish what to show
show = ""
# establishes an empty query
query = ""


# We'll loop forever, or break on exit
while True:
    # clear the terminal screen on each pass
    os.system('clear')

    # Q is for Query list mode
    if show == "Q":
        if len(ql_books) == 0:
            if query == "":
                Io.print_commands('There are currently no results for a query.\n')
            else:
                Io.print_commands('No result was returned for the last query of: "' + query +'"')
        else:
            Io.print_list('Results for query of: "' + query + '"', ql_books, columns)
            Io.print_commands('To add an item from the query results to the reading list, enter the corresponding number, or')

    # R is for Reading list mode
    elif show == "R":
        if len(rl_books) == 0:
            Io.print_commands('There are currently no results for the reading list.\n')
        else:
            Io.print_list('Viewing the reading list', rl_books, columns)
    else:
        # We'll end up at this introduction line, when show is nothing.  
        Io.print_commands('Welcome to the books query/reading list app!\n')

    # get the user input
    command = Io.input_commands()

    # determine if a number value has been entered
    if command.isnumeric():
        value = int(command)
        if value > 0 and value <=len(ql_books):
            selection = ql_books[value-1]
            if Books.dict_in_list(rl_books, selection) == True:
                input("\nNOTE: The selection is already in the reading list. Press enter to continue.")
            else:
                rl_books.append(selection)
                input("\nSUCCESS: The selection has been added to the reading list. Press enter to continue.")
        else:
            input("\nNOTE: The selection is not within the range of the query results. Press enter to continue.")

    # N is for new query
    elif command.upper() == "N":
        query = Io.input_query()
        if query != "":
            ql_books = Books.query(query, columns, 5)
            show = "Q"
        else:
            input("\nNOTE: Since no characters have been entered, a new query will not occur. Press enter to continue.")

    # Q is for showing query list    
    elif command.upper() == "Q":
        show = command.upper()

    # R is for showing reading list
    elif command.upper() == "R":
        show = command.upper()

    # X is to exit the app
    elif command.upper() == "X":
        os.system('clear')
        print('Goodbye!\n')
        break

    # When any other input comes in
    else:
        input("\nNOTE: Currently, only the characters 'N', 'Q', 'R', 'X', or numeric values are supported for input. Press enter to continue.")




