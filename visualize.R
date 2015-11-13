library(rgl)
train <- read.table("trainTable.txt")
open3d()
plot3d(train$V2,train$V3,train$V4, col=as.numeric(  train$V1))
test <- read.table("testTable.txt")
open3d()
plot3d(test$V2,test$V3,test$V4, col=as.numeric(  test$V1))

readline(prompt="Press <return to continue") 
