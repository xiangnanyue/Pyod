import os
import matplotlib.pyplot as plt
from data.load_data import generate_data
from utility.utility import get_precn
from sklearn.metrics import roc_auc_score
from models.hbos import Hbos

if __name__ == "__main__":
    # percentage of outliers
    contamination = 0.1
    n_train = 1000
    n_test = 500

    X_train, y_train, c_train, X_test, y_test, c_test = generate_data(
        n=n_train,
        contamination=contamination,
        n_test=n_test)

    # train a HBOS detector
    clf = Hbos(contamination=0.1)
    clf.fit(X_train)

    y_train_pred = clf.y_pred
    y_train_score = clf.decision_scores

    y_test_pred = clf.predict(X_test)
    y_test_score = clf.decision_function(X_test)

    print('Precision@n on train data is', get_precn(y_train, y_train_score))
    print('ROC on train data is', roc_auc_score(y_train, y_train_score))

    print('Precision@n on test data is', get_precn(y_test, y_test_score))
    print('ROC on test data is', roc_auc_score(y_test, y_test_score))

    # plot the results
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(221)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=c_train)
    plt.title('train data')

    ax = fig.add_subplot(222)
    plt.scatter(X_test[:, 0], X_test[:, 1], c=c_test)
    plt.title('test data')

    ax = fig.add_subplot(223)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train_pred)
    plt.title('y_pred_train by HBOS')

    ax = fig.add_subplot(224)
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test_pred)
    plt.title('y_pred_test by HBOS')

    plt.savefig(os.path.join('figures', 'sample.png'), dpi=300)
    plt.show()
