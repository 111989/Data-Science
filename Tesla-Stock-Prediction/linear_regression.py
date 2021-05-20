import numpy as np
import pandas as pd
import random


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

