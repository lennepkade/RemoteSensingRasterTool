#  _____                                                      _            
# |  __ \                                                    (_)           
# | |__) |_ _ _ __ ___    __ _ _ __ ___   __ _ _______  _ __  _  ___ _ __  
# |  ___/ _` | '__/ __|  / _` | '_ ` _ \ / _` |_  / _ \| '_ \| |/ _ \ '_ \ 
# | |  | (_| | | | (__  | (_| | | | | | | (_| |/ / (_) | | | | |  __/ | | |
# |_|  _\__,_|_| _\___|  \__,_|_| |_| |_|\__,_/___\___/|_| |_|_|\___|_| |_|
#     | |       / ____|                                                    
#   __| | ___  | |  __ _   _ _   _  __ _ _ __   ___                        
#  / _` |/ _ \ | | |_ | | | | | | |/ _` | '_ \ / _ \                       
# | (_| |  __/ | |__| | |_| | |_| | (_| | | | |  __/                       
#  \__,_|\___|  \_____|\__,_|\__, |\__,_|_| |_|\___|                       
#                             __/ |                              
#                             \__/
#
# Script to creat a mask from NDCI (or the file you want)
# Choice a thresold number (default 0.45), and every pixel below this number will be set to 0, upper to 0.45 set to 1


##Raster=group
##Mask from NDCI=name
##raster=raster
##thresold=number 0.45
##mask=output raster

outputs_GDALOGRRASTERCALCULATOR_1=processing.runalg('gdalogr:rastercalculator', raster,'1',None,'1',None,'1',None,'1',None,'1',None,'1','numpy.where(A<='+str(thresold)+',0,1)',-1,0,None,mask)