import numpy as np
import rasterio
from matplotlib import pyplot

from osgeo import gdal
import matplotlib.pyplot as plt
from rasterio.plot import (show, show_hist, get_plt,
                           plotting_extent, adjust_band)
from scipy.signal import argrelextrema, savgol_filter
from PyNomaly import loop
import numpy.ma as ma

tifPath1 = "d:\\data\\3010\\2_2.tif"


datasat = gdal.Open(tifPath1)

histogram1 = datasat.GetRasterBand(1).GetHistogram()
histogram2 = datasat.GetRasterBand(2).GetHistogram()
histogram3 = datasat.GetRasterBand(3).GetHistogram()


data = argrelextrema(np.array(histogram1), np.greater)
data2 = savgol_filter(np.array(histogram1), 99, 1)

m = loop.LocalOutlierProbability(histogram1, n_neighbors=3).fit()

scores = m.local_outlier_probabilities

mask = np.where(scores > 0.7, True, False)

maskhistogram = ma.MaskedArray(data=histogram1, mask=mask)

print(maskhistogram)

x = np.linspace(1, 100, len(histogram1))

plt.plot(x, histogram1, ls="-", lw=1, label="1")
#plt.plot(x, data2, ls="-", lw=1, label="2")
plt.plot(x, maskhistogram, ls="-", lw=1, label="3")
plt.legend()

plt.show()
