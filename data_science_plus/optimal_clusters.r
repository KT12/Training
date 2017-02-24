# Tutorial from https://datascienceplus.com/finding-optimal-number-of-clusters/

# Import library `readr``
library('readr')

# Set correct directory
setwd("/home/ktt/Training/data_science_plus/")

# Load data from 'data.csv' (space delimited)
StudentKnowledgeData <- read_delim('data.csv', delim=' ')

# View data
View(StudentKnowledgeData)

# Can also check data using `head`
head(df)

# Pre processing
mydata <- StudentKnowledgeData

# Transform any categorical var
mydata <- as.data.frame(unclass(mydata))

# Remove any NA's
mydataclean <- na.omit(mydata)

# Check data again
summary(mydataclean)
dim(mydataclean)

# Scale and de-mean data
scaled_data = as.matrix((scale(mydataclean)))

# Try to cluster with k=3 means
# nstart attempts multiple initial configurations
kmm = kmeans(scaled_data, 3, nstart = 50,iter.max = 15)

kmm

# (between_SS / total_SS =  29.3 %) is low
# A measure of internal cohesion, external separation
# Want to try to increase without overfitting

# Elbow method to find optimal cluster numbers
set.seed(123)

# Compute and plot for k=2 to k=15
k.max <- 15
data <- scaled_data
wss <- sapply(1:k.max, function(k){kmeans(data, k, nstart=50, iter.max=15)$tot.withinss})

wss

# Plot k vs within cluster SS
plot(1:k.max, wss, type='b', pch=19, frame=FALSE,
     xlab='Num of clusters',
     ylab='Total within cluster SS')

# Not clear what is the best choice for k

# Use Bayesian Info Criterion
library(mclust)
d_clust <- Mclust(as.matrix(scaled_data), G=1:15,
                  modelNames = mclust.options('emModelNames'))
d_clust$BIC
plot(d_clust)

library(NbClust)
nb <- NbClust(scaled_data, diss = NULL, distance='euclidean',
              min.nc = 2, max.nc = 5, method = 'kmeans',
              index = 'all', alphaBeale = 0.1)
hist(nb$Best.nc[1,], breaks = max(na.omit(nb$Best.nc[1,])))