from scipy.sparse.csr import csr_matrix 
import numpy as np
import random
import matplotlib.pyplot as plt


def load_data(ordered_asins, ordered_features, df): 
    
    asins = {}
    set_asins = []
    set_filtered_asins = set(ordered_asins)

    #Keep lins of df for wich we have features
    for d, c, p, s in zip(df['asin'],\
                          df['category'],\
                          df['publish_date'],\
                          df['sales_rank']):
        
        if d in set_filtered_asins:
            asins[d] = [c, p, s]
            set_asins.append(d)

    set_asins = set(set_asins)
    
    features = []
    a = []
    category = []
    publish_date = []
    sales_rank = []

    for f_a, f in zip(ordered_asins, ordered_features):
        if(f_a in set_asins and asins[f_a][0] is not None): 
            category.append(asins[f_a][0])
            publish_date.append(max(asins[f_a][1]))
            sales_rank.append(asins[f_a][2])
            a.append(f_a)
            features.append(np.array(f.flat))
            
    return a, features, category, publish_date, sales_rank

def plot_by_cluster(clusters, target_info):
    info = range(len(np.unique(target_info)))
    k = len(np.unique(clusters))
    f = plt.figure(figsize=(15, 20))

    #Entire ceil division 
    plot_rows = k//2
    if(k%2 > 0): 
        plot_rows +=1
    
    for i in range(k): 
        args = []
        for e, c in enumerate(clusters): 
            if c == i+1: 
                args.append(target_info[e])

        ax = plt.subplot(plot_rows, 2, i + 1) 
        ax.set_title("Cluster={}".format(i+1))
        n, bins, patches = plt.hist(args, bins=len(np.unique(target_info)))
        plt.xticks(bins + .5, info)
        plt.xticks(rotation=90)

    plt.show()
    
def equalize_by_category(asins, features, category, publish_date, sales_rank, num_by_category=2000): 
    eq_asins = []
    eq_features = []
    eq_category = []
    eq_publish_date = []
    eq_sales_rank =[]

    #Count data by category
    categories, counts = np.unique(category, return_counts=True)
    d = dict()
    for cat, count in zip(categories, counts): 
        d[cat] = count

    for a, f, c, p, s in zip(asins, features, category, publish_date, sales_rank):
        if d[c] > num_by_category: 
            keep = num_by_category/(d[c])
            if random.random() < keep: 
                eq_asins.append(a)
                eq_features.append(f)
                eq_category.append(c)
                eq_publish_date.append(p)
                eq_sales_rank.append(s)
  
    return eq_asins, eq_features, eq_category, eq_publish_date, eq_sales_rank


def equalize_by_year(asins, features, category, publish_date, sales_rank, num_by_category=2000): 
    eq_asins = []
    eq_features = []
    eq_category = []
    eq_publish_date = []
    eq_sales_rank =[]

    #Count data by category
    year, counts = np.unique(publish_date, return_counts=True)
    d = dict()
    for y, count in zip(year, counts): 
        d[y] = count

    for a, f, c, p, s in zip(asins, features, category, publish_date, sales_rank):
        if d[p] > num_by_category: 
            keep = num_by_category/(d[p])
            if random.random() < keep: 
                eq_asins.append(a)
                eq_features.append(f)
                eq_category.append(c)
                eq_publish_date.append(p)
                eq_sales_rank.append(s)
  
    return eq_asins, eq_features, eq_category, eq_publish_date, eq_sales_rank