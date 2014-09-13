import json
import os
import re


class RecordJsonWriter(object):
    "Takes an input file, parses it according to a standard, and outputs as valid JSON"
    def __init__(self):
        self.input_path = ''
        self.entries = list()
        self.errors = list()
        self.phone_number_digit_requirement = 10

    def load_input_file(self, filepath):
        self.input_path = filepath

    def output_json(self):
        with open(self.input_path, 'r') as input_file:
            for line_number, entry in enumerate(input_file):
                parsed_entry = self.parse_entry(entry)
                if parsed_entry:
                    self.entries.append(parsed_entry)
                else:
                    self.errors.append(line_number)

        self.write_json_file(self.entries, self.errors)
        self.initialize()

    def parse_entry(self, entry):
        if not self._entry_format_valid(entry):
            return False
        if not self._phone_number_digit_requirement_met(entry):
            return False

        entry_dict = {
            'color': self._get_color(entry),
            'firstname': self._get_first_name(entry),
            'lastname': self._get_last_name(entry),
            'phonenumber': self._get_phone_number(entry),
            'zipcode': self._get_zip_code(entry)
        }

        return entry_dict

    def _entry_format_valid(self, entry):
        entry_split = entry.split(', ')
        if len(entry_split) < 4:
            return False
        if len(entry_split) == 4:
            namesplit = entry_split[0].split(' ')
            if len(namesplit) == 2 or len(namesplit) == 3:
                return True
            else:
                return False
        if len(entry_split) == 5:
            return True
        else:
            return False

    def _phone_number_digit_requirement_met(self, entry):
        phone_number = self._get_phone_number(entry)
        number_without_punctuation = filter(lambda x: x.isdigit(), phone_number)
        if len(number_without_punctuation) == self.phone_number_digit_requirement:
            return True
        else:
            return False

    def _get_phone_number(self, entry):
        if not self._entry_format_valid(entry):
            return False
        else:
            entry_split = entry.split(', ')

            position_2 = entry_split[2]
            position_2 = filter(lambda x: x.isdigit(), position_2)

            position_3 = entry_split[3]
            position_3 = filter(lambda x: x.isdigit(), position_3)

            if self._contains_digits(position_2) and len(position_2) > 5:
                number = position_2
            elif self._contains_digits(position_3) and len(position_3) > 5:
                number = position_3

            number_without_punctuation = filter(lambda x: x.isdigit(), number)
            formatted_number = "%s-%s-%s" % (
                number_without_punctuation[0:3],
                number_without_punctuation[3:6],
                number_without_punctuation[6:10],
            )

            return formatted_number.rstrip()

    def _get_color(self, entry):
        if not self._entry_format_valid(entry):
            return False
        else:
            entry_split = entry.split(', ')

            if len(entry_split) == 4:
                color = entry_split[1]
            else:
                if not self._contains_digits(entry_split[-1]):
                    color = entry_split[-1]
                else:
                    color = entry_split[3]

            return color.rstrip()

    def _get_first_name(self, entry):
        if not self._entry_format_valid(entry):
            return False
        else:
            entry_split = entry.split(', ')
            if len(entry_split) == 4:
                first_name = entry_split[0].split(' ')[0]
            else:
                if self._contains_digits(entry_split[-1]):
                    first_name = entry_split[1]
                else:
                    first_name = entry_split[0]

            return first_name.rstrip()

    def _get_last_name(self, entry):
        if not self._entry_format_valid(entry):
            return False
        else:
            entry_split = entry.split(', ')
            if len(entry_split) == 4:
                last_name = entry_split[0].split(' ')[1]
            else:
                if self._contains_digits(entry_split[-1]):
                    last_name = entry_split[0]
                else:
                    last_name = entry_split[1]

            return last_name.rstrip()

    def _get_zip_code(self, entry):
        if not self._entry_format_valid(entry):
            return False
        else:
            entry_split = entry.split(', ')

            if len(entry_split) == 4:
                zip_code = entry_split[2]
            else:
                if self._contains_digits(entry_split[-1]):
                    zip_code = entry_split[-1]
                else:
                    zip_code = entry_split[2]

            return zip_code.rstrip()

    def _contains_digits(self, string):
        _digits = re.compile('\d')
        return bool(_digits.search(string))

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
