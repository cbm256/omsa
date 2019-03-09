data = read.csv("highway1.csv", header = TRUE, sep = ',')
rate = as.numeric(data[,2])
signs = as.numeric(data[,6])

plot(signs, rate)
cor(signs, rate)

model = lm(formula = rate ~ signs)
summary(model)

confint(model, level=.95)

plot(signs, rate)
plot (fitted(model), resid(model))
qqnorm(resid(model))
qqline(resid(model))

predict(model, data.frame(signs=1.25), interval="prediction")

