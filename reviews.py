import json
from collections import Counter
from random import sample, shuffle


# A generator for reading the JSON file.
def gen_examples(filename, max_length=None):
    with open(filename) as f:
        for review in json.load(f):
            if not max_length or len(review['text'].split()) < max_length:
                if review['rating'] not in ('2','4'):
                    yield((review['title'],review['text'],review['rating']))


def get_reviews():
    # Read the titles, bodies and ratings of all reviews.
    filename = '/data/reviews.json'
    titles,bodies,ratings = zip(*(gen_examples(filename, max_length=None)))

    print('Total number of reviews: {}'.format(len(ratings)))



    # The number of reviews is not equally distributed among the ratings. In the next step, we downsample the reviews so that there is the same number for each rating. The discarded reviews are picked at random.

    counter = Counter(ratings)

    print(counter)

    min_count = counter.most_common()[-1][1]

    indices = []

    for r  in list(counter):
        indices.extend(
            sample(
                [i for i,e in enumerate(ratings) if e==r],
                min_count
            )
        )

    shuffle(indices)
    titles,bodies,ratings = zip(*((titles[k],bodies[k],ratings[k]) for k in indices))
    del indices

    punctuation = '!.?:'
    
    labels = [dict((v,k) for k,v in enumerate(sorted(list(counter))))[rating] for rating in ratings]
    ratings = [int(r) for r in ratings]
    
    return titles,bodies,ratings,labels,punctuation
