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
# R Script to compute OA/Kappa from a confusion matrix file
# Parse all csv files from a folder, then create table with filename, OA, and Kappa

require(sp)
#require(raster)
#require(maptools)
#require(rgeos)
#require(gtools)

initwd <- '/media/Backups/Sauvegarde Nico/stats/RF/'
outputCsv = '../RFstat-3tree.csv'
#classifier <- strsplit(initwd,"\\/")
#classifier <- classifier[[1]][length(classifier[1])]

setwd(initwd)


inCsv <- list.files(path='.',pattern='*.csv$')

if(file.exists(outputCsv)){
  file.remove(outputCsv)
}

mydf <- data.frame('imageName'=character(),'OA'=numeric(),'Kappa'=numeric())

for(i in inCsv){
#readConfu <- readConfu[-c(6,7,8,9),-c(6,7,8,9)]
readConfu <- read.csv2(i,sep=',',header=FALSE)

confuMatrix <- data.matrix(readConfu)

# Compute Overall Acuracy
OA = round(sum(diag(confuMatrix))/sum(confuMatrix),2)

# Compute Cohen Kappa
n = sum(confuMatrix)
nl = rowSums(confuMatrix)
nc = colSums(confuMatrix)

Kappa = round(((n**2)*OA - sum(nc*nl))/(n**2-sum(nc*nl)),2)

# print results
paste('OA :',OA)
paste('Kappa :',OA)

# Save to table
imageName = strsplit(strsplit(i, "\\.")[[1]], "\\_")[[1]][1]

# create line result
result <- data.frame(imageName,OA,Kappa)
mydf <- rbind(mydf, result)
}

if(file.exists(outputCsv)){
file.remove(outputCsv)}

write.csv2(mydf,sep=";",file=outputCsv,row.names=FALSE,dec=",")
