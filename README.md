<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forecasting System - Demand Prediction for Retail Outlet</title>
</head>
<body>
    <h1>Forecasting System - Demand Prediction for Retail Outlet</h1>

    <h2>📄 Project Overview</h2>
    <p>This project aims to predict the demand for various product categories (furniture, office supplies, and technology) at a retail outlet, based on historical data from 2014 to 2018. By applying time series forecasting models, this project helps optimize inventory management and provides actionable insights into seasonal sales trends across product categories.</p>

    <h2>📊 Objective</h2>
    <p>The project’s primary objective is to build a robust <strong>forecasting system</strong> to assist retail outlets in:</p>
    <ul>
        <li><strong>Inventory Planning:</strong> Align inventory with forecasted demand to reduce overstocking or stockouts.</li>
        <li><strong>Business Strategy:</strong> Use demand insights to create promotions and marketing plans around high-demand periods.</li>
        <li><strong>Operational Efficiency:</strong> Improve resource allocation based on demand predictions.</li>
    </ul>

    <h2>⚙️ Technical Approach</h2>

    <h3>1. Data Preprocessing</h3>
    <ul>
        <li><strong>Data Cleaning:</strong> Ensured no missing values and eliminated irrelevant features like 'Row ID', 'Country', and 'Customer Name'.</li>
        <li><strong>Resampling:</strong> Aggregated sales data to monthly means for smoother trend and seasonality analysis.</li>
        <li><strong>Outlier Detection:</strong> Identified outliers within each product category (e.g., Furniture, Office Supplies, Technology) using box plots.</li>
    </ul>

    <h3>2. Time Series Analysis</h3>
    <ul>
        <li><strong>Stationarity Testing:</strong> Employed the <strong>Augmented Dickey-Fuller (ADF) test</strong> to confirm that the time series data was stationary.</li>
        <li><strong>Seasonal Decomposition:</strong> Used <code>statsmodels</code> to decompose the time series for each product category, analyzing trends, seasonality, and residuals.</li>
    </ul>

    <h3>3. Forecasting Models</h3>
    <ul>
        <li><strong>SARIMA (Seasonal ARIMA):</strong> Applied SARIMA models for each product category, optimizing parameters to minimize the AIC score.</li>
        <li><strong>FbProphet:</strong> Leveraged <code>fbprophet</code> for additional predictive modeling, providing both trend and seasonal forecasts, particularly for extended forecasts beyond SARIMA's capabilities.</li>
        <li><strong>Model Evaluation:</strong> Evaluated predictions using Mean Squared Error (MSE) and Root Mean Squared Error (RMSE) to measure model accuracy.</li>
    </ul>

    <h2>📈 Results and Findings</h2>
    <ul>
        <li><strong>Furniture:</strong> Displayed a decreasing sales trend post-2015 with high seasonality peaks in late Q4 each year.</li>
        <li><strong>Office Supplies:</strong> Predicted an upward trend, especially in early Q2 and Q4, suggesting increased demand toward the year-end.</li>
        <li><strong>Technology:</strong> Despite high initial sales, forecasted a steady decline over time, with demand spikes in Q3.</li>
    </ul>

    <p><strong>Visual Insights:</strong></p>
    <ul>
        <li>Plots for each category show trends, seasonality, and residuals, offering insights into both annual demand cycles and monthly fluctuations.</li>
        <li>SARIMA and Prophet models provided confidence intervals, highlighting periods of higher uncertainty in predictions.</li>
    </ul>

    <h2>🔍 Business Implications</h2>
    <ul>
        <li><strong>Inventory Management:</strong> Optimize inventory cycles based on forecasted demand, reducing costs associated with overstocking or stockouts.</li>
        <li><strong>Promotional Strategies:</strong> Focus marketing efforts during high-demand periods (e.g., late Q4 for furniture, early Q2 for office supplies).</li>
        <li><strong>Resource Allocation:</strong> Adjust workforce and resources according to forecasted demand peaks, improving operational efficiency.</li>
    </ul>

    <h2>🛠️ Technologies Used</h2>
    <ul>
        <li><strong>Programming Languages:</strong> Python</li>
        <li><strong>Libraries:</strong> Pandas, Numpy, Statsmodels, FbProphet, Matplotlib, Seaborn, pmdarima</li>
        <li><strong>Tools:</strong> Jupyter Notebook, Google Colab</li>
    </ul>

    <h2>🗂 Repository Structure</h2>
    <pre>
|-- data/
    |-- Superstore.xls             # Raw data file
|-- notebooks/
    |-- Forecasting_System.ipynb   # Main notebook for analysis and modeling
|-- images/
    |-- demand_trends.png          # Trend and seasonality plots
|-- README.md                      # Project documentation
    </pre>

    <h2>📌 Getting Started</h2>
    <p>To get started, follow these steps:</p>
    <h3>1. Install Dependencies:</h3>
    <pre>
        pip install pandas numpy statsmodels pmdarima fbprophet matplotlib seaborn
    </pre>

    <h3>2. Run the Notebook:</h3>
    <p>Open <code>Forecasting_System.ipynb</code> in Jupyter or Google Colab, and execute cells sequentially to reproduce results.</p>

    <h2>🤝 Collaborations and Contributions</h2>
    <p>Interested in collaborating or have suggestions? Feel free to reach out or submit a pull request!</p>
</body>
</html>
