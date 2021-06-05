import numpy as np 
import pandas as pd 
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from keras.layers import LSTM
from sklearn.model_selection import KFold, cross_val_score, train_test_split


orders_file = 'olist_orders_dataset.csv'
items_file = 'olist_order_items_dataset.csv'


id = 'order_id'
cus = 'customer_id'
status = 'order_status'
purchase_timestamp = 'order_purchase_timestamp'


orders = pd.read_csv(orders_file, index_col=0, parse_dates=[purchase_timestamp]).sort_values(by=purchase_timestamp, ascending=True)

orders['month'] = orders[purchase_timestamp].dt.month
orders['year'] = orders[purchase_timestamp].dt.year
orders['weekday'] = orders[purchase_timestamp].dt.weekday
orders['day'] = orders[purchase_timestamp].dt.day

successful_statuses = ['delivered' 'invoiced' 'shipped' 'processing', 'created' 'approved']
successful_orders = orders[(orders[status] != 'canceled') & (orders[status] != 'unavailable')]

items = pd.read_csv(items_file, index_col=0)
order_items = pd.merge(orders, items, how='left', on='order_id')


sales = order_items.groupby(['month', 'year'], as_index=False)['price'].sum()
sales = sales[sales['year'].isin([2018, 2017])]
sales = sales.sort_values(['year', 'month'])
sales['date'] = '{year}-{month}'.format(year=sales['year'], month=sales['month'])


df_diff = sales.copy()
df_diff['prev_price'] = df_diff['price'].shift(1)
df_diff = df_diff.dropna()
df_diff['diff'] = (df_diff['price'] - df_diff['prev_price'])
df_supervised = df_diff.drop(['prev_price'],axis=1)


for inc in range(1,13):
    field_name = 'lag_' + str(inc)
    df_supervised[field_name] = df_supervised['diff'].shift(inc)

df_supervised = df_supervised.dropna().reset_index(drop=True)

df_model = df_supervised.drop(['month','price', 'year', 'date'],axis=1)
train_set, test_set = df_model[0:-6].values, df_model[-6:].values

#apply Min Max Scaler
scaler = MinMaxScaler(feature_range=(-1, 1))
scaler = scaler.fit(train_set)
# reshape training set
train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
train_set_scaled = scaler.transform(train_set)
# reshape test set
test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
test_set_scaled = scaler.transform(test_set)

X_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1]
X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test, y_test = test_set_scaled[:, 1:], test_set_scaled[:, 0:1]
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

model = Sequential()
model.add(LSTM(4, batch_input_shape=(1, X_train.shape[1], X_train.shape[2]), stateful=True))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1, shuffle=False)

y_pred = model.predict(X_test,batch_size=1)

y_pred = y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])
pred_test_set = []
for index in range(0,len(y_pred)):
    np.concatenate([y_pred[index],X_test[index]],axis=1)
    pred_test_set.append(np.concatenate([y_pred[index],X_test[index]],axis=1))
#reshape pred_test_set
pred_test_set = np.array(pred_test_set)
pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])
#inverse transform
pred_test_set_inverted = scaler.inverse_transform(pred_test_set)

#create dataframe that shows the predicted sales
result_list = []
sales_dates = list(sales[-7:].date)
act_sales = list(sales[-7:].price)
for index in range(0,len(pred_test_set_inverted)):
    result_dict = {}
    result_dict['pred_value'] = int(pred_test_set_inverted[index][0] + act_sales[index])
    result_dict['date'] = sales_dates[index+1]
    result_list.append(result_dict)
df_result = pd.DataFrame(result_list)

print(df_result)

