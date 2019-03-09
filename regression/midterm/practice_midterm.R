data = read.csv("abb.csv", header = TRUE, sep = ',')



model1 = lm(price ~ room_type + reviews + overall_satisfaction + accommodates + bedrooms, data= data)

summary(model1)

plot(cooks.distance(model1), type ='h', col='red')
test = data[-94,]
test = test[-94,]
model2 = lm(price ~ room_type + reviews + overall_satisfaction + accommodates + bedrooms, data= test)

predict(model2, data.frame(bedrooms=1,accommodates=2, reviews=92, overall_satisfaction=3.5, room_type="Private room"), interval="prediction")