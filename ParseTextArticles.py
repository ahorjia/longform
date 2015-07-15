
import os
import re
from re import IGNORECASE
from ProquestArticle import ProquestArticle


DELIMITER = "________________"


def parse_file(file_path):
    labels = all_labels()
    pas = []
    with open(file_path, "r") as my_file:
        lines = my_file.readlines()

        for line_number in range(len(lines)):
            if lines[line_number].startswith(DELIMITER):
                ln, pa = parse_block(lines, line_number + 1, labels)
                line_number += ln
                pas.append(pa)

    return pas


def parse_block(lines, starting_line_number, labels):
    pa = ProquestArticle()
    for line_number in range(starting_line_number, len(lines)):
        if lines[line_number].startswith(DELIMITER):
            return line_number, pa

        for key in pa.__dict__:
            compare_string = (key + ':').lower().replace('_', ' ')
            if lines[line_number].lower().startswith(compare_string):
                pa.__dict__[key] = lines[line_number][len(compare_string) + 1:]

    return len(lines), pa


def parse_file_extract_keys(file_path):
    patt = re.compile('\A[a-z\s]*\:', IGNORECASE)
    labels = set()
    with open(file_path, "r") as my_file:
        data = my_file.readlines()

        data = [patt.findall(line) for line in data if patt.match(line)]

        for item in data:
            labels.update(item)

    return labels


def parse_all_files_extract_keys(dir_path):
    all_labels = set()
    for f in os.listdir(dir_path):
        if f.endswith(".txt"):
            full_file_name = os.path.join(dir_path, f)
            all_labels.update(parse_file_extract_keys(full_file_name))
            # print parse_file_extract_keys(full_file_name)

    return all_labels


def title_categories():
    extracted_categories = ['The Critics:', 'Records:', 'Onstage:', 'Dancing:', 'Destinations:', 'Dance:', 'Notebook:', 'Reunion:', 'Fogbound:', 'Encores:', 'Casual:', 'Revivals:', 'Art:', 'Projections:', 'Homecoming:', 'Headliners Movies:', 'Anniversary:', 'Postscript:', 'The Talk of the Town:', 'Contenders:', 'Portrait:', 'Remix:', 'Fiction:', 'Reflections:', 'TV:', 'Cue:', 'Pop Music:', 'Background Music:', 'Muses:', 'Influences:', 'Troubadours:', 'Books:', 'Profiles:', 'Lessons:', 'Life Lessons:', 'Annals of Broadcasting:']
    # final_label = final_labels()
    # lst2 = [lbl for lbl in extracted_categories if lbl not in final_label]
    print len(extracted_categories)
    return extracted_categories


def all_labels():
    extracted_labels = ['Supplement:', 'Author:', 'Abstract:', 'Links:', 'Full text:', 'Location:', 'Narrow subject:', 'Broad subject:', 'People:', 'Title:', 'Publication title:', 'Volume:', 'Issue:', 'Pages:', 'Publication year:', 'Publication date:', 'Year:', 'Publisher:', 'Place of publication:', 'Country of publication:', 'Publication subject:', 'ISSN:', 'Source type:', 'Language of publication:', 'Document type:', 'Document feature:', 'ProQuest document ID:', 'Document URL:', 'Last Updated:', 'Database:']
    print len(extracted_labels)
    return extracted_labels

if __name__ == '__main__':
    root_dir = "/Users/ali.ghorbani/GoogleDrive/MT/TheNewYorker"
    file_name = "2001.txt"

    full_file_name = os.path.join(root_dir, file_name)
    print parse_file(full_file_name)
    # print parse_file_extract_keys(full_file_name)
    # print [item for item in parse_all_files_extract_keys(root_dir) if len(item) < 20 and not item.isupper()]
    # print title_categories()