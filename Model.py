from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB, ComplementNB
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
from numpy.random import seed

class RF:
    def __init__(self, X, y, X_test, y_test):
        # super(RandomForestClassifier, self).__init__(self)
        seed(2020)
        self.model = RandomForestClassifier(n_estimators=120,
                                            max_depth=12,
                                            min_samples_split=10,
                                            min_samples_leaf=10,
                                            criterion="gini",
                                            oob_score=True,
                                            class_weight={1: 1, 2: 5},
                                            random_state=13,
                                            verbose=0)
        self.X = X
        self.y = y
        self.X_test = X_test
        self.y_test = y_test

    def rf_train(self):
        self.model.fit(self.X, self.y)
        return self.model.feature_importances_, self.model.oob_score_

    def rf_predict(self):
        result = self.model.predict(self.X_test)
        return result

    def rf_predict_prob(self):
        result = self.model.predict_proba(self.X_test)
        return result

    def rf_score(self):
        return self.model.score(self.X_test, self.y_test)

    def rf_save(self):
        joblib.dump(self.model, 'model/rf.pkl')


def rf_para_tuning(x, y):
    param_test1 = {'min_samples_leaf': range(10, 60, 10), 'min_samples_split': range(10, 101, 10)}
    gsearch1 = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=60,
                                                             oob_score=True),
                            param_grid=param_test1, scoring='roc_auc', cv=5)
    gsearch1.fit(x, y)
    print(gsearch1.scorer_)
    print(gsearch1.best_params_)
    print(gsearch1.best_score_)


class GBDT:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        # super(GradientBoostingClassifier, self).__init__(self)
        self.model = GradientBoostingClassifier(loss='deviance',
                                                n_estimators=150,
                                                learning_rate=0.05,
                                                subsample=0.8,
                                                min_samples_split=6,
                                                min_samples_leaf=4,
                                                criterion='friedman_mse',
                                                max_depth=13,
                                                random_state=13,
                                                verbose=0)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def gbdt_train(self):
        self.model.fit(self.X, self.y)
        return self.model.feature_importances_, self.model.train_score_

    def gbdt_predict(self):
        result = self.model.predict(self.X_test)
        return result

    def gbdt_predict_prob(self):
        result = self.model.predict_proba(self.X_test)
        return result

    def gbdt_score(self):
        return self.model.score(self.X_test, self.y_test)


class LRl2:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        self.model = LogisticRegression(penalty='l2',
                                        C=0.85,
                                        solver='liblinear',
                                        max_iter=300,
                                        class_weight={1: 1, 2: 4},
                                        random_state=13,
                                        tol=1e-4)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def lr_train(self):
        self.model.fit(self.X, self.y)
        return self.model.coef_

    def lr_predict(self):
        return self.model.predict(self.X_test)

    def lr_predict_proba(self):
        return self.model.predict_proba(self.X_test)

    def lr_score(self):
        return self.model.score(self.X_test, self.y_test)


class LRl1:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        self.model = LogisticRegression(penalty='l1',
                                        C=0.85,
                                        solver='liblinear',
                                        max_iter=300,
                                        class_weight={1: 1, 2: 4},
                                        random_state=13,
                                        tol=1e-4)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def lr_train(self):
        self.model.fit(self.X, self.y)
        return self.model.coef_

    def lr_predict(self):
        return self.model.predict(self.X_test)

    def lr_predict_proba(self):
        return self.model.predict_proba(self.X_test)

    def lr_score(self):
        return self.model.score(self.X_test, self.y_test)


class KNN:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        self.model = KNeighborsClassifier(n_neighbors=2,
                                          weights='distance',
                                          algorithm='auto',
                                          leaf_size=30,
                                          p=2,
                                          metric='minkowski',
                                          metric_params=None,
                                          n_jobs=None)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def knn_train(self):
        self.model.fit(self.X, self.y)

    def knn_predict(self):
        return self.model.predict(self.X_test)

    def knn_predict_proba(self):
        return self.model.predict_proba(self.X_test)

    def score(self):
        return self.model.score(self.X_test, self.y_test)


class SVM:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        self.model = SVC(C=1.0,
                         kernel='linear',
                         degree=3,
                         gamma='scale',
                         coef0=0.0,
                         shrinking=True,
                         probability=True,
                         tol=0.001,
                         cache_size=200,
                         class_weight={1: 1, 2: 3},
                         verbose=False,
                         max_iter=-1,
                         decision_function_shape='ovr',
                         break_ties=False,
                         random_state=13)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def svm_train(self):
        self.model.fit(self.X, self.y)
        return self.model.coef_

    def svm_predict(self):
        return self.model.predict(self.X_test)

    def svm_predict_confidence(self):
        return self.model.predict_proba(self.X_test)

    def svm_score(self):
        return self.model.score(self.X_test, self.y_test)


class MLP:
    def __init__(self, X, y, X_test, y_test):
        seed(2020)
        self.model = MLPClassifier(hidden_layer_sizes=2,
                                   activation='relu',
                                   solver='sgd',
                                   learning_rate_init=0.01,
                                   max_iter=400,
                                   random_state=13)
        std = StandardScaler()
        self.X = std.fit_transform(X)
        self.y = y
        self.X_test = std.transform(X_test)
        self.y_test = y_test

    def mlp_train(self):
        self.model.fit(self.X, self.y)

    def mlp_predict(self):
        return self.model.predict(self.X_test)

    def mlp_predict_prob(self):
        return self.model.predict_proba(self.X_test)

    def mlp_score(self):
        return self.model.score(self.X_test, self.y_test)


class StackModel:
    def __init__(self):
        seed(2020)
        self.model = [RandomForestClassifier(n_estimators=150,
                                             max_depth=11,
                                             min_samples_split=10,
                                             min_samples_leaf=10,
                                             criterion="gini",
                                             oob_score=True,
                                             class_weight={1: 1, 2: 4},
                                             random_state=13,
                                             verbose=0),
                      SVC(C=1.0,
                         kernel='linear',
                         degree=3,
                         gamma='scale',
                         coef0=0.0,
                         shrinking=True,
                         probability=True,
                         tol=0.001,
                         cache_size=200,
                         class_weight={1: 1, 2: 3},
                         verbose=False,
                         max_iter=-1,
                         decision_function_shape='ovr',
                         break_ties=False,
                         random_state=13)]
        self.LR = LogisticRegression(penalty='l2',
                                     C=0.85,
                                     solver='liblinear',
                                     max_iter=300,
                                     class_weight={1: 1, 2: 4},
                                     random_state=13,
                                     tol=1e-4)

        self.RF = RandomForestClassifier(n_estimators=80,
                                         criterion="gini",
                                         class_weight={1: 1, 2: 2.5},
                                         random_state=13,
                                         verbose=0)

        self.GBDT = GradientBoostingClassifier()

    def train(self, X, y):
        y = y.reshape(len(y), )
        blend_train = np.zeros((X.shape[0], len(self.model)))
        n_folds = 5
        skf = StratifiedKFold(n_folds)
        for j, clf in enumerate(self.model):
            '''training every single model'''
            for i, (train, test) in enumerate(skf.split(X, y)):
                '''part i as predicting, the rest as training. predicting result of part ad new feature'''
                print(j, i)
                X_train, y_train, X_test, y_test = X[train], y[train], X[test], y[test]
                clf.fit(X_train, y_train)
                y_submission = clf.predict_proba(X_test)[:, 1]
                blend_train[test, j] = y_submission
            self.LR.fit(blend_train, y)

    def predict_proba(self, X, y):
        blend_test = np.zeros((X.shape[0], len(self.model)))
        n_folds = 5
        skf = StratifiedKFold(n_folds)
        for j, clf in enumerate(self.model):
            '''training every single model'''
            blend_test_j = np.zeros((X.shape[0], skf.get_n_splits(X, y)))
            for i, (train, test) in enumerate(skf.split(X, y)):
                blend_test_j[:, i] = clf.predict_proba(X)[:, 1]
            '''using mean of k models as new feature'''
            blend_test[:, j] = blend_test_j.mean(axis=1)
            # print("val auc Score: %f" % roc_auc_score(self.y_predict, self.blend_test[:, j]))
        print('ensemble get score:', self.LR.score(blend_test, y))
        return self.LR.predict(blend_test), self.LR.predict_proba(blend_test)


class VotingModel:
    def __init__(self):
        seed(2020)
        self.rf = RandomForestClassifier(n_estimators=120,
                                         max_depth=12,
                                         min_samples_split=10,
                                         min_samples_leaf=10,
                                         criterion="gini",
                                         oob_score=True,
                                         class_weight={1: 1, 2: 5},
                                         random_state=13,
                                         verbose=0)
        self.gbdt = GradientBoostingClassifier(loss='deviance',
                                               n_estimators=150,
                                               learning_rate=0.05,
                                               subsample=0.8,
                                               criterion='friedman_mse',
                                               max_depth=13,
                                               random_state=13,
                                               verbose=0)
        self.lr = LogisticRegression(penalty='l2',
                                     C=0.85,
                                     solver='liblinear',
                                     max_iter=300,
                                     class_weight={1: 1, 2: 4},
                                     random_state=13,
                                     tol=1e-4)
        self.svm = SVC(C=1.0,
                       kernel='linear',
                       degree=3,
                       gamma='scale',
                       coef0=0.0,
                       shrinking=True,
                       probability=True,
                       tol=0.001,
                       cache_size=200,
                       class_weight={1: 1, 2: 3},
                       verbose=False,
                       max_iter=300,
                       decision_function_shape='ovr',
                       break_ties=False,
                       random_state=13)
        self.model = VotingClassifier(estimators=[('rf', self.rf),
                                                  ('gbdt', self.gbdt),
                                                  ('lr', self.lr),
                                                  ('svm', self.svm)],
                                      voting='soft',
                                      weights=[1, 0.7, 0.8, 0.8])

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def predict_proba(self, X_test):
        return self.predict_proba(X_test)

