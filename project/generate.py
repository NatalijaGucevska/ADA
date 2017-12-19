import pickle
import pandas as pd
import numpy as np
import os
import os.path
from urllib import parse


def generate_book_to_url_mapping(url_file_path):
    """
    given a path to a list of downloadable URLs, it generates
    the link between the URLs and a relative filesystem path
    pointing to the resized file on the server's filesystem
    """

    book_url_to_path = dict()
    slices = ["slice5", "", "slice1", "slice2", "slice3", "slice4"]
    directories =  [os.path.join("../filtered_cover/", folder) for folder in slices]

    with open(url_file_path, "r") as f:
        for l in f:
            l_raw = l.strip()
            l = parse.unquote(l_raw)
            basename = os.path.basename(l)

            # we try on each directory to find the file
            for directory in directories:
                path = os.path.join(directory, "resized", basename)
                if os.path.isfile(path):
                    book_url_to_path[l_raw] = path
                    break

    return book_url_to_path

def read_image_features(path):
    """
    given the path to a binary file which contains
    10 bytes ASIN then 4096 * 4 bytes float

    parse them as a python generator
    """
    step = 0
    i = 0
    step_size = 100000

    with open(path, 'rb') as f:
        while True:
            if i > step * step_size:
                print(step * step_size)
                step += 1
            i += 1
            asin = f.read(10)
            if asin == '':
                break
            floats = f.read(4 * 4096)
            try:
                np_array = np.fromstring(floats, dtype=np.float32, count=4096)
            except ValueError:
                break
            yield asin, np_array


def generate_final_dataset(path_to_filtered_merge_data,
                           path_to_url_file,
                           path_to_binary_features,
                           output_path,
                           output_features_path):
    """
    given the path of the filtered merge data (contains a dataframe with amazon
    and openlibrary data merged with categories and years set)

    given a file containing a list of url separated by \n listing
    the url of each cover images

    given the path to a binary file which contains
    10 bytes ASIN then 4096 * 4 bytes float

    given the output file path

    generates to output file path a pickle for a dictionnary indexed by
    ASIN and containing years, category, features and ASIN
    """

    def single_date(years):
        if len(years) == 0:
            return -1
        else:
            return min(years)

    print("open dataset")
    with open(path_to_filtered_merge_data, 'rb') as f:
        df = pickle.load(f)

    print("url to path mapping")
    book_url_to_path = generate_book_to_url_mapping(path_to_url_file)

    df["year"] = df["publish_date"].map(single_date)
    df["has_file"] = df["image_url"].map(lambda url: url in book_url_to_path)
    df["file"] = df["image_url"].map(lambda url: book_url_to_path.get(url))

    print("cleanup")
    # cleanup
    df_filtered = df[(df["category"].notnull())& (df["category"] != "") & (df["year"] != -1) & (df["year"] != 0) & (df["sales_rank"].notnull()) & (df["has_file"] == True)]

    print("final dataframe")
    asin_list = df_filtered["asin"].tolist()
    asin_set = set(asin_list)

    columns_to_keep = ["asin", "year", "sales_rank", "category", "file"]
    final_dataset = df_filtered[columns_to_keep].set_index("asin").to_dict(orient="index")
    final_dataset_features = dict()
    found = set()

    print("load features, can take time")
    for k, features in read_image_features(path_to_binary_features):
        asin = k.decode("utf-8")
        if asin in asin_set:
            found.add(asin)
            final_dataset_features[asin] = features

    to_remove = asin_set - found
    for asin in to_remove:
        del final_dataset[asin]

    print("initial_length={}, filtered_length={}, final_length={}".format(len(df), len(df_filtered), len(final_dataset)))

    with open(output_path, "wb") as f:
        pickle.dump(final_dataset, f)
    print("export features")
    with open(output_features_path, "wb") as f:
        pickle.dump(final_dataset_features, f)


generate_final_dataset("../filtered_merge_data.pickle", "url.txt", "../image_features_Books.b.1", "truc.pickle", "truc.features.pickle")
