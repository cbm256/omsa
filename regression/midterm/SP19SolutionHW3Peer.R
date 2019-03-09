# read data
data = read.csv('sleep.csv',header=TRUE) #, sep = ',')
head(data)

#Response Variables 
NonDreaming <- data$NonDreaming
Dreaming <- data$Dreaming
TotalSleep <- data$TotalSleep #(for this assignment, we will not use TotalSleep)

#Continuous Variables
BodyWt <- data$BodyWt
BrainWt <- data$BrainWt
LifeSpan <- data$LifeSpan
Gestation <- data$Gestation

#Categorical Variables
Predation <- data$Predation
Exposure <- data$Exposure
Danger <- data$Danger


# Question 1 
# 1a. Scatterplots - check the linearity of of the predicting continuous variables
pairs(data) #or plot(data)

# 1b. Calculate and interpret the correlation coefficients for continuous variables
NonDreamingcor <- cor(data[c(2,3,7,8)],data[4]) 
NonDreamingcor


#Using the scatterplots, are you able to visually validate the direction and strength of the 
#correlation? If you see clusters of data points, try adding a directional line (abline) to the 
#scatterplot by individually inspect each predicting variable. You may need to transform the 
#predicting continuous variable(s) to improve the linearity of the data.

# 1c Visually inspect continuous predicting variables. Include final plots for each variable 
#in your report. 

#Inspect BodyWt
plot(BodyWt, NonDreaming) 
abline(lm(NonDreaming ~ BodyWt, data = data))

# Transform BodyWt
plot(log(BodyWt), NonDreaming)
abline(lm(NonDreaming ~ log(BodyWt), data = data))

# Inspect and Transform BrainWt
plot(BrainWt, NonDreaming)
abline(lm(NonDreaming ~ BrainWt, data = data))
plot(log(BrainWt), NonDreaming)
abline(lm(NonDreaming ~ log(BrainWt), data = data))

# Inspect and Transform LifeSpan
plot(LifeSpan, NonDreaming)
abline(lm(NonDreaming ~ LifeSpan, data = data))
plot(log(LifeSpan), NonDreaming)
abline(lm(NonDreaming ~ log(LifeSpan), data = data))

# Inspect and Transform Gestation
plot(Gestation, NonDreaming)
abline(lm(NonDreaming ~ Gestation, data = data))
plot(log(Gestation), NonDreaming)
abline(lm(NonDreaming ~ log(Gestation), data = data))


#1d - Create and interpret Box plots for predicting categorical variables (1 through 5 or lowest to highest)
boxplot(NonDreaming ~ Predation, xlab = "Predation", ylab = "NonDreamy Sleep")
boxplot(NonDreaming ~ Exposure, xlab = "Exposure", ylab = "NonDreamy Sleep")
boxplot(NonDreaming ~ Danger, xlab = "Total Danger", ylab = "NonDreamy Sleep")

#1e -Based on this section for exploratory analysis, is it reasonable to assume a linear regression 
#model? Would you suggest that NonDreaming varies with all or only some of the independent variables? 
#Would you recommend using the categorical variables Predation, Exposure, and Dangerin the model? Why?


#Question 2 

#Repeat #1a, 1b, 1c, 1d, and 1e excercises for the response variable Dreaming. Label your answers 2a, 2b, 2c, 2d, 2e.

# Question 2 
# 2a. Scatterplots - check the linearity of of the predicting continuous variables
pairs(data) #or plot(data)

# 2b. Calculate and interpret the correlation coefficients for continuous variables

Dreamingcor <- cor(data[c(2,3,7,8)], data[5]) 
Dreamingcor

#Using the scatterplots, are you able to visually validate the direction and strength of the 
#correlation? If you see clusters of data points, try adding a directional line (abline) to the 
#scatterplot by individually inspect each predicting variable. You may need to transform the 
#predicting continuous variable(s) to improve the linearity of the data.

#Inspect BodyWt

plot(BodyWt, Dreaming) 
abline(lm(Dreaming ~ BodyWt, data = data))

# Transform BodyWt
plot(log(BodyWt), Dreaming)
abline(lm(Dreaming ~ log(BodyWt), data = data))

# Inspect and Transform BrainWt
plot(BrainWt, Dreaming)
abline(lm(Dreaming ~ BrainWt, data = data))
plot(log(BrainWt), Dreaming)
abline(lm(Dreaming ~ log(BrainWt), data = data))

# Inspect and Transform LifeSpan
plot(LifeSpan, Dreaming)
abline(lm(Dreaming ~ LifeSpan, data = data))
plot(log(LifeSpan), Dreaming)
abline(lm(Dreaming ~ log(LifeSpan), data = data))

# Inspect and Transform Gestation
plot(Gestation, Dreaming)
abline(lm(Dreaming ~ Gestation, data = data))
plot(log(Gestation), Dreaming)
abline(lm(Dreaming ~ log(Gestation), data = data))


#2d - Create and interpret Box plots for predicting categorical variables (1 through 5 or lowest to highest)
par(mfrow = c(2, 2), pty = "s") 
boxplot(Dreaming ~ Predation, xlab = "Predation", ylab = "Dreamy Sleep")
boxplot(Dreaming ~ Exposure, xlab = "Exposure", ylab = "Dreamy Sleep")
boxplot(Dreaming ~ Danger, xlab = "Total Danger", ylab = "Dreamy Sleep")


#Question 3: Fitting the Linear Regression Model
# 3. Plot full model for NonDreaming without transforming predicting variables. Remember 
#to exclude the remaining response variables for sleep and the Species column.

#1. What are the model parameters and what are their estimates?
#2. What is the equation for the regression line?
#3. Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4. Interpret the estimated value of the parameters, including the error term, corresponding 
#to BodyWt and Predation in the context of the problem. 
#5 Check the assumptions of the model through plotting. Note potential outliers, if any.

model3 <- lm(NonDreaming ~. -Species -Dreaming -TotalSleep, data = data)
summary(model3)
par(mfrow = c(2, 2), pty = "s") 
plot(model3, cook.levels = c(4/42,0.5,1))



#3a. Change model3 to log transform the response variable, NonDreaming.
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to BodyWt and Predation in the context of the problem.
#5 Did model3a improve over model3a? Explain how you determined if the model improved or not.

model3a <- lm(log(NonDreaming) ~ BodyWt +BrainWt +LifeSpan +Gestation +Exposure +Predation +Danger, data = data)
summary(model3a)
par(mfrow = c(2, 2), pty = "s") 
plot(model3a)


#3b. Change model3a to remove the log transform of NonDreaming, and add the
#log transformation to BrainWt, BodyWt, LifeSpan and Gestation.
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Predation in the context of the problem.
#5 Did model3b improve over model3a? Explain how you determined if the model improved or not.
 
model3b <- lm(NonDreaming ~ log(BodyWt) +log(BrainWt) +log(LifeSpan) +log(Gestation) +Exposure +Predation +Danger, data = data)
summary(model3b)
par(mfrow = c(2, 2), pty = "s")
plot(model3b)



#3c. Because the Danger variable is an interpolation of the Exposure and Predation 
#variables, lets remove them from the model, using model3b as your baseline.
  
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Danger in the context of the problem
#5 Did model3c improve over model3b? Explain how you determined if the model improved or not.

model3c <- lm(NonDreaming ~ log(BodyWt) +log(BrainWt) +log(LifeSpan) +log(Gestation) +Danger, data = data)
summary(model3c)
par(mfrow = c(2, 2), pty = "s")
plot(model3c)

#Compare model3c with model3b
anova(model3b, model3c)

#3d  For our final model, let's attempt to improve the data assumptions and model predictability by adding
#back the transformation of the response variable, NonDreaming. Using model3c as your baseline.
  
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Danger in the context of the problem. 
#5 Did finalmodel improve over model3c? Explain how you determined if the model improved or not.

finalmodel3 <- lm(log(NonDreaming) ~ log(BodyWt) + log(BrainWt) + log(LifeSpan) + log(Gestation) + Danger, data = data)
summary(finalmodel3)
par(mfrow = c(2, 2), pty = "s")
plot(finalmodel3)


#4, 4a, 4b, 4c, 4d - Repeat the same process as #3, 3a, 3b, 3c, 3d with the response variable Dreaming.
#Important!  Because row 11 (for species Echidna) has a zero value for Dreaming, lets remove
#that row of data prior to running Question 4, and rename our data variable data2.


#R-Code #remove row 11 
data2 = data[-11,] #use data2 as variable for Q4 and Q6

#Question 4: Fitting the Linear Regression Model
# 4. Plot full model for Dreaming without transforming predicting variables. Remember 
#to exclude the remaining response variables for sleep and the Species column.

#1. What are the model parameters and what are their estimates?
#2. What is the equation for the regression line?
#3. Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4. Interpret the estimated value of the parameters, including the error term, corresponding 
#to BodyWt and Predation in the context of the problem. 
#5 Check the assumptions of the model through plotting. Note potential outliers, if any.

model4 <- lm(Dreaming ~. -Species -NonDreaming -TotalSleep, data = data2)
summary(model4)
par(mfrow = c(2, 2), pty = "s") 
plot(model4, cook.levels = c(4/41,0.5,1))



#4a. Change model4 to log transform the response variable, Dreaming.
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to BodyWt and Predation in the context of the problem.
#5 Did model4a improve over model4a? Explain how you determined if the model improved or not.

model4a <- lm(log(Dreaming) ~ BodyWt +BrainWt +LifeSpan +Gestation +Exposure +Predation +Danger, data = data2)
summary(model4a)
par(mfrow = c(2, 2), pty = "s") 
plot(model4a)


#4b. Change model4a to remove the log transform of Dreaming, and add the
#log transformation to BrainWt, BodyWt, LifeSpan and Gestation.
#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Predation in the context of the problem.
#5 Did model4b improve over model4a? Explain how you determined if the model improved or not.

model4b <- lm(Dreaming ~ log(BodyWt) +log(BrainWt) +log(LifeSpan) +log(Gestation) +Exposure +Predation +Danger, data = data2)
summary(model4b)
par(mfrow = c(2, 2), pty = "s")
plot(model4b)



#4c. Because the Danger variable is an interpolation of the Exposure and Predation 
#variables, lets remove them from the model, using model4b as your baseline.

#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Danger in the context of the problem
#5 Did model4c improve over model4b? Explain how you determined if the model improved or not.

model4c <- lm(Dreaming ~ log(BodyWt) +log(BrainWt) +log(LifeSpan) +log(Gestation) +Danger, data = data2)
summary(model4c)
par(mfrow = c(2, 2), pty = "s")
plot(model4c)

#Compare model4c with model4b
anova(model4b, model4c)

#4d  For our final model, let's attempt to improve the data assumptions and model predictability by adding
#back the transformation of the response variable, Dreaming. Using model4c as your baseline.

#1  What are the model parameters and what are their estimates?
#2 What is the equation for the regression line?
#3 Which predicting variable(s) are significant at alpha = 0.05? What are their p-values? 
#4 Interpret the estimated value of the parameters, including the error term, corresponding 
#to log(BodyWt) and Danger in the context of the problem. 
#5 Did finalmodel improve over model4c? Explain how you determined if the model improved or not.

finalmodel4 <- lm(log(Dreaming) ~ log(BodyWt) + log(BrainWt) + log(LifeSpan) + log(Gestation) + Danger, data = data2)
summary(finalmodel4)
par(mfrow = c(2, 2), pty = "s")
plot(finalmodel4)


# Question 5 - Checking the Assumptions of the Model
#Plot the relevant residual plots to check the final model assumptions. (Linearity does not need to be analyzed as
#this was addressed in the first section of the assignment). Enumerate the assumptions and describe
#what graphical techniques you used. Interpret the displays with respect to the assumptions of the linear regression
#model. Be sure to include the analysis of outliers. Comment on any apparent departures from 
#the assumptions of the linear regression model)

plot(finalmodel3, cook.levels = c(4/42,0.5,1))


#Question 6 - Repeat question 5 using the models produced in Question 4 (using the Dreaming response).
#Be sure you have followed the instructions under Question 4 regarding removing a row of data, changing
#the variable for data to data2 and replacing the NonDreaming response variable with Dreaming.

plot(finalmodel4, cook.levels = c(4/41,0.5,1))
