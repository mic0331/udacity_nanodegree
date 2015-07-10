# do not forget to se the working directory to be the directory where the data 
# are located
require(ggplot2)

library(tidyr)# load the data
data = read.csv("stroopdata.csv")
# get column names
colnames(data)
# get basic info about the dataset
summary(data)
# get standard deviations
sd(data$Congruent)
sd(data$Incongruent)
# box plot per column
boxplot(data, use.cols = TRUE)

library(reshape)
d <- melt(data)
ggplot(d,aes(x = value)) + 
  facet_wrap(~variable,scales = "free_x") + 
  geom_histogram()

hist(data$Congruent)
hist(data$Incongruent)

# density curve
ggplot(d, aes(value, fill = variable)) + geom_density(alpha = 0.2)

# density histograms
ggplot(d, aes(value, fill = variable)) + geom_histogram(alpha = 0.5, aes(y = ..density..), position = 'identity')

#draw qqplots
qqnorm(data$Congruent); qqline(data$Congruent)
qqnorm(data$Incongruent); qqline(data$Incongruent)

# remove the outliers from the dataset
remove_outliers <- function(x, na.rm = TRUE, ...) {
  qnt <- quantile(x, probs=c(.25, .75), na.rm = na.rm, ...)
  H <- 1.5 * IQR(x, na.rm = na.rm)
  y <- x
  y[x < (qnt[1] - H)] <- NA
  y[x > (qnt[2] + H)] <- NA
  y
}

# blacklist the outliers
data$Congruent <- remove_outliers(data$Congruent)
data$Incongruent <- remove_outliers(data$Incongruent)

# independent 2-group t-test
t.test(data$Congruent, data$Incongruent)

