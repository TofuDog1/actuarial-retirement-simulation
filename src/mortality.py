import numpy
import pandas
from config import life_table_path

life_table_df = pandas.read_csv(life_table_path, index_col=0)
qx = life_table_df['qx'].array

def sample_death_age(start_age):
    age = start_age

    while numpy.random.random() > qx[age]:
        age += 1
    return age