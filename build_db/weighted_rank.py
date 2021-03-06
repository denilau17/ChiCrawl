#code to calculate weighted rank for each bar

import sqlite3

#get average star rating for all chicago bars
def get_chicago_avg(c):
    s = "SELECT avg(rating) FROM bars"
    return c.execute(s).fetchall()[0][0]

#calculate weighted rank (Bayesian average) for a bar
def weighted_rank(num_reviews, num_stars, chi_avg):
    m = 5 #min number reviews to be listed
    b = (float(num_reviews)/(num_reviews+m))*num_stars + (float(m)/(num_reviews+m))*chi_avg
    return b

#input data to SQL database
def apply_wr(c):
    s = "SELECT name, rating, num_reviews FROM bars"
    values = c.execute(s).fetchall()
    rv = []
    for value in values:
        wr = weighted_rank(value[2], value[1], chi_avg)
        rv.append(wr)
        a = '''UPDATE bars SET weighted_rank = ''' + str(wr) + ''' WHERE name = "''' + str(value[0])+ '''"'''
        c.execute(a).fetchall()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    connection = sqlite3.connect("../data/bars3.db")
    c = connection.cursor()
    connection.create_function("weighted_rank", 3, weighted_rank)
    chi_avg = get_chicago_avg(c)
    apply_wr(c)
 
