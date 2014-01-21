PSQL + Pandas Awesomeness
==========================

(Pandas)[http://pandas.pydata.org/] is a popular library in Python that is commonly used for data analysis and it provides Python equivalent of the R dataframe that is fundamental to data analysis. Some engineers and data scientists however are increasingly adopting SQL based libraries for building large scale machine learning algorithms. (MADlib)(http://madlib.net) is one such library for scalable, parallel, in-database machine learning.

While there exist commercial tools to visualize data that is resides on databases (example: Tableau), many a times it would be cool to be able to quickly visualize the output of a SQL query, without having to switch to a commercial tool or have to use a wrapper to a SQL engine. The pandas_via_psql project just demonstrates how simple it is to redirect the output of a SQL query to some boilerplate Pandas's plotting functions, to quickly visualize the data from the command line.

Pre-Requsites
==============

You'll need Pandas to be installed on your machine. You should also have (PSQL)[http://www.postgresql.org/docs/8.1/static/app-psql.html] or a similar SQL command line interface to connect to your database and also ensure that you have password-less access to your remote database (set up SSH keys appropriately).

Datasets Used
==============

For this demo, I'm using two publicly available datasets. 
* [The UCI wine quality dataset](http://archive.ics.uci.edu/ml/datasets/Wine+Quality).
* [The S&P daily prices dataset]().


Usage
======

Invoke Pandas plotting functions by piping in the output from a psql query.
You can re-use this boiler-plate code for Scatter Plots, Box Plots, Histograms and Time Series Plots on your tables.


Scatter Matrix
===============

This is pretty useful when you are interested in analyzing the correlation between a bunch of features in a dataset, particularly in their correlation with the target attribute/label. You might then perform feature selection based on a visual output of the correlations.

Here is how the scatter matrix can be created on the UCI Wine Quality Dataset

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select * from wine;' | python plotter.py scatter
```

Here is the output ![Scatter Matrix of all features from the Wine Quality Dataset]
(https://raw2.github.com/vatsan/pandas_via_psql/master/plots/scatter_matrix.png)

Histogram Plot
==============

To get a quick glimpse of the distribution of the data in your columns, a histogram plot of all columns is quite useful.

You could invoke it from your command line like so:

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py hist
```

Here is the output ![Histogram Plots of some features from the Wine Quality Dataset](https://raw2.github.com/vatsan/pandas_via_psql/master/plots/histogram.png)


Box Plot
=========

Box plots are useful in visually getting a feel for the quartile ranges of numerical columns in your dataset. You could invoke it from your command line like so:

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py box
```

Here is the output ![Box Plot of some features from the Wine Quality Dataset](https://raw2.github.com/vatsan/pandas_via_psql/master/plots/boxplot.png)


Time Series Plot
=================

Again, Pandas has an impressive collection of functions for time series analysis but to quickly visualize a time series, you can run the following from your command line:

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select dt, high, low  from sandp_prices where dt > 1998 order by dt;' | python plotter.py tseries
```

Here is the output ![Time Series Plotting of S&P](https://raw2.github.com/vatsan/pandas_via_psql/master/plots/time_series.png)
