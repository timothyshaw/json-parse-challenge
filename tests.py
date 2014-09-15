import random
import unittest

from parser_writer import RecordJsonWriter


class TestRecordJsonWriter(unittest.TestCase):
    def setUp(self):
        self.writer = RecordJsonWriter()
        self.entry_parts = ['Timothy', 'Shaw', '52556', '555 555 5555', 'orange']
        self.format = [
            self.writer.first_name,
            self.writer.last_name,
            self.writer.zipcode,
            self.writer.phone_number,
            self.writer.color
        ]

    def test_get_first_name_last_name(self):
        first_name, last_name = self.writer._get_first_name_last_name(
            self.entry_parts,
            self.format
        )
        self.assertEqual(self.entry_parts[0], first_name)
        self.assertEqual(self.entry_parts[1], last_name)

    def test_entry_parts_match_format(self):
        self.assertTrue(
            self.writer.entry_parts_match_format(self.entry_parts, self.format)
        )

        bad_entry = self.entry_parts
        bad_entry[0], bad_entry[2] = bad_entry[2], bad_entry[0]
        self.assertFalse(
            self.writer.entry_parts_match_format(bad_entry, self.format)
        )

    def test_add_entries_errors(self):
        self.assertEqual(len(self.writer.entries), 0)
        self.assertEqual(len(self.writer.errors), 0)

        entry = ', '.join(self.entry_parts)
        line_number = 0
        self.writer.process_entry(entry, line_number)
        self.assertEqual(len(self.writer.entries), 1)
        self.assertEqual(len(self.writer.errors), 0)

        bad_entry = ', '.join(['52556', 'Shaw', 'Timothy', '111 222 3333333', 'gr33n'])
        line_number = 1
        self.writer.process_entry(bad_entry, line_number)
        self.assertEqual(len(self.writer.entries), 1)
        self.assertEqual(len(self.writer.errors), 1)

if __name__ == '__main__':
    unittest.main()
