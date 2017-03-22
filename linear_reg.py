import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

import utils


def main():
    data_path = utils.to_data_dir('data.csv')
    with open(data_path, 'r') as file:
        df = pd.read_csv(file, index_col=False, header=0)

    xs = df.iloc[:, 1:]
    y = df.iloc[:, 0]

    X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.2, random_state=0)

    lr = linear_model.LinearRegression()

    lr.fit(X_train, y_train)

    # The coefficients
    # print('Coefficients: ', lr.coef_)
    # Explained variance score: 1 is perfect prediction
    print(f'Variance score: {lr.score(X_test, y_test):.2f}')

if __name__ == '__main__':
    main()
