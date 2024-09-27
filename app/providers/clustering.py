import random


class Clustering:

    def _initialize_centroids(self,data, k):
        return random.sample(data, k)

    def _assign_clusters(self, data, centroids):
        clusters = []
        for point in data:
            distances = [abs(point - centroid) for centroid in centroids]
            clusters.append(distances.index(min(distances)))
        return clusters

    def _recalculate_centroids(self, data, clusters, k):
        new_centroids = []
        for i in range(k):
            cluster_points = [data[j] for j in range(len(data)) if clusters[j] == i]
            if cluster_points:
                new_centroids.append(sum(cluster_points) / len(cluster_points))
            else:
                new_centroids.append(random.choice(data))
        return new_centroids

    def _get_clustered_values(self, data, clusters, k):
        clustered_values = [[] for _ in range(k)]
        for i, point in enumerate(data):
            clustered_values[clusters[i]].append(point)
        return clustered_values

    def kmeans(self, data, k, max_iterations=100):
        if len(data) > 1:
            centroids = self._initialize_centroids(data, k)
            for _ in range(max_iterations):
                clusters = self._assign_clusters(data, centroids)
                new_centroids = self._recalculate_centroids(data, clusters, k)
                if new_centroids == centroids:
                    break
                centroids = new_centroids
            clustered_values = self._get_clustered_values(data, clusters, k)


            # Sort clusters based on their minimum value
            clustered_values.sort(key=lambda cluster: (cluster[0] if cluster else float('inf')))

            return clustered_values
        else:
            return [data]