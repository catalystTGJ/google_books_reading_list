import gb_read
from io import StringIO

# instantiate both required objects here, so that testing can work with them.
# NOTE: the last 10 lines of the gb_read.py need to be commented out before unit testing.
books = gb_read.Books()
io = gb_read.Io()

def test_ensure_string():
    # This is a support method which aids in the appearance of the output to the screen of either the query results or the reading list.
    # the function will take one parameter and determine if the value is a list, and if so, it will convert to a string,
    # otherwise it will return the same data from the paramenter that was received.

    # here it will simply return the same string that was received.
    assert io.ensure_string("test") == "test"

    # here it will convert the list to a string of comma separated values.
    assert io.ensure_string(["test", "test", "test"]) == "test, test, test"

def test_print_commands(capsys):
    # This is a simple method that combines a string as a passed parameter with the word "Commands" separated with new lines.
    # This is used a few times by the Io class, so we have it to eliminate redundancy.
    message = "A message that will appear above the word commands with a separating new line."
    expected_output = f"{message}\nCommands:\n\n"
    io.print_commands(message)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == expected_output

def test_print_list(capsys):
    # This is a support method that prints out a list of either a query result or reading list with a description line above it.
    # This is a tricky bit to set up for testing due to the new line characters.
    # Note: This method is called on by the "show_list" method.
    message = "A message that will appear above the list with a separating new line."
    dict_list = [{"title":"Dune","publisher":"Penguin","authors":"Frank Herbert"}]
    columns = ["title","publisher","authors"]
    expected_list_output = f'{message}\n\n          TITLE   PUBLISHER   AUTHORS         \n\n1.)       Dune    Penguin     Frank Herbert   \n\n'
    io.print_list(message, dict_list, columns)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == expected_list_output

def test_print_footer_message_wait(monkeypatch):
    # This is a method that prints a footer message that will sometimes exist after a command/event.
    # This method will clear the footer_message variable after it is printed.
    io.footer_message = "Note: A footer message will appear to inform a user, and wait for pressing enter."
    input_enter = StringIO('\n')
    monkeypatch.setattr('sys.stdin', input_enter)
    io.print_footer_message_wait()
    assert io.footer_message == ""

def test_show_list(capsys):
    # This method is used to show either the query result or the reading list
    # When show is set to "Q", and books.query is "", the following is the result.
    io.show = "Q"
    expected_output  = 'There are currently no results for a query.\n\nCommands:\n\n'
    io.show_list(books)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == expected_output

    # When show is set to "Q", and books.query is not "", the following is the result.
    books.query = "a"
    expected_output  = 'No result was returned for the last query of: "a"\n\nCommands:\n\n'
    io.show_list(books)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == expected_output

    #Note: the testing of the print list is already covered above.

    # When show is set to "R", and rl_books is empty, the following is the result.
    io.show = "R"
    expected_output  = 'There are currently no results for the reading list.\n\nCommands:\n\n'
    io.show_list(books)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == expected_output

    #Note: the testing of the print list is already covered above.

def test_input_command(monkeypatch):
    # This method simply sets the io.command value to whatever the user enters.
    input_q = StringIO('q\n')
    monkeypatch.setattr('sys.stdin', input_q)
    io.input_command()
    assert io.command == "q"

    # if the user enters nothing, then command will be nothing as well.
    input_enter = StringIO('\n')
    monkeypatch.setattr('sys.stdin', input_enter)
    io.input_command()
    assert io.command == ""

def test_evaluate_command(monkeypatch):
    # This method will evualate the current input command and make necessary changes to other values,
    # or set a footer_message, or collect input for a query, or some combination of these things.
    # Since this method may perform a query for book data, the books object must be passed in.
    
    # when command is set to something unexpected,
    io.command = "W"
    io.evaluate_command(books)
    assert io.footer_message == "NOTE: Currently, only the characters 'N', 'Q', 'R', 'X', or numeric values are supported for input."

    # when command is set to "q", show will be set to "Q"
    io.command = "q"
    io.evaluate_command(books)
    assert io.show == "Q"

    # when command is set to "r", show will be set to "R"
    io.command = "R"
    io.evaluate_command(books)
    assert io.show == "R"

    # when command is set to "x", show will be set to footer_message will be set
    # a clear screen will also occur.
    io.command = "x"
    io.evaluate_command(books)
    assert io.footer_message == 'Goodbye!\n'

    # when command is "n", an input for a query will occur.
    # if the input is nothing, ql_books will not contain data.
    io.command = "n"
    input_enter = StringIO('\n')
    monkeypatch.setattr('sys.stdin', input_enter)
    io.evaluate_command(books)
    assert len(books.ql_books) == 0

    # if the input is more than nothing, and has a returning result,
    # ql_books will contain data
    input_dune= StringIO('Dune\n')
    monkeypatch.setattr('sys.stdin', input_dune)
    io.evaluate_command(books)
    assert len(books.ql_books) == 5

def test_dict_in_list():
    # This is a support method which aids in the assembly of either a query result, or adding a book to the reading list.
    # This function simply tests for the existence of a dictionary in a list of dictionaries. the function returns a boolean result.
    # Based on the subset of desired columns for this project, Google's data will return what appears to be duplicate items.
    # As well, a user might try to add the same book to their reading list, so this function aids in preventing both of these use cases.
    book_dict = {"title":"Dune","publisher":"Penguin","authors":["Frank Herbert"]}

    # here we set up a positive result, where the above book_dict will be found in the list of dictionaries.
    book_dict_list = [{"title":"Dune","publisher":"Penguin","authors":["Frank Herbert"]}]
    assert books.dict_in_list(book_dict_list, book_dict) == True

    # here we set up a negative result, where the above book_dict will not be found in the list of dictionaries.
    book_dict_list = [{"title":"The Science of Dune","publisher":"BenBella Books, Inc.","authors":["Kevin Grazier"]}]
    assert books.dict_in_list(book_dict_list, book_dict) == False

def test_google_api_query():
    # This is the method that interfaces with Google's Books API, provided a "query", it will return a matching result.
    # The function will return only as many items as desired based on a single integer parameter representing the maximum number of itmes to return.

    #The following will return nothing
    books.google_api_query("", 1)
    assert books.ql_books == []

    # The followiing will return 1 book
    books.google_api_query("Dune", 1)
    assert books.ql_books == [{"title":"Dune","publisher":"Penguin","authors":["Frank Herbert"]}]

    # Note, the data returned for the "authors" is actually a list and not just a string.