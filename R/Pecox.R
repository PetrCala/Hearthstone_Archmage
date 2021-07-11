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


#Reading the data

data <- read_xlsx("Model data.xlsx")
View(data)

y <- data$'Overall Winrate'
x <- data$'Sample Size'

model <- lm(y ~ x)

