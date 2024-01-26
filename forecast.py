import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load the data
data_path = 'combined_cleaned_data.csv'
data = pd.read_csv(data_path)

# Remove non-relevant rows at the top (if they exist)
data = data.iloc[2:].reset_index(drop=True)

# Convert 'Inwards Quantity' and 'Outwards Quantity' to numeric
data['Inwards Quantity'] = pd.to_numeric(data['Inwards Quantity'], errors='coerce')
data['Outwards Quantity'] = pd.to_numeric(data['Outwards Quantity'], errors='coerce')

# Fill NaN values with 0 for calculation
data.fillna({'Inwards Quantity': 0, 'Outwards Quantity': 0}, inplace=True)

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Drop rows with NaT in 'Date' column if they exist
data.dropna(subset=['Date'], inplace=True)

# Set 'Date' as the index of the dataframe
data.set_index('Date', inplace=True)

# Resample data to a quarter-end frequency and sum values within each quarter, using the 'QE' convention
data_quarterly = data.resample('QE', label='right', closed='right').sum()

# Prepare the ARIMA model for inwards quantity forecasting
model_in = ARIMA(data_quarterly['Inwards Quantity'], order=(1, 1, 1))
model_fit_in = model_in.fit()

# Forecast inwards quantity for the next quarter
forecast_in = model_fit_in.get_forecast(steps=1)
forecast_in_value = forecast_in.predicted_mean.iloc[0]

# Prepare the ARIMA model for outwards quantity forecasting
model_out = ARIMA(data_quarterly['Outwards Quantity'], order=(1, 1, 1))
model_fit_out = model_out.fit()

# Forecast outwards quantity for the next quarter
forecast_out = model_fit_out.get_forecast(steps=1)
forecast_out_value = forecast_out.predicted_mean.iloc[0]

# Plot the historical and forecasted quantities
plt.figure(figsize=(15, 8))
plt.plot(data_quarterly.index, data_quarterly['Inwards Quantity'], label='Historical Inwards Quantity', marker='o')
plt.plot(data_quarterly.index, data_quarterly['Outwards Quantity'], label='Historical Outwards Quantity', marker='o')

# Dates for forecast
forecast_date = data_quarterly.index[-1] + pd.offsets.QuarterEnd(1)

# Plot forecasted values with a line
plt.plot([data_quarterly.index[-1], forecast_date], [data_quarterly['Inwards Quantity'].iloc[-1], forecast_in_value], color='red', linestyle='--', marker='o', label='Forecasted Inwards Quantity')
plt.plot([data_quarterly.index[-1], forecast_date], [data_quarterly['Outwards Quantity'].iloc[-1], forecast_out_value], color='green', linestyle='--', marker='o', label='Forecasted Outwards Quantity')

# Adjust plot limits to make room for annotations
plt.ylim([0, plt.ylim()[1]*1.3])

# Annotate the forecasted quantities outside the plot area
plt.annotate(f'Forecast In: {forecast_in_value:,.0f}', (forecast_date, forecast_in_value), xytext=(0, 100), 
             textcoords='offset points', ha='center', va='bottom', color='red', arrowprops=dict(arrowstyle='->', color='red'))
plt.annotate(f'Forecast Out: {forecast_out_value:,.0f}', (forecast_date, forecast_out_value), xytext=(0, -100), 
             textcoords='offset points', ha='center', va='top', color='green', arrowprops=dict(arrowstyle='->', color='green'))

plt.xlabel('Year')
plt.ylabel('Quantity in Million Kgs')
plt.title('Quarterly Inwards and Outwards Quantity with Forecast')
plt.legend()
plt.grid(True)
plt.savefig('/mnt/data/corrected_forecast_graph.png')
plt.close()
