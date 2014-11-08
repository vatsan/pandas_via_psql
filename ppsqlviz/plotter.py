'''
Pandas Plotting from STDIN.
Srivatsan Ramanujam <vatsan.cs@utexas.edu> 
20 Jan 2014
============================================================================================================================
Usage:
=========
Syntax: python plotter.py <hist|box|scatter|tseries|density|hexbin>
Examples:
=========
1) home$ psql -d vatsandb -h dca -U gpadmin -c 'select * from wine;' | python plotter.py scatter
2) home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py box
3) home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py hist
4) home$ psql -d vatsandb -h dca -U gpadmin -c 'select dt, high, low  from sandp_prices where dt > 1998 order by dt;' | python plotter.py tseries
5) home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids, hue, proline from wine;' | python plotter.py density
6) home$ psql -d vatsandb -h dca -U gpadmin -c 'select ash, flavanoids from wine;' | python plotter.py hexbin
============================================================================================================================
'''

import pandas as pd
from pandas import DataFrame
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from StringIO import StringIO
import numpy as np
import fileinput
import re
import numpy as np

def scatterMatrix(dframe):
    '''
       Show Scatter Matrix
    '''
    df = DataFrame(dframe)
    #Rename columns so that the plot if not very cluttered.
    df.columns = range(len(df.columns))
    smatrix = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()
    
def hexbinPlot(dframe):
    '''
       Show 2-d hexbin plot
    '''
    x_label, y_label=dframe.columns[0],dframe.columns[1]
    x, y = dframe[x_label],dframe[y_label]
    hexbinplt = plt.hexbin(x,y,gridsize=30)
    cbar = plt.colorbar()
    cbar.set_label('count')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    
def boxPlot(dframe):
    '''
       Show Box Plot of various fields
    '''
    box_plot = dframe.boxplot()
    plt.show()
    
def histogramPlot(dframe):
    '''
       Show histogram of various fields
    '''
    if(len(dframe.columns)>1):
        hist_plot = dframe.hist(figsize=(6, 6))
    else:
        hist_plot = dframe.hist()
    plt.show()
    
def timeSeriesPlot(dframe):
    '''
       Show time series plot using pandas. The first column should be a date/time column.
    '''
    #The first column should be a date column and that will used as an index.
    dframe.set_index(dframe.columns[0]).plot()
    plt.show()

def densityPlot(dframe):
    '''
       Show Kernel Density Plots
    '''
    if(len(dframe.columns)>1):
        hist_plot = dframe.plot(kind='kde',linewidth=3, figsize=(6, 6))
    else:
        hist_plot = dframe.plot(kind='kde',linewidth=3)
    plt.show()

def barPlot(dframe):
    '''
       Show Bar Plot. The first column should be the x-coordinates (e.g.,bin centers) and 
       the second column should be the y-coordinates (e.g., counts).
    '''
    x_label, y_label=dframe.columns[0],dframe.columns[1]
    x = dframe.iloc[0][0]
    y = dframe.iloc[0][1]
    x = x.replace('{','')
    x = x.replace('}','')
    y = y.replace('{','')
    y = y.replace('}','')
    x = x.split(',')
    y = y.split(',')
    x = np.array(map(float,x))
    y = np.array(map(float,y))
    width = 0.7* (x[1]-x[0])
    plt.bar(x,y,align='center',width=width)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show() 
    
def imgPlot(dframe):
    '''
       Show Image
    '''
    if(len(dframe.columns)>1):
        r = int(dframe.iloc[0][0])
        c = int(dframe.iloc[0][1])
        patch = dframe.iloc[0][2]
        patch = patch.replace('{','');
        patch = patch.replace('}','');
        str_pixels = patch.split(',');
        pixels = np.array(map(float, str_pixels));
        pixels = pixels.reshape(r,c)
        plt.imshow(pixels,cmap = cm.Greys_r)
    else:
        print 'Usage: for image plot, 3 columns are expected, with the first two columns being the number of rows and number of columns that make up the image and the third column being the actual image pixelsa as a vector'
    plt.show()

def imgRGBPlot(dframe):
    '''
       Show RGB Image
    '''
    if(len(dframe.columns)>1):
        r = int(dframe.iloc[0][0])
        c = int(dframe.iloc[0][1])
        patch = dframe.iloc[0][2]
        patch = patch.replace('{','');
        patch = patch.replace('}','');
        str_pixels = patch.split(',');
        pixels = np.array(map(float, str_pixels));
        im = np.reshape(pixels, (-1,3)) # reshape
        im = np.dstack((np.reshape([np.uint8(float(i)) for i in pixels[0:r*c]], (r,c)),
                np.reshape([np.uint8(float(i)) for i in pixels[r*c:2*r*c]], (r,c)),
                np.reshape([np.uint8(float(i)) for i in pixels[2*r*c:3*r*c]], (r,c))))
        plt.imshow(im)
    else:
        print 'Usage: for image plot, 3 columns are expected, with the first two columns being the number of rows and number of columns that make up the image and the third column being the actual image pixelsa with R,G,& B values listed sequentially	as a vector'
    plt.show()
    
def readTableFromPipe(plot_type):
    '''
       Read the output of a SQL query from a pipe and display a scatter plot
    '''
    rows_pattern = re.compile(r'^\(\d+ rows\)$')
    underline_pattern = re.compile(r'^(-+\+-+)+$')
    single_underline_pattern = re.compile(r'^(-)+$')
    data =[]
    for line in fileinput.input():
        #Skip lines not representing header or data
        if(line.strip() and not rows_pattern.match(line) and not underline_pattern.match(line) and not single_underline_pattern.match(line)):
            data.append(re.sub('\s+','',line))
    dframe = pd.read_csv(StringIO('\n'.join(data)), sep='|', index_col=False)
    if(plot_type=='scatter'):
        scatterMatrix(dframe)
    elif(plot_type=='box'):
        boxPlot(dframe)
    elif(plot_type=='hist'):
        histogramPlot(dframe)
    elif(plot_type=='tseries'):
        timeSeriesPlot(dframe)
    elif(plot_type=='density'):
        densityPlot(dframe)
    elif(plot_type=='hexbin'):
        hexbinPlot(dframe)
    elif(plot_type=='bar'):
        barPlot(dframe)
    elif(plot_type=='image'):
    	imgPlot(dframe)
    elif(plot_type=='imageRGB'):
    	imgRGBPlot(dframe)
        
if(__name__ == '__main__'):
    from sys import argv
    if(len(argv)!=2):
        print 'Usage: python plotter.py <hist|box|scatter|tseries|density|hexbin>'
    else:
        plot_type = argv[1]
        #Remove arguments list from Argv (else fileinput will cry).
        argv.pop()
        readTableFromPipe(plot_type)
