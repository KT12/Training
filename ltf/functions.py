import tensorflow as tf
import numpy as np

def create_samples(n_clusters, n_samples_per_cluster, n_features, embiggen_factor, seed):
    # n_clusters = number of clusters
    # n_samples_per_cluster = number of points clustered around a given centroid
    # n_features = dimension of data to cluster (in this case 2)
    # seed = random number generators seed

    # set seed
    np.random.seed(seed)
    # slices will contain the random points created
    slices = []
    # centroids are the centroids around which the points will be generated
    centroids = []

    # Create samples for each cluster
    for i in range(n_clusters):
        samples = tf.random_normal((n_samples_per_cluster, n_features), mean=0.0,
        stddev=5.0, dtype=tf.float32, seed=seed, name="cluster_{}".format(i))
        # Create centroid randomly
        current_centroid = (np.random.random((1, n_features)) * embiggen_factor) - (embiggen_factor / 2)
        # Add centroid to list of centroids
        centroids.append(current_centroid)
        # Add centroid coordinates to each zero-meaned sample
        samples += current_centroid
        # Add actual points to slices
        slices.append(samples)
    # Create a big 'samples' dataset
    samples = tf.concat(slices, 0, name='samples')
    centroids = tf.concat(centroids, 0, name='centroids')
    return centroids, samples

def plot_clusters(all_samples, centroids, n_samples_per_cluster):
    import matplotlib.pyplot as plt
    # Plot out the different clusters
    # Choose a different color for each cluster
    colour = plt.cm.rainbow(np.linspace(0, 1, len(centroids)))
    for i, centroid in enumerate(centroids):
        # Grab just the samples for the given cluster andplot them out
        # with a new color
        samples = all_samples[i * n_samples_per_cluster:(i+1)*n_samples_per_cluster]
        plt.scatter(samples[:,0], samples[:,1], c=colour[i])
        # Also plot centroid
        plt.plot(centroid[0], centroid[1], markersize=35, marker='x',
        color='k', mew=10)
        plt.plot(centroid[0], centroid[1], markersize=30, marker='x',
        color='m', mew=5)
    plt.show()

def choose_random_centroids(samples, n_clusters):
    # Initialization: select 'n_clusters' number of random points
    # number of rows in n_samples = number of samples
    n_samples = tf.shape(samples)[0]
    # Shuffled index for each sample
    random_indices = tf.random_shuffle(tf.range(0, n_samples))
    begin = [0,]
    size = [n_clusters,]
    size[0] = n_clusters
    # Create fixed number of indices
    # http://stackoverflow.com/questions/39054414/tensorflow-using-tf-slice-to-split-the-input
    centroid_indices = tf.slice(random_indices, begin, size)
    # print(centroid_indices)
    initial_centroids = tf.gather(samples, centroid_indices)
    return initial_centroids

def assign_to_nearest(samples, centroids):
    # https://www.tensorflow.org/api_docs/python/tf/expand_dims
    expanded_vectors = tf.expand_dims(samples, 0)
    expanded_centroids = tf.expand_dims(centroids, 1)
    distances = tf.reduce_sum(tf.square(tf.subtract(expanded_vectors, expanded_centroids)), 2)
    mins = tf.argmin(distances, 0)

    nearest_indices = mins
    return nearest_indices

def update_centroids(samples, nearest_indices, n_clusters):
    nearest_indices = tf.to_int32(nearest_indices)
    # https://www.tensorflow.org/api_docs/python/tf/dynamic_partition
    partitions = tf.dynamic_partition(samples, nearest_indices, n_clusters)
    new_centroids = tf.concat([tf.expand_dims(tf.reduce_mean(partition, 0), 0)
        for partition in partitions], 0)
    return new_centroids