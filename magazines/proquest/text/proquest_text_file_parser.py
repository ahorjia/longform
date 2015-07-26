
from magazines.article import Article


class ProquestTextFileParser:

    DELIMITER = "________________"

    def __init__(self):
        self.pas = []
        self.directory_path = None
        pass

    def __unicode__(self):
        return u"# of parsed files {0} from directory {1}".format(len(self.pas), self.directory_path)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_parsed_articles(self):
        return self.pas

    def parse_directory(self, directory_path, echo_file_name=False):
        import fnmatch
        import os

        self.pas = []
        self.directory_path = directory_path
        for root, dir_names, file_names in os.walk(directory_path):
            for file_name in fnmatch.filter(file_names, '*.txt'):
                full_file_name = os.path.join(root, file_name)
                if echo_file_name:
                    print full_file_name

                self.pas += self.parse_file(full_file_name)

        return self.pas

    def parse_file(self, file_path):
        with open(file_path, "r") as my_file:
            lines = my_file.readlines()
            pas = self.parse_file_content(lines)

        return pas

    def parse_file_content(self, lines):
        pas = []
        for line_number in range(len(lines)):
            if lines[line_number].startswith(ProquestTextFileParser.DELIMITER):
                block_lines = [lines[line_number]]
                for secondary_line_number in range(line_number + 1, len(lines)):
                    if not lines[secondary_line_number].startswith(ProquestTextFileParser.DELIMITER):
                        block_lines.append(lines[secondary_line_number])
                    else:
                        pas.append(self.parse_block(block_lines))
                        break

                line_number += secondary_line_number

        # ProquestTextFileParser.cleanup_full_text(pas)
        return pas

    def parse_block(self, lines):
        if not lines[0].startswith(ProquestTextFileParser.DELIMITER):
            raise AssertionError()

        for line_index in range(1, len(lines)):
            if lines[line_index].startswith(ProquestTextFileParser.DELIMITER):
                raise AssertionError()

        pa = Article()
        for key in pa.__dict__:
            label_data = self.parse_label(lines[1:], key)
            pa.__dict__[key] = None if label_data == [] else '\n'.join(label_data)

        pa.raw_text = lines[1:]
        return pa

    def parse_label(self, lines, key):
        compare_string = (key + ':').lower().replace('_', ' ')
        return_lines = []
        for line_index in range(len(lines)):
            if lines[line_index].startswith(ProquestTextFileParser.DELIMITER):
                raise AssertionError()

        for line_index in range(len(lines)):
            if lines[line_index].lower().startswith(compare_string):
                return_lines.append(lines[line_index][len(compare_string) + 1:])
                for line_index_2 in range(line_index + 1, len(lines)):
                    if lines[line_index_2] in ['\n', '\r', '\r\n']:
                        return return_lines
                    else:
                        return_lines.append(lines[line_index_2])

                return return_lines

        return return_lines

    @staticmethod
    def title_categories():
        extracted_categories = ['The Critics:', 'Records:', 'Onstage:', 'Dancing:', 'Destinations:', 'Dance:', 'Notebook:', 'Reunion:', 'Fogbound:', 'Encores:', 'Casual:', 'Revivals:', 'Art:', 'Projections:', 'Homecoming:', 'Headliners Movies:', 'Anniversary:', 'Postscript:', 'The Talk of the Town:', 'Contenders:', 'Portrait:', 'Remix:', 'Fiction:', 'Reflections:', 'TV:', 'Cue:', 'Pop Music:', 'Background Music:', 'Muses:', 'Influences:', 'Troubadours:', 'Books:', 'Profiles:', 'Lessons:', 'Life Lessons:', 'Annals of Broadcasting:']
        return extracted_categories

    @staticmethod
    def all_labels():
        extracted_labels = ['Supplement:', 'Author:', 'Abstract:', 'Links:', 'Full text:', 'Location:', 'Narrow subject:', 'Broad subject:', 'People:', 'Title:', 'Publication title:', 'Volume:', 'Issue:', 'Pages:', 'Publication year:', 'Publication date:', 'Year:', 'Publisher:', 'Place of publication:', 'Country of publication:', 'Publication subject:', 'ISSN:', 'Source type:', 'Language of publication:', 'Document type:', 'Document feature:', 'ProQuest document ID:', 'Document URL:', 'Last Updated:', 'Database:']
        return extracted_labels
