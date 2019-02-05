data = read.csv("fram.csv", header=TRUE)
data$SEX <- as.factor(data$SEX)
data$CURSMOKE <- as.factor(data$CURSMOKE)


head(data)

model = lm(SYSBP ~., data)

summary(model)

data3 <- data[data$BMI>=30,]

model2 = lm(SYSBP ~., data3)

summary(model2)