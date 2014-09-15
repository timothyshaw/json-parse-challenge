import json
import os
import re


class RecordJsonWriter(object):
    """
    Parses a file containing entries of people and their information.
    Organizes the data according to a standard, then outputs it as valid json.
    Keeps track of invalid lines and outputs that as part of the json.
    """

    first_name = re.compile("^([a-zA-Z \.])+$")
    last_name = re.compile("^([a-zA-Z \.])*$")
    first_and_last = re.compile("^([a-zA-Z \.])+$")
    phone_number = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
    zipcode = re.compile("^[\d]{5,5}$")
    color = re.compile("^[a-zA-Z ]+$")

    accepted_formats = [
        [last_name, first_name, phone_number, color, zipcode],
        [first_and_last, color, zipcode, phone_number],
        [first_name, last_name, zipcode, phone_number, color]
    ]

    input_path = ''
    entries = list()
    errors = list()

    def load_input_file(self, filepath):
        self.input_path = filepath

    def output_json(self):
        with open(self.input_path, 'r') as input_file:
            for line_number, entry in enumerate(input_file):
                self.process_entry(entry, line_number)

        self.write_json_file(self.entries, self.errors)
        self.initialize()

    def process_entry(self, entry, line_number):
        parsed_entry = self.parse_entry(entry)
        if parsed_entry:
            self.entries.append(parsed_entry)
        else:
            self.errors.append(line_number)

    def parse_entry(self, entry):
        entry_parts = entry.split(', ')
        for format in self.accepted_formats:
            if len(entry_parts) == len(format):
                if self.entry_parts_match_format(entry_parts, format):
                    firstname, lastname = self._get_first_name_last_name(entry_parts, format)
                    entry_dict = {
                        'color': self._get_color(entry_parts, format),
                        'firstname': firstname,
                        'lastname': lastname,
                        'phonenumber': self._get_phone_number(entry_parts, format),
                        'zipcode': self._get_zipcode(entry_parts, format)
                    }

                    return entry_dict

        return False

    def _get_first_name_last_name(self, entry_parts, format):
        if len(entry_parts) == 4:
            firstname = entry_parts[
                format.index(self.first_and_last)
            ].split(' ')[0]
            lastname = entry_parts[
                format.index(self.first_and_last)
            ].split(' ')[-1]
        else:
            firstname = entry_parts[format.index(self.first_name)]
            lastname = entry_parts[format.index(self.last_name)]

        return (firstname.rstrip(), lastname.rstrip())

    def _get_phone_number(self, entry_parts, format):
        number = entry_parts[format.index(self.phone_number)]
        number_without_punctuation = filter(lambda x: x.isdigit(), number)
        formatted_number = "%s-%s-%s" % (
            number_without_punctuation[0:3],
            number_without_punctuation[3:6],
            number_without_punctuation[6:10],
        )
        return formatted_number

    def _get_color(self, entry_parts, format):
        return entry_parts[format.index(self.color)].rstrip()

    def _get_zipcode(self, entry_parts, format):
        return entry_parts[format.index(self.zipcode)].rstrip()

    def entry_parts_match_format(self, entry_parts, format):
        for index, part in enumerate(entry_parts):
            if not format[index].match(part):
                return False

        return True

    def write_json_file(self, entries, errors):
        entries_sorted = sorted(
            entries,
            key=lambda entry: (entry['lastname'], entry['firstname'])
        )

        output = {
            "entries": entries_sorted,
            "errors": errors
        }

        with open('output/result.out', 'w') as output_file:
            json.dump(output, output_file, indent=2, sort_keys=True)

    def initialize(self):
        self.input_path = ''
        self.entries = list()
        self.errors = list()
