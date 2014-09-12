json-parse-challenge
====================

Coding challenge that takes a file of records, parsing them and outputting as valid json according to a standard.

Details
====================

The input file will contain entries of personal information in multiple formats. These entries must be normalized into a standard JSON format.

Some sample lines might be:

    Lastname, Firstname, (703)-742-0996, Blue, 10013
    Firstname Lastname, Red, 11237, 703 955 0373
    Firstname, Lastname, 10013, 646 111 0101, Green

The order and format of the lines may vary as above, in those 3 specific formats.

Some lines may be invalid, but should not interfere with processing. If a line is invalid, the line number is appeneded to an "errors" key at the end of the json file.

The "entries" list in the json file should be sorted in ascending alphabetical order by (last name, first name).
