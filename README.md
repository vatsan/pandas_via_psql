Usage:
=======
Invoke Pandas plotting functions by piping in the output from a psql query.
You can re-use this boiler-plate code for Scatter Plots, Box Plots, Histograms and Time Series Plots on your tables.

Datasets Used
==============

For this demo, I'm using two publicly available datasets. 
* [The UCI wine quality dataset](http://archive.ics.uci.edu/ml/datasets/Wine+Quality).
* [The S&P daily prices dataset]().


Scatter Matrix
===============

This is pretty useful when you are interested in analyzing the correlation between a bunch of features in a dataset, particularly in their correlation with the target attribute/label. You might then perform feature selection based on a visual output of the correlations.

Here is how the scatter matrix can be created on the UCI Wine Quality Dataset

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select * from wine;' | python plotter.py scatter
```

Here is the output [Scatter Matrix of all features from the Wine Quality Dataset]
(https://github.com/vatsan/pandas_via_psql/blob/master/plots/scatter_matrix.png)

Histogram Plot
==============


```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py hist
```

Here is the output [Histogram Plots of some features from the Wine Quality Dataset](https://github.com/vatsan/pandas_via_psql/blob/master/plots/histogram.png)


Box Plot
=========


```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py box
```

Here is the output [Box Plot of some features from the Wine Quality Dataset](https://github.com/vatsan/pandas_via_psql/blob/master/plots/boxplot.png)


Time Series Plot
=================

```
home$ psql -d vatsandb -h dca -U gpadmin -c 'select dt, high, low  from sandp_prices where dt > 1998 order by dt;' | python plotter.py tseries
```

Here is the output [Time Series Plotting of S&P](https://github.com/vatsan/pandas_via_psql/blob/master/plots/time_series.png)
