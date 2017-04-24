import tensorflow as tf
import numpy as np

from functions import *

n_features = 2
n_clusters = 3
n_samples_per_cluster = 500
seed = 700
embiggen_factor = 70

np.random.seed()

data_centroids, samples = create_samples(n_clusters, n_samples_per_cluster, n_features,
    embiggen_factor, seed)
initial_centroids = choose_random_centroids(samples, n_clusters)
nearest_indices = assign_to_nearest(samples, initial_centroids)
updated_centroids = update_centroids(samples, nearest_indices, n_clusters)

model = tf.global_variables_initializer()
with tf.Session() as session:
    sample_values = session.run(samples)
    #plot_clusters(sample_values, initial_centroids, n_samples_per_cluster)
    for i in range(1024):
        updated_centroid_value = session.run(updated_centroids)
        if i%128 == 0:
            print(nearest_indices)
            plot_to_nearest(sample_values, updated_centroid_value, nearest_indices)
