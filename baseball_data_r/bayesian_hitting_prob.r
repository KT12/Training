# https://baseballwithr.wordpress.com/2017/02/20/bayesian-learning-about-a-hitting-probability/

library('TeachBayes')

# Construct df of plausible hitting probabilities

bayes_df <- data.frame(P = seq(0.2, 0.34, by=0.01),
                       Prior=rep(1/15, 15))

# Player hits 100 times, getting 30 hits
# Add column with likelihood of this outcome,
# as a function of the hitting P

bayes_df$Likelihood <- dbinom(30, size=100, prob=bayes_df$P)

# Use bayesian_crank() function to compute posteriors
bayes_df <- bayesian_crank(bayes_df)

# Plot priors and posteriors
prior_post_plot(bayes_df)

# Use discint to find prob interval for P

discint(select(bayes_df, P, Posterior), 0.6)

# Investigate Joey Votto's 2016 batting probability

normal_prior <- normal.select(list(p=.5, x=.320), list(p=.1, x=.280))

normal_prior

normal_draw(c(0.320, 0.031))

# Votto hit .326 in 556 AB's
# SE = sqrt(.326 * (1 - .326) / 556) = 0.0199

normal_update(normal_prior, c(0.326, 0.0199))

many_normal_plots(list(c(0.32, 0.0312), c(0.324, 0.0168)))

qnorm(c(0.05, 0.95), mean=.324, sd=0.0168)