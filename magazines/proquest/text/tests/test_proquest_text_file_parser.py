from unittest import TestCase
from magazines.article import Article
from magazines.proquest.text.proquest_text_file_parser import ProquestTextFileParser

__author__ = 'ali.ghorbani'


class TestProquestTextFileParser(TestCase):
    def test_parse_file(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_file1.txt"
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 1)
        self.assertEqual(pas[0].narrow_subject, 'American cinema, Feature films, Actors, Producers, Film directors, Debuts, Wives, Daughters, Sports, Careers\n')
        self.assertEqual(pas[0].abstract, "Actor, producer, and first-time director Tommy Lee Jones is briefly profiled. His 2005 directorial debut \"The Three Burials of Mequiades Estrada,\" which he also stars in, is discussed along with his wife Dawn's and daughter Victoria's roles in the making of the film. Jones's love for polo and future career plans are also mentioned.\n")
        self.assertEqual(pas[0].author, "Ross, Lillian\n")
        self.assertEqual(pas[0].broad_subject, 'Film-USA, Film-Productions\n')

    def test_parse_block_no_delimiter(self):
        lines = ['blah']
        tfp = ProquestTextFileParser()
        with self.assertRaises(AssertionError):
            tfp.parse_block(lines)

    def test_parse_block_top_delimiter_pass(self):
        lines = ['_______________________________________']
        tfp = ProquestTextFileParser()
        tfp.parse_block(lines)

    def test_parse_block_inside_delimiter_fail(self):
        lines = ['_______________________________________', 'line1', '___________________________', 'line2']
        tfp = ProquestTextFileParser()
        with self.assertRaises(AssertionError):
            tfp.parse_block(lines)

    def test_parse_block_delimit_good_pass(self):
        lines = ['_______________________________________', 'line1', 'line12', 'line2']
        tfp = ProquestTextFileParser()
        tfp.parse_block(lines)

    def test_parse_label_1(self):
        lines = ['Volume: 81', '\x0A']
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "volume")
        self.assertEqual(a, ['81'])

    def test_parse_label_2(self):
        lines = ['Volume: 81', '\x0A', 'Issue: 43', '\x0A', 'Pages: 28-29', '\x0A']
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "volume")
        self.assertEqual(a, ['81'])

    def test_parse_label_3(self):
        lines = ['Publication title: The New Yorker', '\x0A', 'Volume: 81', '\x0A', 'Issue: 43', '\x0A', 'Pages: 28-29',
                 '\x0A']
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "volume")
        self.assertEqual(a, ['81'])

    def test_parse_label_from_file_1(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_label_parser.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "volume")
        self.assertEqual(a, ['81\n'])

    def test_parse_label_from_file_2(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_label_parser.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "Last updated")
        self.assertEqual(a, ['2014-09-26\n'])

    def test_parse_label_from_file_3(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_label_parser.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        a = tfp.parse_label(lines, "Database")
        print a
        self.assertEqual(a, ['International Index to Performing Arts Full Text\n',
                             'some other stuff\n', 'another stuff\n'])

    def test_parse_block_from_file_1(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/test_block_parser.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        a = tfp.parse_block(lines)
        self.assertEqual(a.author, "Ross, Lillian\n")
        self.assertEqual(a.abstract, "Actor, producer, and first-time director Tommy Lee Jones is briefly profiled. His 2005 directorial debut \"The Three Burials of Mequiades Estrada,\" which he also stars in, is discussed along with his wife Dawn's and daughter Victoria's roles in the making of the film. Jones's love for polo and future career plans are also mentioned.\n")
        self.assertEqual(a.narrow_subject, "American cinema, Feature films, Actors, Producers, Film directors, Debuts, Wives, Daughters, Sports, Careers\n")
        self.assertEqual(a.broad_subject, "Film-USA, Film-Productions\n")
        self.assertEqual(a.people, "Jones, Tommy Lee, Jones, Dawn, Jones, Victoria\n")
        self.assertEqual(a.title, "The Talk of the Town: The Pictures: Lunch With Tommy Lee\n")
        self.assertEqual(a.publication_title, "The New Yorker\n")
        self.assertEqual(a.volume, "81\n")
        self.assertEqual(a.issue, "43\n")
        self.assertEqual(a.pages, "28-29\n")
        self.assertEqual(a.database, "International Index to Performing Arts Full Text\n\nsome other stuff\n\nanother stuff\n")
        self.assertEqual(a.full_text, "Tommy Lee Jones, actor, producer, and first-time big-screen director, was having lunch the other day at The Players club, in Gramercy Park. Jones appears in his nhaven and barbered. He chose to sit downstairs, in the Grill Room, near an old pool table and a huge fireplace.\n\nand held it. \"I went to an interview with Charlie Rose,\" he said. \"You go in there, and it's all dark, except for the light directed on the table. It looked very much like an execution chamber.\" He took a sip of the Bloody Mary he had ordered. \"I'm happy to be here,\" he said. \"The main thing is, I feel at home in New York. It's open-minded and openhearted.\"\n\n\"Thank you, sir,\" Jones said, shaking the hand.\n\n\"And you've just--?\" Allinson said.\n\n\"Finished a new film,\" Jones said.\n\nGood idea. Hemingway would have liked it.\n")

    def test_parse_file_content_from_file_1(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/full_file.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file_content(lines)
        self.assertEqual(len(pas), 583)
        a = pas[582]
        self.assertEqual(a.author, "Burros, Marian\r\n")
        self.assertEqual(a.abstract, "A collection of recipes for New Year's Eve reflects the changing tastes of Americans. Such items as Cider Rice Pilaf, Broccoli Puree, and Chocolate-Wrapped Pears are featured.\r\n")
        self.assertEqual(a.subject, "Recipes; Cooking\r\n")
        self.assertEqual(a.title, "New Year, New Fare\r\n")
        self.assertEqual(a.publication_title, "New York Times Magazine\r\n")
        self.assertEqual(a.pages, "49\r\n")
        self.assertEqual(a.number_of_pages, "0\r\n")
        self.assertEqual(a.publication_date, "Dec 21, 1986\r\n")
        self.assertEqual(a.publisher, "New York Times Company\r\n")
        self.assertEqual(a.database, "New York Times\r\n")
        self.assertEqual(a.full_text, "Not available.\r\n")

    def test_parse_file_content_from_file_2(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/full_file.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file_content(lines)
        self.assertEqual(len(pas), 583)
        a = pas[0]
        self.assertEqual(a.author, "Starr, Roger\r\n")
        self.assertEqual(a.abstract, "None available.\r\n")
        self.assertEqual(a.publication_subject, "General Interest Periodicals--United States\r\n")
        self.assertEqual(a.title, "Crime: How it destroys, what can be done\r\n")
        self.assertEqual(a.publication_title, "New York Times Magazine\r\n")
        self.assertEqual(a.document_type, "PERIODICAL\r\n")

    def test_parse_file_content_from_file_rollingstone(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/rollingstone.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file_content(lines)
        self.assertEqual(len(pas), 615)
        a = pas[614]
        self.assertEqual(a.abstract, "None available.\r\n")
        self.assertEqual(a.title, "The 10 Worst Movies of 1994\r\n")
        self.assertEqual(a.publication_title, "Rolling Stone\r\n")
        self.assertEqual(a.publication_subject, "Popular Music, Music, Pop Culture\r\n")

    def test_parse_file_content_from_file_none(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/rollingstone.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file_content(lines)
        self.assertEqual(len(pas), 615)
        a = pas[614]
        self.assertEqual(a.author, None)

    def test_parse_file_content_from_file_none_2(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/rollingstone.txt"
        with open(test_file) as f:
            lines = f.readlines()
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file_content(lines)
        self.assertEqual(len(pas), 615)
        a = pas[614]
        self.assertEqual(a.author, None)
        self.assertEqual(a.broad_subject, None)

    def test_parse_file(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/full_file.txt"
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 583)
        a = pas[582]
        self.assertEqual(a.author, "Burros, Marian\r\n")
        self.assertEqual(a.abstract, "A collection of recipes for New Year's Eve reflects the changing tastes of Americans. Such items as Cider Rice Pilaf, Broccoli Puree, and Chocolate-Wrapped Pears are featured.\r\n")
        self.assertEqual(a.subject, "Recipes; Cooking\r\n")
        self.assertEqual(a.title, "New Year, New Fare\r\n")
        self.assertEqual(a.publication_title, "New York Times Magazine\r\n")
        self.assertEqual(a.pages, "49\r\n")
        self.assertEqual(a.number_of_pages, "0\r\n")
        self.assertEqual(a.publication_date, "Dec 21, 1986\r\n")
        self.assertEqual(a.publisher, "New York Times Company\r\n")
        self.assertEqual(a.database, "New York Times\r\n")
        self.assertEqual(a.full_text, "Not available.\r\n")

    def test_parse_file_2(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/full_file.txt"
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 583)
        a = pas[0]
        self.assertEqual(a.author, "Starr, Roger\r\n")
        self.assertEqual(a.abstract, "None available.\r\n")
        self.assertEqual(a.publication_subject, "General Interest Periodicals--United States\r\n")
        self.assertEqual(a.title, "Crime: How it destroys, what can be done\r\n")
        self.assertEqual(a.publication_title, "New York Times Magazine\r\n")
        self.assertEqual(a.document_type, "PERIODICAL\r\n")

    def test_parse_file_rollingstone(self):
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/rollingstone.txt"
        tfp = ProquestTextFileParser()
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 615)
        a = pas[614]
        self.assertEqual(a.abstract, "None available.\r\n")
        self.assertEqual(a.title, "The 10 Worst Movies of 1994\r\n")
        self.assertEqual(a.publication_title, "Rolling Stone\r\n")
        self.assertEqual(a.publication_subject, "Popular Music, Music, Pop Culture\r\n")

    def test_parse_folder(self):
        test_folder = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder"
        tfp = ProquestTextFileParser()
        self.assertEqual(tfp.directory_path, None)
        self.assertEqual(tfp.pas, [])
        self.assertEqual(str(tfp), '# of parsed files 0 from directory None')
        pas1 = tfp.parse_directory(test_folder)
        self.assertEqual(len(pas1), 1199)
        self.assertEqual(str(tfp), '# of parsed files 1199 from directory /Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder')

    def test_parse_folder_nested(self):
        test_folder = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder2"
        tfp = ProquestTextFileParser()
        self.assertEqual(tfp.directory_path, None)
        self.assertEqual(tfp.pas, [])
        self.assertEqual(str(tfp), '# of parsed files 0 from directory None')
        pas1 = tfp.parse_directory(test_folder)
        self.assertEqual(len(pas1), 2398)
        self.assertEqual(str(tfp), '# of parsed files 2398 from directory /Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder2')

    def test_parse_files_count_pas(self):
        tfp = ProquestTextFileParser()
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder/full_file.txt"
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 583)
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder/rollingstone.txt"
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 615)
        test_file = "/Users/ali.ghorbani/GoogleDrive/MT/Longform/TestFiles/folder/test_file1.txt"
        pas = tfp.parse_file(test_file)
        self.assertEqual(len(pas), 1)
