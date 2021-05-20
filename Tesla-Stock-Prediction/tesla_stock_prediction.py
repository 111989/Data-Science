import pandas as pd
import quandl, math, random, datetime
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
from linear_regression import LinearRegression, train_test_split

style.use('ggplot')


dataframe = quandl.get('WIKI/TSLA')
print(dataframe.head())

dataframe = dataframe[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
dataframe['high_close_percentage'] = (dataframe['Adj. High'] - dataframe['Adj. Close']) / dataframe['Adj. Close'] * 100
dataframe['change_percentage'] = (dataframe['Adj. Close'] - dataframe['Adj. Open']) / dataframe['Adj. Open'] * 100
dataframe.fillna(value = -99999, inplace = True)
shift_period = int(math.ceil(0.01*len(dataframe)))
dataframe['label'] = dataframe['Adj. Close'].shift(periods = -shift_period)


X = np.array(dataframe.drop(labels = ['label'], axis = 1))
X = preprocessing.scale(X)
X_predict = X[-shift_period:]
X = X[:-shift_period] 
dataframe.dropna(inplace = True)
y = np.array(dataframe['label'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
accuracy_linear = linear_model.score(X_test, y_test)
print(accuracy_linear)
y_predicted = linear_model.predict(X_predict)
print(y_predicted)


dataframe['Prediction'] = np.nan
last_date = dataframe.iloc[-1].name
last_unix_value = last_date.timestamp()
n_seconds = 86400 
next_unix_value = last_unix_value + n_seconds

for prediction in y_predicted:
    next_date = datetime.datetime.fromtimestamp(next_unix_value)
    next_unix_value += n_seconds
    dataframe.loc[next_date] = [np.nan for _ in range(len(dataframe.columns) - 1)] + [prediction]

dataframe['Adj. Close'].plot()
dataframe['Prediction'].plot()
plt.legend(loc = 4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

