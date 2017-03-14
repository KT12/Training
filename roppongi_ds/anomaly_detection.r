# Anomaly detection
# Examples based on the following blog:
# http://tjo.hatenablog.com/entry/2017/01/11/190000
# Which was based on the following book:
# https://www.amazon.co.jp/%E5%85%A5%E9%96%80-%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%81%AB%E3%82%88%E3%82%8B%E7%95%B0%E5%B8%B8%E6%A4%9C%E7%9F%A5%E2%80%95R%E3%81%AB%E3%82%88%E3%82%8B%E5%AE%9F%E8%B7%B5%E3%82%AC%E3%82%A4%E3%83%89-%E4%BA%95%E6%89%8B-%E5%89%9B/dp/4339024910

d <- read.csv('watertreatment_mod.csv')

d.dist <- dist(d[,-1])

d.hcl <- hclust(d.dist, method='ward.D2')

plot(d.hcl, labels=d[,1])

# Try k-means for 4 to 10 clusters

for (i in 4:10){
  km <- kmeans(d[,-1], centers = i)
  print(table(km$cluster))
}

# Investigate the cluster of only 3 datapoints for k > 7
for (i in 8:10){
  km <- kmeans(d[,-1], centers = i)
  cls <- which(table(km$cluster)==3)
  print(d$date[km$cluster==cls])
}

# Seems the 3 same dates have anomalies

###################

# Part 2
# http://tjo.hatenablog.com/entry/2017/02/08/190000

# Anomaly detection for 1-D case under normal distribution

# Create data

set.seed(1)
x1 <- rnorm(300) # White noise
x2 <- rep(c(15, rep(0,49)),6) # Create data spikes
x3 <- c(rep(0,150),rep(3,150)) # Step data

x <- x1 + x2 + x3
y <- x+c(rep(0,130),30,rep(0,169)) # Add anomaly of size 30 at 131st element

# Line plot
plot(y, type = 'l')

# point plot
plot(y)

mu <- mean(y)
s2 <- mean((y - mu)^2)
mu
s2

a <- (y - mu)^2 / s2
thr <- qchisq(0.99, 1) # Deviation from 99% threshold of Chi Sq distro

plot(a)
segments(0, thr, 300, thr, col='red', lty = 3, lwd = 3) # draw lines

# Note how the spike at 30 is looks even more like an anomaly when graphed using Chi Sq

# Hotelling T2

# Normally distrbuted variables in 3D
set.seed(1)
x <- rnorm(n = 500, mean = 1, sd = 1)
set.seed(2)
y <- rnorm(n = 500, mean = 1, sd = 1)
set.seed(3)
z <- rnorm(n = 500, mean = 1, sd = 1)
d <- data.frame(x = x, y = y, z = z)

# Add 3 anomalies
set.seed(4)
idx <- sample(nrow(d), 3)
d[idx,] <- d[idx,] + 10

install.packages('scatterplot3d')
library(scatterplot3d)
scatterplot3d(d, pch=19, cex.symbols=0.5)

# Calculate Hotelling's T^2
X <- as.matrix(d)
mx <- colMeans(X)
Xc <- as.matrix(X) - matrix(1, nrow(X), 1) %*% mx
Sx <- t(Xc) %*% Xc / nrow(X)
am <- rowSums((Xc %*% solve(Sx)) * Xc)
thr <- qchisq(0.99, 1)
plot(am)
segments(0, thr, 500, thr, col='red', lty=3, lwd=3)

# Plot the anomalies in red
idx_a <- which(am > thr)
col_3d <- rep(1, 500)
col_3d[idx_a] <- 2
cex_3d <- rep(0.5, 500)
cex_3d[idx_a] <- 2
scatterplot3d(d, pch=19, cex.symbols = cex_3d, color=col_3d)

# Mahalanobis-Taguchi Method
# http://tjo.hatenablog.com/entry/2017/02/08/190000

# Make 3D points from normally ditributed random numbers

xt <- rnorm(n = 500, mean = 1, sd = 1)
yt <- rnorm(n = 500, mean = 1, sd = 1)
zt <- rnorm(n = 500, mean = 1, sd = 1)
dt <- data.frame(x = xt, y = yt, z = zt)

# Insert 3 deviations in the z direction
idxt <- sample(nrow(dt), 3)
dt[idxt,3] <- dt[idxt,3] + 20
scatterplot3d(dt, pch=19, cex.symbols = 0.5)

# Find anomalies using Hotelling T^2 and Mahalanobis-Taguchi
Xt <- as.matrix(dt)
mxt <- colMeans(Xt)
Xct <- as.matrix(Xt) - matrix(1, nrow(Xt), 1) %*% mxt
Sxt <- t(Xct) %*% Xct / nrow(Xt)
amt <- rowSums((Xct %*% solve(Sxt)) * Xct) / ncol(Xt)
thrt <- 1
plot(amt)
segments(0, thrt, 500, thrt, col = 'red', lty=3, lwd=3)

# Plot the anomalies as red points
idx_at <- which(amt > thrt)
col_3dt <- rep(1, 500)
col_3dt[idx_at] <- 2
cex_3dt <- rep(0.5, 500)
cex_3dt[idx_at] <- 2
scatterplot3d(dt, pch=19, cex.symbols = cex_3dt, color=col_3dt)

# Plot signal/noise ratio

par(mfrow=c(2,2))

for (i in 1:3){
  xc_prime <- Xct[idxt[i],]
  SN1 <- 10*log10(xc_prime^2 / diag(Sxt))
  barplot(SN1)
}