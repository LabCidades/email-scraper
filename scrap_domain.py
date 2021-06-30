import pandas as pd
import glob
import os

if __name__ == '__main__':

    files = glob.glob('output/*.csv')
    df = pd.concat([pd.read_csv(fp).assign(
        url=os.path.basename(fp).split('.')[0]) for fp in files])


