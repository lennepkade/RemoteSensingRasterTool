##Raster=group
##Mask from NDCI=name
##raster=raster
##thresold=number 0.45
##mask=output raster

outputs_GDALOGRRASTERCALCULATOR_1=processing.runalg('gdalogr:rastercalculator', raster,'1',None,'1',None,'1',None,'1',None,'1',None,'1','numpy.where(A<='+str(thresold)+',0,1)',-1,0,None,mask)