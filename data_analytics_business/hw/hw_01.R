install.packages(“Ecdat”)

library(Ecdat)

data(cars)


model = lm(dist~.,data=cars)

round(cor(cars$speed,cars$dist),3)

cars = mutate(cars, dist_meters = dist*0.3048, speed_mps=speed*0.44704)

model = lm(dist_meters~speed_mps, data=cars)

summary(model)



library(car)