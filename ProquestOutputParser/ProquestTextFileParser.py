
from ProquestArticle import ProquestArticle


class ProquestTextFileParser:

    DELIMITER = "________________"

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.pas = []
        pass

    def __unicode__(self):
        return u"# of parsed files {0}".format(len(self.pas))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_parsed_files(self):
        return self.pas

    def parse_all_files(self):
        import fnmatch
        import os

        self.pas = []
        for root, dir_names, file_names in os.walk(self.root_dir):
            for file_name in fnmatch.filter(file_names, '*.txt'):
                full_file_name = os.path.join(root, file_name)
                self.pas += self.parse_file(full_file_name)

    def parse_file(self, file_path):
        with open(file_path, "r") as my_file:
            lines = my_file.readlines()
            pas = self.parse_file_content(lines)

        return pas

    def parse_file_content(self, lines):
        pas = []
        for line_number in range(len(lines)):
            if lines[line_number].startswith(ProquestTextFileParser.DELIMITER):
                ln, pa = self.parse_block(lines, line_number + 1)
                pa.raw_text = lines[line_number:line_number + ln]
                line_number += ln
                pas.append(pa)

        ProquestTextFileParser.cleanup_full_text(pas)
        return pas[:-1]

    def parse_block(self, lines, starting_line_number):
        pa = ProquestArticle()
        for line_number in range(starting_line_number, len(lines)):
            if lines[line_number].startswith(ProquestTextFileParser.DELIMITER):
                return line_number, pa

            for key in pa.__dict__:
                compare_string = (key + ':').lower().replace('_', ' ')
                if lines[line_number].lower().startswith(compare_string):
                    line_number = self.parse_label(pa, lines, line_number, key, compare_string)

        return len(lines), pa

    def parse_label(self, pa, lines, starting_line_number, key, compare_string):
        data_lines = [lines[starting_line_number][len(compare_string) + 1:]]
        for line_number in range(starting_line_number + 1, len(lines)):
            if lines[line_number].startswith(ProquestTextFileParser.DELIMITER):
                pa.__dict__[key] = data_lines
                return line_number

            for key1 in pa.__dict__:
                compare_string1 = (key1 + ':').lower().replace('_', ' ')
                if lines[line_number].lower().startswith(compare_string1):
                    pa.__dict__[key] = data_lines
                    return line_number

            data_lines.append(lines[line_number])

        pa.__dict__[key] = data_lines
        return line_number

    @staticmethod
    def cleanup_full_text(pas):
        # for pa in pas:
        #     if pa.full_text is None or pa.full_text == "" or pa.full_text.startswith("Not available."):
        #         pa.full_text = None

        return pas

    # def parse_file_extract_keys(self, file_path):
    #     patt = re.compile('\A[a-z\s]*\:', IGNORECASE)
    #     labels = set()
    #     with open(file_path, "r") as my_file:
    #         data = my_file.readlines()
    #
    #         data = [patt.findall(line) for line in data if patt.match(line)]
    #
    #         for item in data:
    #             labels.update(item)
    #
    #     return labels

    # def parse_all_files_extract_keys(self, dir_path):
    #     all_labels_set = set()
    #     for f in os.listdir(dir_path):
    #         if f.endswith(".txt"):
    #             full_file_name = os.path.join(dir_path, f)
    #             all_labels_set.update(parse_file_extract_keys(full_file_name))
    #
    #     return all_labels_set

    @staticmethod
    def title_categories():
        extracted_categories = ['The Critics:', 'Records:', 'Onstage:', 'Dancing:', 'Destinations:', 'Dance:', 'Notebook:', 'Reunion:', 'Fogbound:', 'Encores:', 'Casual:', 'Revivals:', 'Art:', 'Projections:', 'Homecoming:', 'Headliners Movies:', 'Anniversary:', 'Postscript:', 'The Talk of the Town:', 'Contenders:', 'Portrait:', 'Remix:', 'Fiction:', 'Reflections:', 'TV:', 'Cue:', 'Pop Music:', 'Background Music:', 'Muses:', 'Influences:', 'Troubadours:', 'Books:', 'Profiles:', 'Lessons:', 'Life Lessons:', 'Annals of Broadcasting:']
        return extracted_categories

    @staticmethod
    def all_labels():
        extracted_labels = ['Supplement:', 'Author:', 'Abstract:', 'Links:', 'Full text:', 'Location:', 'Narrow subject:', 'Broad subject:', 'People:', 'Title:', 'Publication title:', 'Volume:', 'Issue:', 'Pages:', 'Publication year:', 'Publication date:', 'Year:', 'Publisher:', 'Place of publication:', 'Country of publication:', 'Publication subject:', 'ISSN:', 'Source type:', 'Language of publication:', 'Document type:', 'Document feature:', 'ProQuest document ID:', 'Document URL:', 'Last Updated:', 'Database:']
        return extracted_labels
