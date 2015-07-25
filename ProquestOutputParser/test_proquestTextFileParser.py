from unittest import TestCase
from ProquestTextFileParser import ProquestTextFileParser

__author__ = 'ali.ghorbani'


class TestProquestTextFileParser(TestCase):
    def test_parse_file(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_file1.txt"
        tfp = ProquestTextFileParser("some path")
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 1)
        self.assertEqual(pas[0].narrow_subject, 'American cinema, Feature films, Actors, Producers, Film directors, Debuts, Wives, Daughters, Sports, Careers')
        self.assertEqual(pas[0].abstract, "ctor, producer, and first-time director Tommy Lee Jones is briefly profiled. His 2005 directorial debut \"The Three Burials of Mequiades Estrada,\" which he also stars in, is discussed along with his wife Dawn's and daughter Victoria's roles in the making of the film. Jones's love for polo and future career plans are also mentioned.")
        self.assertEqual(pas[0].author, "Ross, Lillian")
