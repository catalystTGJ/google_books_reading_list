

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

1.) To launch, simply type python3 gb_read.py with a terminal window, while within the folder than contains they .py file.

1.) The letters 'N', 'Q', 'R', & 'X' can be used for "New" query, "Query" results, "Reading" list, and Exit.
2.) After a query has been performed the number keys can be used to enter a line number to select a book from the query.
Note: It is required to press the enter key to confirm a choice.

## Behavior

1.) The script will perform a query against google's books api, whenever some characters are entered during a query function.
2.) It will perform a query if no characters are entered.
3.) The query results of the query will be filtered for duplicates, based on the uniqueness of the information of the specific columns included.
4.) The reading list is also protected from addition of duplicate items.
5.) Column widths are dynamically determined based on the data being presented for both query results and the reading list.

## My 50K foot process:

0.) search for some information on how to work with google books api, looking for the simplest approach first.
1.) test a provided sample method to see a result in a web browser.
2.) search for a method that's specific to the language chosen.
3.) Set up a virtual environment and install any necessary libraries.
4.) write the bare minimum code for a successful "get" request to retrieve some data.
5.) analyze the structure of the data returned to determine how to access the desired elements.
6.) code enough to test some data output.
7.) refine/expand the code to get closer to the data output desired, and repeat until data output is realized.
8.) refactor the code to modularize into specific classes/functions, being careful to maintain loose coupling.
9.) refactor the code to produce a more scalable arrangement where it is simple and logical to implement.
10.) expand the code to arrange the output to be cleaner and dynamically responsive to the data being presented.
11.) refactor the code for edge cases, such as duplicate entries, out of range selections, and lack of input.
12.) refactor the code for redundant code blocks, such as duplicate data checking
13.) refactor the code to streamline the main loop's flow and the various input/output arrangements.
14.) test the application with many queries, many entries into the reading list, many views of the query results and view results.
15.) refactor the code to DRY code!







