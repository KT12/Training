import tensorflow as tf
import numpy as np

from functions import create_samples, choose_random_centroids, plot_clusters

n_features = 2
n_clusters = 3
n_samples_per_cluster = 500
seed = 700
embiggen_factor = 70

np.random.seed()

centroids, samples = create_samples(n_clusters, n_samples_per_cluster, n_features,
    embiggen_factor, seed)
initial_centroids = choose_random_centroids(samples, n_clusters)

model = tf.global_variables_initializer()
with tf.Session() as session:
    sample_values = session.run(samples)
    centroid_values = session.run(centroids)

plot_clusters(sample_values, centroid_values, n_samples_per_cluster)