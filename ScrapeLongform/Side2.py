# Phase 2 Data Cleanup
import simplejson as json
from Side1 import LongformArticle
from datetime import datetime
import pickle


long_form_output = "Side1Result.json"
with open(long_form_output, "r") as dataFile:
    data = dataFile.read()

print("Total Row Count", len(data))

json_data = json.loads(data)


def clean_and_combine_string_array(array_entry):
    return_value = ' '.join(array_entry)
    return_value = ' '.join(return_value.split())
    return return_value


def clean_string_array(array_entry):
    return_value = [item for item in array_entry if ' '.join(item.split()) != '' and item.strip() != ',' and item.strip() != '-']
    return return_value


def try_parsing_date(text):
    for fmt in ('%b %Y', '%b %Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


def parse_date(raw_date):
    if raw_date is None:
        return None
    return_value = try_parsing_date(raw_date.strip())
    # return_value = raw_date
    return return_value


def process_article(raw_article):
    return_value = LongformArticle(
        title=clean_and_combine_string_array(raw_article["title"]),
        url_address=raw_article["url_address"],
        summary=clean_and_combine_string_array(raw_article["summary"]),
        writers=clean_string_array(raw_article["writers"]),
        publication_link=raw_article["publication_link"],
        publication=raw_article["publication"],
        publication_date=parse_date(raw_article["publication_date"]),
        reading_time=raw_article["reading_time"],
        post_permlink=raw_article["post_permlink"],
        labels=clean_string_array(raw_article["labels"]))

    return return_value

articles = [process_article(json_entry) for json_entry in json_data]

print(len(json_data))
print(len(articles))


with open("Side2Result.pkl", "wb") as pickledData:
    pickle.dump(articles, pickledData)

print("Completed Side 2!")