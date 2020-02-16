__all__ = [
    "get_structural_holes_HAM"
]
import sys
import numpy as np
import json, os
import scipy.sparse as sps
import scipy.linalg as spl
from sklearn import metrics
from scipy.cluster.vq import kmeans, vq, kmeans2
from collections import Counter
eps=2.220446049250313e-16
import scipy.stats as stat

def sym(w):
    return w.dot(spl.inv(spl.sqrtm(w.T.dot(w))))

def avg_entropy(predicted_labels, actual_labels):
    actual_labels_dict = {}
    predicted_labels_dict = {}
    for label in np.unique(actual_labels):
        actual_labels_dict[label] = np.nonzero(actual_labels==label)[0]
    for label in np.unique(predicted_labels):
        predicted_labels_dict[label] = np.nonzero(predicted_labels==label)[0]
    avg_value = 0
    N = len(predicted_labels)
    # store entropy for each community
    for label, items in predicted_labels_dict.items():
        N_i = float(len(items))
        p_i = []
        for label2, items2  in actual_labels_dict.items():
            common = set(items.tolist()).intersection(set(items2.tolist()))
            p_ij = float(len(common))/ N_i
            p_i.append(p_ij)
        entropy_i = stat.entropy(p_i)
        avg_value += entropy_i * (N_i / float(N))
    return avg_value

def load_adj_matrix(G):
    listE = []
    for edge in G.edges:
        listE.append(edge[0]-1)
        listE.append(edge[1]-1)
        # listE.append(edge[0])
        # listE.append(edge[1])
    adj_tuples = np.array(listE).reshape(-1,2)
    n = len(np.unique(adj_tuples))
    vals = np.array([1] * len(G.edges))
    max_id = max(max(adj_tuples[:, 0]), max(adj_tuples[:, 1])) + 1
    # print(vals)
    # print(n)
    # print(adj_tuples)
    # print(max_id)
    A = sps.csr_matrix((vals, (adj_tuples[:, 0], adj_tuples[:, 1])), shape=(max_id, max_id))
    A = A + A.T
    # print(A)
    return sps.csr_matrix(A)

def majority_voting(votes):
    C = Counter(votes)
    pairs = C.most_common(2)
    if len(pairs)==0:
        return 0
    if pairs[0][0] > 0:
        return pairs[0][0]
    elif len(pairs)>1:
        return pairs[1][0]
    else:
        return 0

def label_by_neighbors(AdjMat,labels):
    assert (AdjMat.shape[0] == len(labels)), "dimensions are not equal"
#     print labels
#     print(labels)
    unlabeled_idx = (labels==0)
    num_unlabeled = sum(unlabeled_idx)
    count = 0
    while num_unlabeled > 0:
        # print(num_unlabeled)
        idxs = np.array(np.nonzero(unlabeled_idx)[0])
        # print(idxs)
        next_labels = np.zeros(len(labels))
        for idx in idxs:
            neighbors = np.nonzero(AdjMat[idx,:] > 0)[1]
            # print(neighbors)
            if len(neighbors)==0:
                next_labels[idx] = majority_voting(labels)
            # print(next_labels)
            else :
                neighbor_labels = labels[neighbors]
#               print idx, neighbors, neighbor_labels
                next_labels[idx] = majority_voting(neighbor_labels)
        labels[idxs] = next_labels[idxs]
        unlabeled_idx = (labels==0)
        num_unlabeled = sum(unlabeled_idx)
#         print num_unlabeled
    return labels


def get_structural_holes_HAM(G, k, c,ground_truth_labels):

    A_mat = load_adj_matrix(G)
    A = A_mat  # adjacency matrix
    n = A.shape[0]  # the number of nodes

    epsilon = 1e-4  # smoothing value: epsilon
    max_iter = 50  # maximum iteration value
    seeeed = 5433
    np.random.seed(seeeed)
    # print(n,c)
    topk = k

    # invD = sps.diags(np.array(A.sum(axis=0))[0, :]  ** (-1.0), 0) # Inv of degree matrix D^-1
    invD = sps.diags((np.array(A.sum(axis=0))[0, :]+eps) ** (-1.0), 0) # Inv of degree matrix D^-1
    L = (sps.identity(n) - invD.dot(A)).tocsr()  # Laplacian matrix L = I - D^-1 * A
    F = sym(np.random.random((n, c))) # Initialize a random orthogonal matrix F

    # Algorithm 1
    for step in range(max_iter):
        Q = sps.identity(n).tocsr()
        P = L.dot(F)
        for i in range(n):
            Q[i, i] = 0.5 / (spl.norm(P[i, :]) + epsilon)

        R = L.T.dot(Q).dot(L)

        W, V = np.linalg.eigh(R.todense())
        Wsort = np.argsort(W)  # sort from smallest to largest
        F = V[:, Wsort[0:c]]  # select the smallest eigenvectors

    # find SH spanner
    SH = np.zeros((n,))
    for i in range(n):
        SH[i] = np.linalg.norm(F[i, :])
    SHrank = np.argsort(SH)  # index of SH

    # print(SHrank[0:topk]+1) # the index starts from 1.


    # METRICS BEGIN

    to_keep_index = np.sort(SHrank[topk:])
    A_temp = A[to_keep_index, :]
    A_temp = A_temp[:, to_keep_index]
    HAM_labels_keep = np.asarray(ground_truth_labels)[to_keep_index]
    allLabels = np.asarray(ground_truth_labels)

    cluster_matrix = F
    labelbook, distortion = kmeans(cluster_matrix[to_keep_index, :], c)
    HAM_labels, dist = vq(cluster_matrix[to_keep_index, :], labelbook)

    print("AMI")
    print('HAM: ' + str(metrics.adjusted_mutual_info_score(HAM_labels, HAM_labels_keep.T[0])))

    # classifify SHS using majority voting
    predLabels = np.zeros(len(ground_truth_labels))
    predLabels[to_keep_index] = HAM_labels + 1
    # print(predLabels)

    HAM_predLabels = label_by_neighbors(A, predLabels)
    # print(HAM_predLabels)
    print('HAM_all: ' + str(metrics.adjusted_mutual_info_score(HAM_predLabels, allLabels.T[0])))

    print("NMI")
    print('HAM: ' + str(metrics.normalized_mutual_info_score(HAM_labels, HAM_labels_keep.T[0])))
    print('HAM_all: ' + str(metrics.normalized_mutual_info_score(HAM_predLabels, allLabels.T[0])))

    print("Entropy")
    print('HAM: ' + str(avg_entropy(HAM_labels, HAM_labels_keep.T[0])))
    print('HAM_all: ' + str(avg_entropy(HAM_predLabels, allLabels.T[0])))

    # METRICS END

    return SHrank[0:topk]+1, HAM_predLabels

if __name__ == "__main__":

    sys.path.append('../../../')
    import OpenGraph as og

    g = og.classes.Graph()

    # edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    # edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
    # edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
    # g.add_edges(edges1)
    # g.add_edges(edges2)
    # g.add_edges(edges3)
    # k = 5
    # c = 5
    # ground_truth_labels = [[0], [0], [0], [1], [1], [1], [2], [3], [3], [3], [4], [4], [4]]

    edges0 = [(1, 32), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4), (3, 33), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (4, 8), (4, 13), (4, 14), (5, 11), (5, 7), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 34), (9, 33), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 33), (24, 26), (24, 28), (24, 34), (24, 30), (25, 32), (25, 26), (25, 28), (26, 32), (27, 34), (27, 30), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 34), (31, 33), (32, 33), (32, 34), (33, 34), ]
    # edges0 = [(0, 31), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10), (0, 11), (0, 12), (0, 13), (0, 17), (0, 19), (0, 21), (1, 2), (1, 3), (1, 7), (1, 13), (1, 17), (1, 19), (1, 21), (1, 30), (2, 3), (2, 32), (2, 7), (2, 8), (2, 9), (2, 13), (2, 27), (2, 28), (3, 7), (3, 12), (3, 13), (4, 10), (4, 6), (5, 6), (5, 10), (5, 16), (6, 16), (8, 30), (8, 33), (8, 32), (9, 33), (13, 33), (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33), (19, 33), (20, 32), (20, 33), (22, 32), (22, 33), (23, 32), (23, 25), (23, 27), (23, 33), (23, 29), (24, 31), (24, 25), (24, 27), (25, 31), (26, 33), (26, 29), (27, 33), (28, 31), (28, 33), (29, 32), (29, 33), (30, 33), (30, 32), (31, 32), (31, 33), (32, 33),]
    g.add_edges(edges0)
    ground_truth_labels =[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    # print(ground_truth_labels)
    k = 3  # top-k spanners
    c = len(np.unique(ground_truth_labels))

    # ground_truth_labels=[[1], [1], [1], [1], [1], [1], [1], [1], [1], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [4], [4], [4], [4], [4], [4], [4], [4], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], [5], ]
    # edges=[(13, 18),(17, 11),(18, 17),(12, 18),(17, 14),(12, 21),(16, 12),(11, 19),(12, 20),(13, 17),(16, 20),(13, 16),(16, 22),(13, 14),(21, 13),(19, 17),(22, 13),(20, 17),(22, 14),(17, 21),(12, 22),(14, 21),(14, 11),(21, 20),(15, 16),(17, 12),(19, 22),(11, 18),(12, 15),(16, 18),(17, 16),(19, 12),(14, 19),(31, 26),(36, 30),(31, 29),(29, 34),(28, 33),(26, 36),(33, 32),(33, 25),(25, 34),(29, 24),(27, 32),(33, 30),(30, 34),(28, 34),(42, 41),(41, 44),(40, 44),(38, 43),(39, 40),(43, 42),(41, 39),(40, 42),(40, 38),(37, 41),(37, 44),(51, 61),(64, 46),(61, 84),(46, 72),(74, 50),(50, 59),(54, 84),(58, 66),(58, 68),(86, 64),(49, 81),(54, 68),(65, 71),(77, 45),(62, 55),(72, 82),(58, 53),(71, 67),(54, 71),(56, 54),(69, 55),(54, 79),(74, 61),(73, 81),(79, 47),(62, 66),(66, 48),(59, 82),(83, 71),(67, 85),(65, 72),(54, 55),(45, 67),(74, 72),(50, 58),(46, 76),(68, 57),(51, 59),(74, 62),(57, 82),(49, 86),(63, 57),(61, 45),(49, 61),(54, 86),(61, 73),(83, 58),(62, 83),(53, 50),(85, 69),(49, 59),(74, 69),(55, 60),(51, 65),(82, 67),(70, 50),(61, 47),(59, 57),]
    # g.add_edges(edges)
    # k = 5  # top-k spanners
    # c = len(np.unique(ground_truth_labels))



    # need the ground_truth_labels.
    k_top, communities = get_structural_holes_HAM(g, k, c, ground_truth_labels)
    print(k_top)
    print(communities)