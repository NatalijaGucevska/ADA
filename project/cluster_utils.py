# This files contains functions useful to plot and manage
# data from our research on cluster of books

import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from math import ceil

grid_for_cluster = {
    10: (4,3),
    20: (4,5), 
    30: (6,5),
    50: (7,8),
    80: (9,9),
    100: (10,10),
    200: (15,14),
    250: (16,16),
    300: (18, 17),
    400: (20,20),
    500: (23,22),
    1000: [(15,15)] * 5,
    2000: [(15,15)] * 8,
    3000: [(20,20)] * 8,
    4000: [(20,20)] * 10,
}

def figsize_for_cluster(grid):
    """
    Compute the figure size given the number of row and columns
    """
    rows, columns = grid
    return (ceil(20.0 * columns / 4.0), ceil(15 * rows / 3.0))


def load_for(dimension, cluster, graph_data, precise=False):
    """
    Preload data to display interactively cluster without
    opening a pickle file each time.
    """
    Z_total, categories_list, categories_set, categories_label, years_list, years_set, category_to_index, year_to_index, books = graph_data
        
    filename = "cluster/dimension{}_cluster{}.pickle".format(dimension, cluster)
    if precise == True:
        filename = "cluster/dimension{}_cluster{}.pickle".format(dimension, cluster)
        
    zs = list()
    
    with open(filename, "rb") as f:
        x = pickle.load(f)
        

        for cluster_index in range(cluster):
            zs.append(np.zeros((len(years_set), len(categories_set))))

        for assignment, book in zip(x[1], books):
            year = book["year"]
            category = book["category"]

            if year in years_set and category in categories_set:
                zs[assignment][year_to_index[year]][category_to_index[category]] += 1
        
        old_settings = np.geterr()
        np.seterr(all="ignore")
        for cluster_index in range(cluster):
            zs[cluster_index] = zs[cluster_index] / Z_total
        np.seterr(**old_settings)
            
    return zs

def plot_3d(ax, Z, title, graph_data, hide_ticks=False):
    """
    Create a 3d plot for cluster dataset with as axis ticks and labels
    the years and the categories.
    """
    Z_total, categories_list, categories_set, categories_label, years_list, years_set, category_to_index, year_to_index, books = graph_data
    
    X = np.array(list(range(len(categories_list))))
    Y = np.array(list(range(len(years_list))))

    X, Y = np.meshgrid(X, Y)

    ax.title.set_text(title)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)

    #ax.set_zlim(0, 1.0)
    if not hide_ticks:
        plt.xticks(np.arange(len(categories_list)), categories_label, rotation=90)
        plt.yticks([x for x in range(len(years_list)) if x % 2 == 0], [y for y in years_list if y % 2 == 0])
    else:
        plt.xticks([])
        plt.yticks([])
        
def load_data(main_dataset):
    """
    return useful data needed to plot graphs for clustering of books
    return Z_total, categories_list, categories_set, categories_label, years_list, years_set, category_to_index, year_to_index, books
    
    where Z_total is the distribution of the book per shrinked years and categories
    where books is the list of the book used when we trained with the Kmeans algorithm
    """
    
    df = main_dataset

    # we create various set and years datastructure
    # - needed to check belong to relationship (seT)
    # - to plot graph (labels)
    # - to build graph data (value to indice)
    years_set = set(df["year"].unique())
    categories_set = set([x for x in df["category"].unique() if x is not None])
       
    years_list = list(range(1990, 2009))
    years_set = set(years_list)

    categories_list = list(categories_set)
    categories_list.sort(key=lambda x: x.lower())
    # truncate for plot for plot
    categories_label = [(label[:25] + '..') if len(label) > 25 else label for label in categories_list]

    category_to_index = dict()
    year_to_index = dict()
    
    for category in categories_set:
        category_to_index[category] = categories_list.index(category)
    for year in years_list:
        year_to_index[year] = years_list.index(year)
    
    # We reuse the exact dataset used with kmeans code
    asin_to_metadata = df[["category", "year"]].to_dict(orient="index")
    books = list()
    with open("test/dataset_with_years_and_categories_asins.txt", "r") as f:
        for l in f:
            asin = l.strip()
            if asin in asin_to_metadata:
                books.append(asin_to_metadata[asin])


    Z_total = np.zeros((len(years_set), len(categories_set)))   

    for i, book in df.iterrows():
        year = book["year"]
        category = book["category"]
        
        if year in years_set and category in categories_set:
            year_index = years_list.index(year)
            category_index = categories_list.index(category)

            Z_total[year_index][category_index] += 1
            
    return Z_total, categories_list, categories_set, categories_label, years_list, years_set, category_to_index, year_to_index, books