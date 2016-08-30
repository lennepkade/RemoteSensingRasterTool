##Raster=group
##raster=raster
#Blue=number 1
# FOR SPOT 5
Blue=0
Green=1
Red= 2
NIR= 3
MIR= 4


#Import library to QGIS
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import scipy as sp
from scipy import ndimage

from osgeo import gdal
import os

class computeIndices:
    def __init__(self,inRaster,Blue,Green,Red,NIR,MIR):
        '''
        Input raster, bands, and output folder
        Compute indices
        Save in output folder. (originalFileName_NDVI.tif)
        '''
        #
        
        rasterFun=rasterFunction()
        self.rasterFun=rasterFun
#        progress.setText(inRaster)
#        progress.setText(outputFolder)
        data,temp=rasterFun.open_data_band(inRaster,'float32')
        self.proj = data.GetProjection()
        self.geo = data.GetGeoTransform()
        
        #get dir without extension
        self.split=os.path.splitext(inRaster)[0]
        
        # loads bands
        try:
            NIR=data.GetRasterBand(NIR).ReadAsArray().astype(sp.float32)
            Red=data.GetRasterBand(Red).ReadAsArray().astype(sp.float32)
            MIR=data.GetRasterBand(MIR).ReadAsArray().astype(sp.float32)
            #Blue=data.GetRasterBand(Blue).ReadAsArray().astype(sp.float32)
            Green=data.GetRasterBand(Green).ReadAsArray().astype(sp.float32)
                   
            
            #NDVI
            #self.ndvi(temp,Red,NIR)
            
            #TNDVI
            #self.tndvi(temp,Red,NIR)
            
            #ARVI
            #self.arvi(temp,Blue,Red,NIR)
            
            #NDCI
            self.ndci(temp,Red,MIR)
            
            #EVI
            #self.evi(temp,Blue,Red,NIR)
            
            #
            #self.evi2(temp,Red,NIR)
            #NDWI
            #self.ndwi(temp,Red,MIR)

        except:
            print('Problem with '+inRaster)
 
    
        
    def ndci(self,temp,Red,MIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_ndci.tif',temp,1,self.geo,self.proj)
        num=MIR-Red
        den=MIR+Red
        temp[den!=0]=num[den!=0]/den[den!=0]
        temp[den==0]=-1
        self.saveIndice(outFile,temp)        
        
    def evi(self,temp,Blue,Red,NIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_evi.tif',temp,1,self.geo,self.proj)
        num=2.5*((NIR)-(Red))
        den=((NIR)+6.0*(Red)-7.5*(Blue)+1)
        temp[den!=0]=(num[den!=0]/den[den!=0])
        temp[den==0]=-1

        self.saveIndice(outFile,temp)
    
    def evi2(self,temp,Red,NIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_evi2.tif',temp,1,self.geo,self.proj)
        num=2.5*(NIR-Red)
        den=NIR+2.4*Red+1.0
        temp[den!=0]=(num[den!=0]/den[den!=0])
        temp[den==0]=-1

        self.saveIndice(outFile,temp)
        
    def ndwi(self,temp,Red,MIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_ndwi.tif',temp,1,self.geo,self.proj)
        num=Red-MIR
        den=Red+MIR
        temp[den!=0]=num[den!=0]/den[den!=0]
        temp[den==0]=-1
        self.saveIndice(outFile,temp)
        
    def ndvi(self,temp,Red,NIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_ndvi.tif',temp,1,self.geo,self.proj)
        num=NIR-Red
        den=NIR+Red
        temp[den!=0]=num[den!=0]/den[den!=0]
        temp[den==0]=-1
        self.saveIndice(outFile,temp)
            
            
    def tndvi(self,temp,Red,NIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_tndvi.tif',temp,1,self.geo,self.proj)
        num=NIR-Red
        den=NIR+Red
        temp[den!=0]=num[den!=0]/den[den!=0]
        temp[den==0]=-1
        temp=(temp+(1/2))**(0.5)
        self.saveIndice(outFile,temp)
        
    def arvi(self,temp,Blue,Red,NIR):
        outFile=self.rasterFun.create_empty_tiff(self.split+'_arvi.tif',temp,1,self.geo,self.proj)
        num=(NIR-(2.0*Red-Blue))
        den=(NIR+(2.0*Red-Blue))
        temp[den!=0]=num[den!=0]/den[den!=0]
        temp[den==0]=-1
        self.saveIndice(outFile,temp)
        
    def saveIndice(self,outFile,temp):
        out=outFile.GetRasterBand(1)
        out.WriteArray(temp)
        out.FlushCache()

        
        

class rasterFunction:

    def open_data_band(self,filename,dt=None):
        """!@brief The function open and load the image given its name. 
        The function open and load the image given its name. 
        The type of the data is checked from the file and the scipy array is initialized accordingly.
            Input:
                filename: the name of the file
            Output:
                data : the opened data with gdal.Open() method
                im : empty table with right dimension (array)
        
        """
        data = gdal.Open(filename,gdal.GA_ReadOnly)
        if data is None:
            print('Impossible to open '+filename)
            exit()
        nc = data.RasterXSize
        nl = data.RasterYSize
    #    d  = data.RasterCount
        
        # Get the type of the data
        if not dt:
            gdal_dt = data.GetRasterBand(1).DataType
            if gdal_dt == gdal.GDT_Byte:
                dt = 'uint8'
            elif gdal_dt == gdal.GDT_Int16:
                dt = 'int16'
            elif gdal_dt == gdal.GDT_UInt16:
                dt = 'uint16'
            elif gdal_dt == gdal.GDT_Int32:
                dt = 'int32'
            elif gdal_dt == gdal.GDT_UInt32:
                dt = 'uint32'
            elif gdal_dt == gdal.GDT_Float32:
                dt = 'float32'
            elif gdal_dt == gdal.GDT_Float64:
                dt = 'float64'
            elif gdal_dt == gdal.GDT_CInt16 or gdal_dt == gdal.GDT_CInt32 or gdal_dt == gdal.GDT_CFloat32 or gdal_dt == gdal.GDT_CFloat64 :
                dt = 'complex64'
            else:
                print('Data type unkown')
                exit()
        
        # Initialize the array
        im = sp.empty((nl,nc),dtype=dt) 
        return data,im
    
    '''
    Old function that open all the bands
    '''
    #    
    #    for i in range(d):
    #        im[:,:,i]=data.GetRasterBand(i+1).ReadAsArray()
    #    
    #    GeoTransform = data.GetGeoTransform()
    #    Projection = data.GetProjection()
    #    data = None
    
    
    def create_empty_tiff(self,outname,im,d,GeoTransform,Projection,gdal_dt=None):
        '''!@brief Write an empty image on the hard drive.
        
        Input: 
            outname: the name of the file to be written
            im: the image cube
            GeoTransform: the geotransform information 
            Projection: the projection information
        Output:
            Nothing --
        '''
        nl = im.shape[0]
        nc = im.shape[1]
    
        driver = gdal.GetDriverByName('GTiff')
        dt = im.dtype.name
        # Get the data type
        if not gdal_dt:
            if dt == 'bool' or dt == 'uint8':
                gdal_dt=gdal.GDT_Byte
            elif dt == 'int8' or dt == 'int16':
                gdal_dt=gdal.GDT_Int16
            elif dt == 'uint16':
                gdal_dt=gdal.GDT_UInt16
            elif dt == 'int32':
                gdal_dt=gdal.GDT_Int32
            elif dt == 'uint32':
                gdal_dt=gdal.GDT_UInt32
            elif dt == 'int64' or dt == 'uint64' or dt == 'float16' or dt == 'float32':
                gdal_dt=gdal.GDT_Float32
            elif dt == 'float64':
                gdal_dt=gdal.GDT_Float64
            elif dt == 'complex64':
                gdal_dt=gdal.GDT_CFloat64
            else:
                print('Data type non-suported')
                exit()
        
        dst_ds = driver.Create(outname,nc,nl, d, gdal_dt)
        dst_ds.SetGeoTransform(GeoTransform)
        dst_ds.SetProjection(Projection)
        
        return dst_ds



computeIndices(raster,Blue,Green,Red,NIR,MIR)
print('done')
if __name__ == '__main__':
    inRaster="/home/lennepkade/Bureau/datapag/02-Results/02-Data/pansharp_Spot7.tif"
    Blue=1
    Green=2
    Red=3
    NIR=4
    MIR=4
    computeIndices(inRaster,Blue,Green,Red,NIR,MIR)
