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

# R Script to merge all csv in subfolders

initwd <- 'C:/yourWorkingFolder/'
outCsv <- 'zonalStat.csv'

setwd(initwd)

# Get all csv in all subfolders
inCsv <- list.files(recursive=TRUE,pattern='*.csv$')
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