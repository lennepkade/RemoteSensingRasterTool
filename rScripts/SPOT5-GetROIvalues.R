require(sp)
require(raster)
require(maptools)
require(rgeos)
require(gtools)

initwd <- '/home/lennepkade/Bureau/toa'
setwd(initwd)


folders=list.dirs(getwd(),recursive=FALSE)

for (folder in folders){
setwd(folder)
  
# Get all tif from folder
inRaster <- list.files(folder,pattern='*.tif$')

# Order them to have main image first
inRaster <- inRaster[order(nchar(inRaster))]

for(rasterLoop in inRaster){
print(paste('calculating ',rasterLoop))
# get fileName with no extension and/or no indice
fileName <- strsplit(strsplit(rasterLoop, "\\.")[[1]], "\\_")[[1]]
inShape <- paste(fileName[1],'.shp',sep='')

openRaster <- raster(rasterLoop)

avoidImage <- FALSE

# if indice image (type : image_ndvi.tif), take same shp as original image
# fileName[2] is the indice name, or it's NA
if (!is.na(fileName[2])){
  
  # if mask, avoid calc
  if(fileName[2]=='mask'){
    avoidImage <- TRUE
    }
  else{
    indiceImage <-TRUE
  }
  indiceName <- fileName[2]
  
}
else{
  indiceImage <-FALSE
  inShape <- paste(fileName[1],'.shp',sep='')
}

# If same scene but indices, performs stat with same shp
# if shp with samename exist, perform stat
# if shp doesn't exists or avoidImage is TRUE, do not perform stat

if (file.exists(inShape) & avoidImage==FALSE)
  {
  inShape <- readShapePoly(inShape)

csvToWrite <- paste(fileName[1],'.csv',sep='')
if(indiceImage){
  
  mydf=read.csv2(csvToWrite)
}
else{
  mydf <- data.frame(inShape)
  # Save image name in image column
  mydf['imageName'] <- fileName[1]
}

# For each band, write zonal stat
for(i in 1:openRaster@file@nbands){
  openBand <- raster(rasterLoop,band=i)
  if(indiceImage){
   band=indiceName 
  }
  else{
    if(i==1){band='V'}
  else if(i==2){band='R'}
  else if(i==3){band='NIR'}
  else if(i==4){band='MIR'}
  }
  print(paste('calculating',band))
  
  #assign band name with min/max like NIRmin, NIRmax...      
  mydfMin <- paste(band, 'min', sep = "")
  mydfMax <- paste(band, 'max', sep = "")
  
  #fill table
  minB <- extract(openBand,inShape, fun = min)
  maxB <- extract(openBand,inShape, fun = max)
  mydf[mydfMin] <- round(minB,2)
  mydf[mydfMax] <- round(maxB,2)
}

write.csv2(mydf,csvToWrite)

}
else{
  print('No vector with the same name as your main image or image to avoid')
}
}
}

### Merge all CSV 
# Go back to root
setwd(initwd)

# Get all csv in all subfolders
inCsv <- list.files(recursive=TRUE,pattern='*.csv$')
outCsv <- 'zonalStat.csv'
# save it at root with name zonalStat.csv
if(file.exists(outCsv)){
  file.remove(outCsv)
}

# create empty data frame
df<-data.frame()

# loop throught csv and save it in df
for(i in inCsv){
  print(i)
  temp <-read.csv2(i)
  
  #using smartbind from gtools to combine if different column number
  df<-smartbind(df, temp)
  rm(temp)
}

write.csv2(df,outCsv)
