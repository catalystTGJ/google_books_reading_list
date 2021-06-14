

- [Installation](#installation)
- [Usage](#usage)
- [Behavior](#behavior)
- [My 50K foot process](#my-50k-foot-process)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Installation

**Requirements:** Uses "requests" library

Requirements.txt is available

Otherwise, pip install requests

## Usage

1. Ensure that an appropriate virtual environment is activated that has "requests" library installed.
2. To launch, simply type python3 gb_read.py within a terminal window, while within the folder than contains the .py file.
3. The letters 'N', 'Q', 'R', & 'X' can be used for "New" query, "Query" results, "Reading" list, and Exit.
4. After a query has been performed the number keys can be used to enter a line number to select a book from the query.

Note: It is required to press the enter key to confirm a choice.

## Behavior

1. The script will perform a query against google's books api, whenever some characters are entered during a query function.
2. It will not perform a query, if no characters are entered.
3. The query results of the query will be filtered for duplicates, based on the uniqueness of the information of the specific columns included.
4. The reading list is also protected from addition of duplicate items.
5. Column widths are dynamically determined based on the data being presented for both query results and the reading list.
6. The current columns included in the query results and reading list are: Title, Publisher, and Authors
7. Authors can be one or more names. When more than one, the names will displayed as a simple comma separated string of text.

## My 50K foot process:

1. Search for some information on how to work with google books api, looking for the simplest approach first.
2. Test a provided sample method to see a result in a web browser.
3. Search for a method that's specific to the language chosen.
4. Set up a virtual environment and install any necessary libraries.
5. Write the bare minimum code for a successful "get" request to retrieve some data.
6. Analyze the structure of the data returned to determine how to access the desired elements.
7. Code enough to test some data output.
8. Refine/expand the code to get closer to the data output desired, and repeat until data output is realized.
9. Refactor the code to modularize into specific classes/functions, being careful to maintain loose coupling.
10. Refactor the code to produce a more scalable arrangement where it is simple and logical to implement.
11. Expand the code to arrange the output to be cleaner and dynamically responsive to the data being presented.
12. Refactor the code for edge cases, such as duplicate entries, out of range selections, and lack of input.
13. Refactor the code for redundant code blocks, such as duplicate data checking
14. Refactor the code to streamline the main loop's flow and the various input/output arrangements.
15. Test the application with many queries, many entries into the reading list, many views of the query results and view results.
16. Refactor the code to DRY code!
17. Test more!







