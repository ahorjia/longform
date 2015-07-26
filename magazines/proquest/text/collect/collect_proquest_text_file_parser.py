from unittest import TestCase
from magazines.constants import *
from magazines.proquest.text.proquest_text_file_parser import ProquestTextFileParser
import pickle

__author__ = 'ali.ghorbani'


class CollectProquestTextFileParser(TestCase):
    def test_parse_folder_all_magazines(self):
        test_folder = "/Users/ali.ghorbani/GoogleDrive/MT/Magazines"
        tfp = ProquestTextFileParser()
        self.assertEqual(tfp.directory_path, None)
        self.assertEqual(tfp.pas, [])
        self.assertEqual(str(tfp), '# of parsed files 0 from directory None')
        pas = tfp.parse_directory(test_folder, True)
        with open(parsed_pas_file_path, 'w') as f:
            pickle.dump(pas, f)

        print "{0} articles extracted".format(len(pas))

    def test_basic_try_parse_result(self):
        with open(parsed_pas_file_path, 'r') as f:
            pas = pickle.load(f)

        print "{0} articles loaded".format(len(pas))
