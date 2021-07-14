library(readr)
library(tidyverse)
library(ggplot2)
library(readxl)
library(stats)
library(DescTools)
library(sandwich)
library(lmtest)
library(multiwayvcov)
library(metafor)
library(bayesm)
library(puniform)
library(haven)
library(meta)
library(AER)
library(BMS)
library(corrplot)
library(foreign)
library(xtable)
library(LowRankQP)
library(foreign)
library(multcomp)
library(qdap)


#Reading the data

data <- read_xlsx("Model data All vs. All.xlsx")
#View(data)

model_data <- data[,6:dim(data)[2]]
colnames(model_data) <- gsub(",", "",colnames(model_data))
colnames(model_data) <- gsub(":", "",colnames(model_data))
colnames(model_data) <- gsub("!", "",colnames(model_data))
colnames(model_data) <- gsub("-", "_",colnames(model_data))
colnames(model_data) <- gsub("'", "_",colnames(model_data))
colnames(model_data) <- gsub(" ", "_",colnames(model_data))
colnames(model_data) <- gsub("\\(", "",colnames(model_data))
colnames(model_data) <- gsub("\\)", "",colnames(model_data))


formula <- paste(colnames(model_data)[1],paste(colnames(model_data)[-1],sep="", collapse = "+"), sep="~",collapse = NULL)
formula <- as.formula(gsub("+C_Thun_the_Shattered+","+",formula))
reg_test <- lm(formula = formula, data = model_data)
car::vif(reg_test) #VIF coefficients


BMA1 = bms(reg_test, burn=1e4,iter=1e5, g="UIP", mprior="uniform", nmodel=20000,mcmc="bd", user.int =FALSE)
print(BMA1)

#Extracting the coefficients and plotting the results
coef(BMA1,order.by.pip= F, exact=T, include.constant=T)
image(BMA1, yprop2pip=FALSE,order.by.pip=TRUE, do.par=TRUE, do.grid=TRUE, do.axis=TRUE, xlab = "", main = "") #takes time, beware

summary(BMA1)
plot(BMA1)
print(BMA1$topmod[1])





