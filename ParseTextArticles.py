
from ProquestTextFileParser import ProquestTextFileParser
from ArticlesBasicStats import ArticlesBasicStats


if __name__ == '__main__':
    root_dir = "/Users/ali.ghorbani/GoogleDrive/MT/"

    parser = ProquestTextFileParser(root_dir)
    parser.parse_all_files()
    pas = parser.get_parsed_files()
    ab = ArticlesBasicStats(pas)
    ab.basic_report()
    ab.full_text_articles_of_give_size(16)
    pass
