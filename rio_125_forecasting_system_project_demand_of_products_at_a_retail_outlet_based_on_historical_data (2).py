# -*- coding: utf-8 -*-
"""Rio -125 /Forecasting System - Project Demand of Products at a Retail Outlet Based on historical data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A7vqLudVsMrAmL6zLXm0Imuh-2EFPJ_x
"""

#importing necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
!pip install pmdarima
from pmdarima import auto_arima
import pmdarima as pm

from sklearn.metrics import mean_squared_error,mean_absolute_error
from statsmodels.tools.eval_measures import rmse

import warnings
warnings.filterwarnings("ignore")
sns.set_style('darkgrid')

!pip install Prophet
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from google.colab import drive

!pip install --upgrade xlrd

#reading data to python environment
pd.set_option('display.max_columns', 9994)
df = pd.read_excel("/content/Superstore.xls")
df.head()

"""### **Exploratory Data Analysis**"""

df.shape

df.info()

df.corr()['Sales']



"""other Features have no correlation with the sales feature.

# *Indexing time series data*
"""

df = df.set_index(['Order Date'])

df.index.min(), df.index.max()

"""Note:
The dataset used for this project is a superstore data from 2014 to 2018 containing 9994 entries and 21 features and this is a time series data.
Dataset contains object, float and integer Data types and the date columns are already in datetime format.
there is no feature having strong correlation with sales feature.
For forecasting, we are using mainly the Sales Data with the order data of different product categories.

## **Visualising Data**
"""

from pylab import rcParams
rcParams['figure.figsize'] = 15, 9
df['Sales'].plot();

"""Resampling Data"""

#monthly mean sales begin
mean_monthlysales = df.resample(rule='MS').mean()['Sales']
print(mean_monthlysales)
mean_monthlysales.plot(figsize=(15,5),c='green')
plt.show()

"""Note:
Mean monthly sales is maximum in month march of year 2014.
Also on month sep 2014, jan 2015, march 2016, oct 2016 shows higher sales.
There is a huge dip in the graph during feb 2014 which shows least sales.
"""

df.resample(rule='A').max()['Profit'].plot(kind='bar', figsize = (12,4))
plt.show()

"""Note: maximum profit is observed in the year 2016 and least in the year 2015.

## **Data Pre-processing**
"""

#checking different categories in 'category' column
df['Category'].unique()

#checking for missing values
df.isna().sum()

"""Note: The Dataset not containing any missing values."""

#checking for unique values in columns
{column: len(df[column].unique()) for column in df.columns}

df = df.copy()
#dropping unnecessary columns
col = ['Row ID','Country','Customer Name','Product Name','Order ID','Customer ID','Ship Date','Ship Mode','Segment','City','State','Postal Code','Region','Product ID','Sub-Category','Quantity','Discount','Profit']
df.drop(col,axis=1, inplace=True)

df.shape

"""# Since dataset contain multiple categories of products we have to create seperate Dataframes for each category for analysis.

FURNITURE
"""

#selecting rows where category is furniture
furniture_data = df.loc[df['Category'] == 'Furniture']
furniture_data

furniture_data.drop('Category',axis=1, inplace=True)

furniture_data.head()

#sorting by order date
furniture_data = furniture_data.sort_values('Order Date')
furniture_data

furniture_data.describe()

furniture_data.index

#taking monthly mean sales of category furniture
y_furniture = furniture_data['Sales'].resample('MS').mean()

#observing mean monthly sales of furnitures
y_furniture.plot(figsize = (15,5))
plt.title('Mean Monthly Sales of Furniture items', fontsize=16, fontweight='bold')
plt.show()

"""Note: average sales is maximum at Jan 2015"""

furniture_data.plot(figsize=(15,5))
plt.show()

#checking for outliers
fig = plt.figure(figsize=(8,6))
sns.boxplot(y_furniture).set_title('Box Plot on sales of furniture items')
plt.show()

"""There is one outlier in the furniture data.

# OFFICE SUPPLIES
"""

office_supplies_data = df.loc[df['Category'] == 'Office Supplies']
office_supplies_data

office_supplies_data.drop('Category',axis=1, inplace=True)

office_supplies_data = office_supplies_data.sort_values('Order Date')
office_supplies_data.head()

office_supplies_data.describe()

office_supplies_data.index

y_office = office_supplies_data['Sales'].resample('MS').mean()

y_office.plot(figsize = (15,5))
plt.title('Mean Monthly Sales of office items', fontsize=16, fontweight='bold')
plt.show()

"""Sales for office supplies shows maximum at start of year between feb to april and minimum at end of year."""

office_supplies_data.plot(figsize=(15,5), c = 'grey')
plt.show()

fig = plt.figure(figsize=(8,6))
sns.boxplot(y_office).set_title('Box Plot on sales of office items')
plt.show()

"""there are three outliers in the office items data.

## Technology items
"""

technology_data = df.loc[df['Category'] == 'Technology']
technology_data

technology_data.drop('Category',axis=1, inplace=True)

technology_data = technology_data.sort_values('Order Date')

technology_data.describe()

technology_data.index

technology_data.index.min(), technology_data.index.max()

y_technology = technology_data['Sales'].resample('MS').mean()

y_technology.plot(figsize = (15,5))
plt.title('Mean Monthly Sales of Technology items', fontsize=16, fontweight='bold')
plt.show()

"""Technology items have highest sales in march 2014 and also in oct-nov of 2016."""

technology_data.plot(figsize=(15,5), c = 'green', legend = True)
plt.show()

fig = plt.figure(figsize=(8,6))
sns.boxplot(y_technology).set_title('Box Plot on technology items')
plt.show()

"""there are two outliers in the technology data.

### Seasonal Decomposition of each category

# Furniture items
"""

from pylab import rcParams
rcParams['figure.figsize'] = 12, 9
decomposition = sm.tsa.seasonal_decompose(y_furniture, model='additive')
fig = decomposition.plot()
plt.show()

"""Decreasing trend is observed for the sales of furniture after 2015.

# Office items
"""

from pylab import rcParams
rcParams['figure.figsize'] = 12, 9
decomposition = sm.tsa.seasonal_decompose(y_office, model='additive')
fig = decomposition.plot()
plt.show()

"""From the trend graph,there is a rise in curve and reaches a maximum at middle of 2014 after that there is huge fall in sales from 2015 to 2016. Then it gradually rises reach a maximum at beginning of 2016 and repeats.

## Technology
"""

from pylab import rcParams
rcParams['figure.figsize'] = 12, 9
decomposition = sm.tsa.seasonal_decompose(y_technology, model='additive')
fig = decomposition.plot()
plt.show()

"""Above plot shows an upward trend of sales of technology in the middle of 2016 after that it shows decreasing.

## Test for stationarity
"""

#Augmented dickey-fuller test
#H0 : data is non stationary (unit root =1)
#H1 : data is stationery (unit root <1)

def adfuller_test(series):
    result = adfuller(series)
    labels = ['ADF test statistic', 'p-value', 'Number of observations used', '#lags used']
    for value, label in zip(result, labels):
        print(label+' : '+str(value))

    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")

adfuller_test(y_furniture)

adfuller_test(y_office)

adfuller_test(y_technology)

"""Findings:
The p-value<0.05, so rejecting null hypothesis and assume a stationery datasets.
Here the differencing value (d) is zero.

## Autocorrelation and Partial Autocorrelation plots

ACF measures correlation between the time series with a lagged version itself and PACF similiar to ACF but after eliminating the variations.

## Furniture
"""

fig, axes = plt.subplots(1,2,figsize=(16,3), dpi= 100)
sm.graphics.tsa.plot_pacf(y_furniture,lags=23,method="ols",ax=axes[0])
sm.graphics.tsa.plot_acf(y_furniture, lags=23,ax=axes[1])
plt.show()

"""## Office supplies"""

fig, axes = plt.subplots(1,2,figsize=(16,3), dpi= 100)
sm.graphics.tsa.plot_pacf(y_office,lags=23,method="ols",ax=axes[0])
sm.graphics.tsa.plot_acf(y_office, lags=23,ax=axes[1])
plt.show()

"""# Technology"""

fig, axes = plt.subplots(1,2,figsize=(16,3), dpi= 100)
sm.graphics.tsa.plot_pacf(y_technology,lags=23,method="ols",ax=axes[0])
sm.graphics.tsa.plot_acf(y_technology, lags=23,ax=axes[1])
plt.show()

"""# Parameter selection
Parameters of the ARIMA model are defined by

AR(p)-lag order

I(d) -degree of difference

MA(q) - order of moving average

SARIMAX an extension of ARIMA supports time series data with a seasonal component. it is denoted by order (p,d,q)(P,D,Q)m.

P - Seasonal regression

D - differencing

Q - moving average coefficients

m - no.of datapoints in each seasonal cycle

# Here two approaches are used to find optimal parameters for SARIMA model, one by using pmdarima and other by sarimax function of statsmodel.

for pmdarima data is splitted into test and train data (train data from 2014 to 2015 and remaining data is used as test data (from 2016 to 2017).

## Furniture
"""

#splitting into test and train
train1 = y_furniture.loc['2014-01-06':'2015-12-30']
test1 = y_furniture.loc['2015-12-30':]

"""# approach 1: Using pyramid ARIMA for choosing best parameters"""

model = pm.auto_arima(train1, start_p=1, start_q=1,
                      test='adf',        # use adftest to find optimal 'd'
                      max_p=3, max_q=3,  # maximum p and q
                      m=12,              # frequency of series
                      d=None,            # let model determine 'd'
                      seasonal=True,     #  Seasonality
                      start_P=0,
                      D=0,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=True)

print(model.summary().tables[1])

model.fit(train1)

model_furniture = SARIMAX(y_furniture,order=(0,1,0),seasonal_order=(1,0,0,12),enforce_invertibility=False)

result_furniture = model_furniture.fit()

result_furniture.plot_diagnostics(figsize=(16,8))
plt.show()

"""Residuals are normally distributed and uncorrelated."""

start = len(train1)
end = len(train1) + len(test1) - 1

prediction_furniture = result_furniture.predict(start,end).rename('SARIMA model')
prediction_furniture

test1.plot(figsize=(12,8),legend=True)
prediction_furniture.plot(legend=True)
plt.title("Furniture item sales")
plt.show()

"""Observed and SARIMA prediction are almost close.

## Evaluating model
"""

mean_squared_error(test1,prediction_furniture)

rmse(test1,prediction_furniture)

test1.mean()

model_furniture_ = SARIMAX(y_furniture,order=(0,1, 0),seasonal_order=(1, 0, 0, 12),enforce_invertibility=False)

result_furniture_final = model_furniture_.fit()

forecast_furniture = result_furniture_final.predict(len(y_furniture),len(y_furniture)+11,typ='levels').rename('SARIMA Forecast')
y_furniture.plot(legend=True,figsize=(15,8))
forecast_furniture.plot(legend=True)
plt.show()

"""Decreasing trend is observed from forecast as from above graph."""

pred_furniture = result_furniture_final.get_forecast(steps=24)
pred_ci_furniture = pred_furniture.conf_int()
ax = y_furniture.plot(label='observed',figsize=(15,10))
pred_furniture.predicted_mean.plot(ax=ax,label='Forecast')
ax.fill_between(pred_ci_furniture.index,
               pred_ci_furniture.iloc[:,0],
               pred_ci_furniture.iloc[:,1],alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Furniture Sales')
plt.legend()
plt.show()

"""#Forecast for next two years of furniture sales is predicted as constant.

# Approach 2: Choosing best parameters with lowest AIC score
"""

# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
simple_pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(i[0], i[1], i[2], 12) for i in list(itertools.product(p, d, q))]

print('Parameter combinations for Seasonal ARIMA...')

for param in simple_pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y_furniture,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)


            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

"""AIC estimates relative quality of model and desired result is to find lowest possible AIC score. The (p,d,q)(P,D,Q,m) order (0, 1, 1)(0, 1, 1, 12) have lower AIC value of 251.24."""

#fitting model
best_model = SARIMAX(y_furniture, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
print(best_model.summary().tables[1])

"""# Model diagnosis"""

best_model.plot_diagnostics(figsize=(18, 12))
plt.show()

"""Note:
From above plots,it is clear that the residuals are almost normally distributed and uncorrelated.

# Visualising Forecasts
"""

pred = best_model.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y_furniture['2014':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
plt.title('Forecast of Furniture items', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Furniture Sales')
plt.legend()

plt.show()

y_forecasted = pred.predicted_mean
y_truth = y_furniture['2017-01-01':]

mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

"""The Mean Squared Error of our forecasts is 7554.82
The Root Mean Squared Error of our forecasts is 86.92
"""

# Get forecast 24 steps ahead in future
pred = best_model.get_forecast(steps=24)

# Get confidence intervals of forecasts
pred_ci = pred.conf_int()

ax = y_furniture.plot(label='observed', figsize=(15, 8))

pred.predicted_mean.plot(ax=ax, label='forecast')

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], alpha=0.25)
plt.title('Forecast of Furniture items', fontsize=16, fontweight='bold')
ax.set_xlabel('year')
ax.set_ylabel('Occupancy')

plt.legend()
plt.show()

"""Here also Forecasts shows that the time series model is expected to slightly decreasing.

# office supplies
"""

train2 = y_office.loc['2014-01-06':'2015-12-30']
test2 = y_office.loc['2015-12-30':]

"""# approach 1: using pmdarima"""

model = pm.auto_arima(train2, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=12,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=True,   #  Seasonality
                      start_P=0,
                      D=0,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=True)

print(model.summary().tables[1])

model_office = SARIMAX(y_office,order=(2,2,1),seasonal_order=(0,0,0,12),enforce_invertibility=False)

result_office = model_office.fit()
result_office.plot_diagnostics(figsize=(16,8))
plt.show()

"""Residual plot shows residuals are close to normally distributed and also with Q-Q plot indicates normally distributed. frpm correlogram, residuals are uncorrelated."""

start = len(train2)
end = len(train2) + len(test2) - 1

prediction_office = result_office.predict(start,end).rename('SARIMA model')
prediction_office

test2.plot(figsize=(12,8),legend=True)
prediction_office.plot(legend=True)
plt.title("Office item sales");

"""Sales of office items high on months march of 2016 and january,september of 2017."""

mean_squared_error(test2,prediction_office)

rmse(test2,prediction_office)

test2.mean()

model_office_final = SARIMAX(y_office,order=(2, 2, 1),seasonal_order=(0, 0, 0, 12),enforce_invertibility=False)
result_office_final = model_office_final.fit()

forecast_office = result_office_final.predict(len(y_office),len(y_office)+11,typ='levels').rename('SARIMA forecast')

y_office.plot(legend=True,figsize=(12,8))
forecast_office.plot(legend=True)
plt.title("Office supplies sales");

pred_office = result_office_final.get_forecast(steps=24)
pred_ci_office = pred_office.conf_int()
ax = y_office.plot(label='observed',figsize=(15,9))
pred_office.predicted_mean.plot(ax=ax,label='Forecast')
ax.fill_between(pred_ci_office.index,
               pred_ci_office.iloc[:,0],
               pred_ci_office.iloc[:,1],color='k',alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Office supplies Sales')
plt.legend()
plt.show()

"""Slightly increasing trend in sales is observed for office items.

# approach2:
"""

# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
simple_pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(i[0], i[1], i[2], 12) for i in list(itertools.product(p, d, q))]

print('Parameter combinations for Seasonal ARIMA...')

warnings.filterwarnings("ignore") # specify to ignore warning messages

for param in simple_pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y_office,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)


            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

#fitting model
best_model = SARIMAX(y_office, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
print(best_model.summary().tables[1])

best_model.plot_diagnostics(figsize=(15, 12))
plt.show()

"""Here residuals are near normally distributed from top right and bottom left plots and the correlation plot shows uncorrelated."""

pred = best_model.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y_office['2014':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
plt.title('Forecast of Sales for Office items', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('office Sales')
plt.legend()

plt.show()

y_forecasted = pred.predicted_mean
y_truth = y_office['2017-01-01':]

mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

# Get forecast 24 steps ahead in future
pred_uc = best_model.get_forecast(steps=24)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

ax = y_office.plot(label='observed', figsize=(15, 8))

pred_uc.predicted_mean.plot(ax=ax, label='forecast')

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
plt.title('Sales forecast of Office items', fontsize=16, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Occupancy')

plt.legend()
plt.show()

"""Forecast and confidence intervals shows demand of office items increasing over years.

## Technology
"""

train3 = y_technology.loc['2014-01-06':'2015-12-30']
test3 = y_technology.loc['2015-12-30':]

#approach 1: using pmdarima

model = pm.auto_arima(train3, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3,
                      m=12,
                      d=None,
                      seasonal=True,
                      start_P=0,
                      D=0,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=True)

print(model.summary().tables[1])

model_technology = SARIMAX(y_technology,order=(0,0,0),seasonal_order=(0,0,0,12),enforce_invertibility=False)

"""above indicate our data is white noise, we cannot predict with white noise data."""

result_technology = model_technology.fit()
result_technology.plot_diagnostics(figsize=(16,8))
plt.show()

"""It is clear that there are white noise in data so Lets try the second approach.

approach 2:
"""

# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
simple_pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(i[0], i[1], i[2], 12) for i in list(itertools.product(p, d, q))]

print('Parameter combinations for Seasonal ARIMA...')

for param in simple_pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y_technology,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)


            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

#fitting model
best_model = SARIMAX(y_technology, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)).fit()
print(best_model.summary().tables[1])

best_model.plot_diagnostics(figsize=(18, 12))
plt.show()

"""Residuals are normally distributed with zero mean and they are uncorrelated from correlogram. the model is good."""

pred = best_model.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y_technology['2014':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
plt.title('Sales Forecast of Technology items', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('technology Sales')
plt.legend()

plt.show()

y_forecasted = pred.predicted_mean
y_truth = y_technology['2017-01-01':]

mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

# Get forecast 24 steps ahead in future
pred_uc = best_model.get_forecast(steps=24)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

ax = y_technology.plot(label='observed', figsize=(15, 8))

pred_uc.predicted_mean.plot(ax=ax, label='forecast')

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
plt.title('Sales Forecast of Technology items', fontsize=16, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Occupancy')

plt.legend()
plt.show()

"""Somewhat constant trend in sales for technology items is observed.

## Comparing categories
"""

furniture_data.shape, office_supplies_data.shape, technology_data.shape

#furniture_data.drop('Category', axis=1, inplace=True)
#office_supplies_data.drop('Category', axis=1, inplace=True)
#technology_data('Category', axis=1, inplace=True)

furniture_data = furniture_data.sort_values('Order Date')
office_supplies_data = office_supplies_data.sort_values('Order Date')
technology_data = technology_data.sort_values('Order Date')

furniture_data = furniture_data.groupby('Order Date')['Sales'].sum().reset_index()
office_supplies_data= office_supplies_data.groupby('Order Date')['Sales'].sum().reset_index()
technology_data = technology_data.groupby('Order Date')['Sales'].sum().reset_index()

furniture_data = furniture_data.set_index('Order Date')
office_supplies_data = office_supplies_data.set_index('Order Date')
technology_data = technology_data.set_index('Order Date')

y_furniture = furniture_data['Sales'].resample('MS').mean()
y_office = office_supplies_data['Sales'].resample('MS').mean()
y_technology = technology_data['Sales'].resample('MS').mean()

furniture = pd.DataFrame({'Order Date': y_furniture.index , 'Sales':y_furniture.values})
furniture.head()

office = pd.DataFrame({'Order Date': y_office.index , 'Sales':y_office.values})
office.head()

technology = pd.DataFrame({'Order Date': y_technology.index , 'Sales':y_technology.values})
technology.head()

store = pd.merge(furniture,office, how='inner', on='Order Date')
store.rename(columns={'Sales_x': 'furniture_sales', 'Sales_y': 'office_sales', 'Sales_z': 'technology_sales'}, inplace=True)
store.head()

store_office_furniture_technology = technology.merge(store, how='inner', on='Order Date')
store_office_furniture_technology.rename(columns={'Sales': 'technology_sales', 'Sales_x':'furniture_sales','Sales_y':'office_sales'},inplace=True)
store_office_furniture_technology

sns.set(font_scale=1)
plt.figure(figsize=(20,8))
plt.plot(store_office_furniture_technology['Order Date'],store_office_furniture_technology['furniture_sales'],'p-',label='furniture')
plt.plot(store_office_furniture_technology['Order Date'],store_office_furniture_technology['office_sales'],'g-',label='office supplies')
plt.plot(store_office_furniture_technology['Order Date'],store_office_furniture_technology['technology_sales'],'r-', label='technology')
plt.xlabel('Date',fontsize=14,fontweight='bold')
plt.ylabel('Sales', fontsize = 14,fontweight='bold')
plt.title('Sales Data', fontsize=16, fontweight='bold')
plt.legend()
plt.show()

"""Findings:
from above plot, it is clear that technology items are most selling item compare to other categories and sales of office supplies is least.

sales of technology items is more than 2000 in the year 2014 but after that sales is declining in 2015.

Sales of furniture items shows a maximum at the end of year 2014 and a similiar rise occurs in second half of 2015 and 2016.

office supplies has maximum sales at the end of 2016.

## comparing sales of different categories

a) Furniture vs office items
"""

store.head()

plt.figure(figsize=(20,8))

plt.plot(store['Order Date'],store['furniture_sales'],'p-',label='furniture')
plt.plot(store['Order Date'],store['office_sales'],'g-',label='office supplies')

plt.xlabel('Date',fontsize=14,fontweight='bold')
plt.ylabel('Sales', fontsize = 14,fontweight='bold')
plt.title('Sales of Furniture and Office items', fontsize=16, fontweight='bold')
plt.legend()
plt.show()

"""sales of both product categories is increasing over years.
for office supplies, it shows high sales during the month of september 2016 and furniture items have also similiar sales at that time.
Furniture items have high sales during september 2014 and lower sales during march of 2014 and 2016 while Office items have lower sales during march 2014.
Sales of both categories are high during second half of year.

b) Furniture vs Technology items sales
"""

store_furniture_technology = pd.merge(furniture,technology, how='inner', on='Order Date')
store_furniture_technology.rename(columns={'Sales_x': 'furniture_sales', 'Sales_y': 'technology_sales'}, inplace=True)
store_furniture_technology.head()

plt.figure(figsize=(20,8))
plt.plot(store_furniture_technology ['Order Date'],store_furniture_technology ['furniture_sales'],'p-',label='furniture')
plt.plot(store_furniture_technology ['Order Date'],store_furniture_technology ['technology_sales'],'r-', label='technology')
plt.xlabel('Date',fontsize=14,fontweight='bold')
plt.ylabel('Sales', fontsize = 14,fontweight='bold')
plt.title('Sales of Furniture and Technology Items', fontsize=16, fontweight='bold')
plt.legend()
plt.show()

"""From above plot it is clear that technology items has more demand than furniture items.

higher sales for technology is observed on month of march,september in 2014, secondly in october of 2017.
higher sales for furniture was observed at the end of 2014 (december).
Both of them have lower sales during the start of 2014 probably on month of february.

c) office items vs technology sales
"""

store_office_technology = pd.merge(office,technology, how='inner', on='Order Date')
store_office_technology.rename(columns={'Sales_x': 'office_sales', 'Sales_y': 'technology_sales'}, inplace=True)
store_office_technology.head()

plt.figure(figsize=(20,8))
plt.plot(store_office_technology ['Order Date'],store_office_technology ['office_sales'],'g-',label='office supplies')
plt.plot(store_office_technology ['Order Date'],store_office_technology ['technology_sales'],'r-', label='technology')
plt.xlabel('Date',fontsize=14,fontweight='bold')
plt.ylabel('Sales', fontsize = 14,fontweight='bold')
plt.title('Sales of Office and Technology Items', fontsize=16, fontweight='bold')
plt.legend()
plt.show()

"""# Increasing trend is observed for both categories from 2014 to 2018. Here also technology items have higher sales than office supplies which makes it highly demandable product. Higher sales of furniture was observed on september of 2016.

# Findings:
# Technology items is the highest selling product category.
# Office items is least selling category in the superstore.

## Forecasting using **Fbprophet** **library**

# Furniture
"""

y_furniture_df = y_furniture.to_frame()
y_furniture_df['ds'] = y_furniture_df.index
y_furniture_df.columns = ['y','ds']
y_furniture_df

m_furniture = Prophet()

m_furniture.fit(y_furniture_df)

future_furniture = m_furniture.make_future_dataframe(periods=24,freq='MS')

future_furniture

forecast_furniture = m_furniture.predict(future_furniture)
forecast_furniture

forecast_furniture.columns

forecast_furniture[['ds','yhat_lower', 'yhat_upper','yhat']].tail(12)

m_furniture.plot(forecast_furniture);
plt.title('Sales of furniture')
plt.xlabel('Years')
plt.ylabel('Sales');

"""Above plot is forecasting of furniture items sales for the next two years and it shows decreasing trend in sales for the upcoming years.

High sales is predicted on December of 2018 and August, september in 2019.
Low sales is expected at the beginning of year around February for both categories.
Compared to 2018, 2019 have lower sales of furniture in the month of december and high sales in March than in 2018.
"""

plot_plotly(m_furniture, forecast_furniture)
forecast_furniture.plot(x='ds',y='yhat',figsize=(12,5))

m_furniture.plot_components(forecast_furniture);

"""Note:
The trend plot shows linearly decreasing demand of furniture items from 2014 to 2020.
From the yearly seasonality plot, it is clear that high seasonality occur in the month of november and December.
low seasonality is seen middle of January and in february.
"""

plot_components_plotly(m_furniture , forecast_furniture)

"""**Note**:
Higher seasonality on December 16, August 16 is predicted from the plot.
Lower seasonality predicted on January 15, March 16, July 19.

# Office supplies
"""

y_office_df = y_office.to_frame()
y_office_df['ds'] = y_office_df.index
y_office_df.columns = ['y','ds']
y_office_df

m_office = Prophet()

m_office.fit(y_office_df)

future_office = m_office.make_future_dataframe(periods=24,freq='MS')

future_office

forecast_office = m_office.predict(future_office)
forecast_office

forecast_office.columns

forecast_office[['ds','yhat_lower', 'yhat_upper','yhat']].tail(12)

m_office.plot(forecast_office)
plt.title('Sales of office items')
plt.xlabel('Years')
plt.ylabel('Sales')
plt.show()

"""Note:
Above plot shows increasing sales of office items for the next two years.
Higher sales predicted at the end of year probably in the months of September, November, December in 2019. In 2018 higher sales predicted on march.
In both 2018 and 2019, lower Sales are expected on month of may.
"""

plot_plotly(m_office, forecast_office)
forecast_office.plot(x='ds',y='yhat',figsize=(12,5))

m_office.plot_components(forecast_office);

"""Note:
From trend plot, a linearly increasing trend is observed for the sales of office items, which indicates increasing demand of office items for the next few years.
Higher seasonality is observed on mid of january and lower seasonality on Mid of November.
"""

plot_components_plotly(m_office, forecast_office)

"""Higher seasonality on January 16 and lowest on November 15 is predicted.

# Technology
"""

y_technology_df = y_technology.to_frame()
y_technology_df['ds'] = y_technology_df.index
y_technology_df.columns = ['y','ds']
y_technology_df

m_technology = Prophet()

m_technology.fit(y_technology_df)

future_technology = m_technology.make_future_dataframe(periods=24,freq='MS')

future_technology

forecast_technology = m_technology.predict(future_technology)
forecast_technology

forecast_technology.columns

forecast_technology[['ds','yhat_lower', 'yhat_upper','yhat']].tail(12)

m_technology.plot(forecast_technology);
plt.title('Sales of technology')
plt.xlabel('Years')
plt.ylabel('Sales')

"""From the graph, Higher sales was observed in the year 2016 during month of August-september in 2016.
In 2018 and 2019 higher sales is predicted on month of march respeectively.
Lower sales in 2018 is predicted on december and in 2019 it is predicted on October, which indicate lesser demand on these months.
Sales of technology products is predicted as same as previous years.
"""

plot_plotly(m_technology, forecast_technology)
forecast_technology.plot(x='ds',y='yhat',figsize=(12,5))
m_technology.plot_components(forecast_technology);

plot_components_plotly(m_technology, forecast_technology)

"""A decreasing trend in sales is expected for technology items eventhough their sales are comparatively higher than other product categories.

high seasonality is expected on mid october and mid january.
lower seasonality on middle of september is predicted.
Note:
Demand of office items is increasing as predicted from the above graphs.
Trend of technology items linearly decreasing over years so demand of products is decreasing.
Demand of furniture items is predicted as steadily decreasing.

## **Conclusion**:
# Demand of office items is increasing as predicted by SARIMA model and Fbprophet.
# Demand of furniture items is predicted as steadily decreasing.
## Demand of Technology items is slightly decreasing but it have comparatively large amount of sales.
# Suitable Business strategies have to be implemented to improve sales of product category furniture.
"""