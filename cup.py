#!/usr/bin/env python3
import matplotlib.pyplot as plt
import neural_network as nn
import pandas as pd
import numpy as np
import datetime


# load data
dataset = pd.read_csv('datasets/cup/ML-CUP19-TR.csv', header=None)
dataset_test = pd.read_csv('datasets/cup/ML-CUP19-TS.csv', header=None)
training_set = dataset.iloc[:,:].values
test_set = dataset_test.iloc[:,:].values

# grid search
grid = [{'lr': 0.01, 'epochs': 2000, 'alpha': 0.02, 'lambda': 0.001, 'nhidden': 10, 'mb': 50, 'nfolds': 3, 'activation': 'sigmoid', 'loss': 'mse', 'n_outputs': 2}]
now = datetime.datetime.now()
for i, g in enumerate(grid):
    folder = "{0}_{1}".format(now.strftime('%Y%m%d_%H%M%S'), i+1)
    grid_tr_errors = []
    grid_vl_errors = []
    # hyperparameters
    lr = g["lr"]
    epochs = g["epochs"]
    alpha = g["alpha"]
    lmbda = g["lambda"]
    n_hidden = g["nhidden"]
    mb = g["mb"] # mini-batch equals to number of examples means applying SGD
    loss = g["loss"]
    n_folds = g["nfolds"]
    activation = g["activation"]
    n_outputs = g["n_outputs"]
    # building the model
    model = nn.NeuralNetwork(error='mee', loss=loss, learn_alg='sgd')
    model.add(nn.Layer(dim=(training_set.shape[1]-n_outputs, n_hidden), activation=activation))
    model.add(nn.Layer(dim=(n_hidden, 2), activation='sigmoid', is_output=True))
    # k-fold cross validation
    fold = 1
    for TR, VL in nn.k_fold_cross_validation(X=training_set, K=n_folds, shuffle=True):
        print('Fold #{:d}'.format(fold))
        print(TR.shape)
        print(VL.shape)
        tr_errors, vl_errors = model.fit(TR, VL, lr, epochs, mb, alpha, lmbda)
        grid_tr_errors.append(tr_errors)
        grid_vl_errors.append(vl_errors)
        fold += 1
    # mean the i-th elements of the list of k-folds
    tr_errors = [0] * len(grid_tr_errors[0])
    vl_errors = [0] * len(grid_vl_errors[0])
    for lst in grid_tr_errors:
        for i, e in enumerate(lst):
            tr_errors[i] += e
    for lst in grid_vl_errors:
        for i, e in enumerate(lst):
            vl_errors[i] += e
    tr_errors = [x/n_folds for x in tr_errors]
    vl_errors = [x/n_folds for x in vl_errors]
    # plot learning curve
    plt.plot(tr_errors)
    plt.plot(vl_errors)
    plt.title('Learning curve')
    plt.xlabel('Batch')
    plt.ylabel('Error')
    plt.legend(['training', 'validation'], loc='upper right')
    desc = str(g)
    model.save(folder, desc, plt)
    