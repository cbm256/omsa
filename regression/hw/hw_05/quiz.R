setwd("~/gitClones/omsa/regression/hw/hw_05")

data = read.csv("GA_EDVisits.csv",header=TRUE) 
data = na.omit(data)

# Get names of the column 
names = colnames(data) 
attach(data)

## standardized predictors - use these variables in your modeling in addition to the predictors A5.9, A10.14
sAvgDistS = scale(log(SpecDist)) 
sAvgDistP = scale(log(PedDist))
sMedianIncome = scale(MedianIncome) 
sNumHospitals = scale(No.Hospitals)
sPercentLessHS = scale(PercentLessHS) 
sPercentHS = scale(PercentHS)

model1 = glm(Y ~ sAvgDistS+sAvgDistP+sMedianIncome+sNumHospitals+sPercentLessHS+sPercentHS, family=binomial)

Y = cbind(ED.visits, Asthma_children-ED.visits)

## Define interaction terms
DistA5.9 = sAvgDistS*A5.9 
DistA10.14 = sAvgDistS* A10.14
DistIncome = sAvgDistS*sMedianIncome 
DistLessHS = sAvgDistS*sPercentLessHS
DistHS = sAvgDistS*sPercentHS 
DistPA5.9 = sAvgDistP*A5.9
DistPA10.14 = sAvgDistP* A10.14 
DistPIncome = sAvgDistP*sMedianIncome
DistPLessHS = sAvgDistP*sPercentLessHS 
DistPHS = sAvgDistP*sPercentHS
X = cbind(A5.9, A10.14, sAvgDistS, sAvgDistP, sMedianIncome, sPercentLessHS, sPercentHS, sNumHospitals, DistA5.9, DistA10.14, DistIncome, DistLessHS, DistHS, DistPA5.9, DistPA10.14, DistPIncome, DistPLessHS, DistPHS)

Xnew = cbind(A5.9, A10.14, sAvgDistS, sAvgDistP, sMedianIncome, sPercentLessHS, sPercentHS, sNumHospitals, DistA5.9, DistA10.14, DistIncome, DistLessHS, DistHS, DistPA5.9, DistPA10.14, DistPIncome, DistPLessHS, DistPHS)

colnames(Y) <- cbind("ED.visits", "Asthma_children-ED.visits")
colnames(X) <- cbind("A5.9", "A10.14", "sAvgDistS", "sAvgDistP", "sMedianIncome", "sPercentLessHS", "sPercentHS", "sNumHospitals", "DistA5.9", "DistA10.14", "DistIncome", "DistLessHS", "DistHS", "DistPA5.9", "DistPA10.14", "DistPIncome", "DistPLessHS", "DistPHS")



model2 =  glm(Y ~ X, family=binomial)
summary(model2)


m1 = glm(Y ~ sAvgDistS+sAvgDistP+sMedianIncome+sNumHospitals+sPercentLessHS+sPercentHS, family=binomial)
m2 = glm(Y~ A5.9+A10.14+ sAvgDistS+ sAvgDistP+ sMedianIncome+sPercentLessHS+sPercentHS+sNumHospitals+DistA5.9+DistA10.14+DistIncome+DistLessHS+DistHS+ DistPA5.9+ DistPA10.14+DistPIncome+DistPLessHS+DistPHS, family=binomial)

step(m1, scope = list(lower = m1, upper = m2), direction = "forward")


set.seed(123)
library(glmnet)
model.cv=cv.glmnet(X,Y,family=c("binomial"),alpha=.5,nfolds=5)
model= glmnet(X, Y,family=c("binomial"), alpha = .5, nlambda = 100)
coef(model,s = model.cv$lambda.min)
summary(model)
model
