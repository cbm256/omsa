setwd("/home/jfftilton/gitClones/omsa/data_analytics_business/hw")

eitc = read.csv("eitc.csv", header = TRUE)
eitc$postbill= as.numeric(eitc$year >1993) 
eitc$kids = as.numeric(eitc$children >=1)

a = sapply(subset(eitc, postbill==0 & kids == 0, select = work), mean)
b = sapply(subset(eitc, postbill==0 & kids == 1, select = work), mean)
c =sapply(subset(eitc, postbill==1 & kids == 0, select = work), mean)
d = sapply(subset(eitc, postbill==1 & kids == 1, select = work), mean)

(d-c)-(b-a)

nba = read.csv("nba2017.csv", header = TRUE)

model_1 = lm(Salary ~ Ht + Exp, data = nba)
summary(model_1)

model_2 = lm(log(Salary)~Ht+Exp, data=nba)
summary(model_2)