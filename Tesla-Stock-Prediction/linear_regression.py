import pandas as pd
import quandl, math, random, datetime
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


class LinearRegression:
    """
        Linear Regression heavily penalises 
        outliers. This implementation uses 
        Gradient Descent for optimisation.
    """
    def __init__(self, learning_rate = 0.1, iterations = 100):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def predict(self, X_predict):
        self.X_predict = X_predict
        return self.X_predict.dot(self.weights) + self.bias

    def fit(self, X_train, y_train):            
        self.X_train = X_train
        self.y_train = y_train
        self.n_samples, self.n_features = self.X_train.shape
        self.weights = np.zeros(self.n_features)
        self.bias = 0

        for _ in range(self.iterations):
            # update weights
            y_predicted = self.predict(self.X_train)
            gradient_weights = -2 * (self.X_train.T).dot(self.y_train - y_predicted) / self.n_samples
            gradient_bias = -2 * np.sum(self.y_train - y_predicted) / self.n_samples
            self.weights -= self.learning_rate * gradient_weights
            self.bias -= self.learning_rate * gradient_bias


    def score(self, X_test, y_test):
        self.X_test = X_test
        self.y_test = y_test
        residual_sum_of_squares = np.sum((self.y_test - self.predict(X_test))**2)
        total_sum_of_squares = np.sum((self.y_test - self.y_test.mean())**2)
        return 1 - (residual_sum_of_squares / total_sum_of_squares) if total_sum_of_squares != 0 else None



def train_test_split(X, y, test_size):
    """
        Randomly splits the input features 
        'X' and labels 'y' into 'X_train', 
        'X_test', 'y_train' and 'y_test' 
        such that 'X_test' has 'test_size' 
        samples.
    """
    X, y = pd.DataFrame(X), pd.DataFrame(y)
    if isinstance(test_size, float):
        test_size = round(test_size * len(X))
        
    indices = X.index.tolist()
    test_indices = random.sample(population = indices, k = test_size)
    X_test = X.loc[test_indices]
    y_test = y.loc[test_indices]
    X_train = X.drop(labels = test_indices)
    y_train = y.drop(labels = test_indices)
    
    return X_train, X_test, np.ravel(a = y_train), np.ravel(a = y_test)



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

