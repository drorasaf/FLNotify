"""This module is the implemntation of FLDetector
Original implementation: https://github.com/zaixizhang/FLDetector/tree/main
"""
import numpy as np
from sklearn.cluster import KMeans
from validation import ValidationModel


def lbfgs(S_k_list, Y_k_list, v):
    curr_S_k = np.concat(*S_k_list, dim=1)
    curr_Y_k = np.concat(*Y_k_list, dim=1)
    S_k_time_Y_k = np.dot(curr_S_k.T, curr_Y_k)
    S_k_time_S_k = np.dot(curr_S_k.T, curr_S_k)
    R_k = np.triu(S_k_time_Y_k)
    L_k = S_k_time_Y_k - np.array(R_k)
    sigma_k = np.dot(Y_k_list[-1].T, S_k_list[-1]) / (np.dot(S_k_list[-1].T, S_k_list[-1]))
    D_k_diag = np.diag(S_k_time_Y_k)
    upper_mat = np.concat(*[sigma_k * S_k_time_S_k, L_k], dim=1)
    lower_mat = np.concat(*[L_k.T, -np.diag(D_k_diag)], dim=1)
    mat = np.concat(*[upper_mat, lower_mat], dim=0)
    mat_inv = np.linalg.inv(mat)

    approx_prod = sigma_k * v
    p_mat = np.concat(*[np.dot(curr_S_k.T, sigma_k * v), np.dot(curr_Y_k.T, v)], dim=0)
    approx_prod -= np.dot(np.dot(np.concat(*[sigma_k * curr_S_k, curr_Y_k], dim=1), mat_inv), p_mat)

    return approx_prod


def detection1(score):
    nrefs = 10
    ks = range(1, 8)
    gaps = np.zeros(len(ks))
    gapDiff = np.zeros(len(ks) - 1)
    sdk = np.zeros(len(ks))
    min = np.min(score)
    max = np.max(score)
    score = (score - min)/(max-min)
    for i, k in enumerate(ks):
        estimator = KMeans(n_clusters=k)
        estimator.fit(score.reshape(-1, 1))
        label_pred = estimator.labels_
        center = estimator.cluster_centers_
        Wk = np.sum([np.square(score[m]-center[label_pred[m]]) for m in range(len(score))])
        WkRef = np.zeros(nrefs)
        for j in range(nrefs):
            rand = np.random.uniform(0, 1, len(score))
            estimator = KMeans(n_clusters=k)
            estimator.fit(rand.reshape(-1, 1))
            label_pred = estimator.labels_
            center = estimator.cluster_centers_
            WkRef[j] = np.sum([np.square(rand[m]-center[label_pred[m]]) for m in range(len(rand))])
        gaps[i] = np.log(np.mean(WkRef)) - np.log(Wk)
        sdk[i] = np.sqrt((1.0 + nrefs) / nrefs) * np.std(np.log(WkRef))

        if i > 0:
            gapDiff[i - 1] = gaps[i - 1] - gaps[i] + sdk[i]
    for i in range(len(gapDiff)):
        if gapDiff[i] >= 0:
            select_k = i+1
            break

    if select_k == 1:
        print('No attack detected!')
        return False

    print('Attack Detected!')
    return True


class FLDetector(ValidationModel):
    def validate_client(self, client_results):
        pass
