import json
import re
from json import JSONDecodeError

from enum import Enum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn import svm


class Classification(Enum):
    DECISION_TREE = 1
    SVM = 2


class Summary:
    def __init__(self, text, genre):
        self.text = text
        self.vector = []
        self.genre = genre

    def get_word_count(self, index):
        return self.vector[index]

    def get_length(self):
        return len(self.text)


def get_words_from_text(text):
    words = {}
    words_list = text.split()
    for i in range(len(words_list)):
        word = words_list[i]
        word = re.sub(r'[^a-zA-Z]', '', word)
        word = word.lower()
        words[word] = 1 if words.get(word) is None else words[word] + 1
    return [(k, v) for k, v in words.items()]


class TextClassification:
    def __init__(self, source_file, column_separator, genres_column, summary_column, data_separator):
        self.source_file = source_file
        self.column_separator = column_separator
        self.genres_column = genres_column
        self.summary_column = summary_column
        self.data_separator = data_separator
        self.books: {str: [Summary]} = {}

        self.features = []

        self.tags = []
        self.vectors = []

        self.training_set = {"tags": [], "vectors": []}

        self.testing_set = {"tags": [], "vectors": []}

        self.decision_tree_classifier = tree.DecisionTreeClassifier()
        self.svm_classifier = svm.SVC()

        self.best_params_svm = {}
        self.svm_validated = False

        self.best_params_tree = {}
        self.tree_validated = False

    @staticmethod
    def __clean_genres(genres):
        genres_txt = ""
        for key in genres.keys():
            genres_txt += "\t" + genres[key]
        genres_words_list = get_words_from_text(genres_txt)
        genres_words_list = sorted(genres_words_list, key=lambda tup: tup[1], reverse=True)
        genres_score = {}
        for key in genres.keys():
            max_points = len(genres_words_list)
            for word in genres_words_list:
                if word[0] in re.sub(r'[^a-zA-Z]', '', genres[key]).lower():
                    genres_score[key] = max_points if genres_score.get(key) is None else genres_score[key] + max_points
                max_points -= 1
        genres_score_list = [(k, v) for k, v in genres_score.items()]
        best_key = sorted(genres_score_list, key=lambda tup: tup[1], reverse=True)[0][0]
        return genres[best_key]

    def load_data(self, min_books_per_genre):
        print("Start loading data")
        file = open(self.source_file, "r")
        text = file.read()
        for data in text.split(self.data_separator):
            columns = data.split(self.column_separator)
            if len(columns) != 7:
                continue
            try:
                genres = json.loads(columns[self.genres_column - 1])
            except JSONDecodeError:
                continue
            summary = columns[self.summary_column - 1]
            if len(summary) > 0:
                genre = self.__clean_genres(genres)
                if self.books.get(genre) is None:
                    self.books[genre] = [Summary(summary, genre)]
                else:
                    self.books[genre].append(Summary(summary, genre))
        for genre in list(self.books.keys()):
            if len(self.books[genre]) <= min_books_per_genre:
                self.books.pop(genre)
        self.generate_words_bag()
        print("Finished loading data")

    def generate_words_bag(self):
        print("Start generating words bag")
        summary_list = [summary for sum_list in self.books.values() for summary in sum_list]
        self.tags = [s.genre for s in summary_list]
        texts_list = [s.text for s in summary_list]
        count_vector = CountVectorizer(stop_words="english", token_pattern=r"\b[^\d\W]+\b")
        self.vectors = count_vector.fit_transform(texts_list).toarray()
        self.features = count_vector.get_feature_names_out()
        for i in range(len(summary_list)):
            summary_list[i].vector = self.vectors[i]
        print("Finished generating words bag")

    def feature_selection(self, k=1000):
        print("Starting feature selection")
        sel = SelectKBest(chi2, k=k)
        self.vectors = sel.fit_transform(self.vectors, self.tags)
        self.features = sel.get_feature_names_out(self.features)
        print("Finished feature selection")

    def extract_training_and_testing_sets(self, training_percentage=70):
        index = 0
        for genre in self.books.keys():
            genre_size = len(self.books[genre])
            training_size = int(genre_size * training_percentage / 100)
            samples_added = 0
            for i in range(genre_size):
                if samples_added == training_size:
                    self.testing_set["tags"].append(self.tags[index])
                    self.testing_set["vectors"].append(self.vectors[index])
                else:
                    self.training_set["tags"].append(self.tags[index])
                    self.training_set["vectors"].append(self.vectors[index])
                    samples_added += 1
                index += 1

    def cross_validation_svm(self):
        print("Starting cross validation for svm")
        params = [{"C": 1, "kernel": 'rbf', "gamma": 'scale'},
                  {"C": 10, "kernel": 'rbf', "gamma": 'scale'},
                  {"C": 10, "kernel": 'rbf', "gamma": 'auto'},
                  {"C": 1, "kernel": 'linear', "gamma": 'scale'}]
        max_score = -1
        max_score_index = -1
        index = 0
        for p in params:
            self.svm_classifier = svm.SVC(kernel=p["kernel"], C=p["C"], gamma=p["gamma"])
            vectors = self.training_set["vectors"]
            tags = self.training_set["tags"]
            scores = cross_val_score(self.svm_classifier, vectors, tags, cv=2, scoring="accuracy")
            if scores.mean() > max_score:
                max_score = scores.mean()
                max_score_index = index
            index += 1
        print(f"Best params {params[max_score_index]}")
        print("Finished cross validation for svm")
        self.best_params_svm = params[max_score_index]
        self.svm_validated = True

    def cross_validation_tree(self):
        print("Starting cross validation for decision tree")
        params = [{"criterion": 'gini', "splitter": 'best'},
                  {"criterion": 'gini', "splitter": 'random'},
                  {"criterion": 'entropy', "splitter": 'best'}]
        max_score = -1
        max_score_index = -1
        index = 0
        for p in params:
            self.svm_classifier = tree.DecisionTreeClassifier(criterion=p["criterion"], splitter=p["splitter"])
            vectors = self.training_set["vectors"]
            tags = self.training_set["tags"]
            scores = cross_val_score(self.decision_tree_classifier, vectors, tags, cv=2, scoring="accuracy")
            if scores.mean() > max_score:
                max_score = scores.mean()
                max_score_index = index
            index += 1
        print(f"Best params {params[max_score_index]}")
        print("Finished cross validation for decision tree")
        self.best_params_tree = params[max_score_index]
        self.tree_validated = True

    def train_decision_tree_classifier(self):
        print("Starting training decision tree classifier")
        self.extract_training_and_testing_sets()
        if not self.tree_validated:
            self.cross_validation_tree()
        best_params = self.best_params_tree
        self.decision_tree_classifier = tree.DecisionTreeClassifier(criterion=best_params["criterion"],
                                                                    splitter=best_params["splitter"])
        vectors = self.training_set["vectors"]
        tags = self.training_set["tags"]
        self.decision_tree_classifier = self.decision_tree_classifier.fit(vectors, tags)
        print("Finished training decision tree classifier")

    def train_svm_classifier(self):
        print("Starting training svm classifier")
        self.extract_training_and_testing_sets()
        if not self.svm_validated:
            self.cross_validation_svm()
        best_params = self.best_params_svm
        self.svm_classifier = svm.SVC(C=best_params["C"], kernel=best_params["kernel"], gamma=best_params["gamma"])
        vectors = self.training_set["vectors"]
        tags = self.training_set["tags"]
        self.svm_classifier = self.svm_classifier.fit(vectors, tags)
        print("Finished training svm classifier")

    def test_classifier(self, classifier: Classification):
        print("Starting testing classifier")
        y_predicted = self.predict(self.testing_set["vectors"], classification=classifier)
        print("Finished testing classifier")
        return accuracy_score(self.testing_set["tags"], y_predicted)

    def get_vector_from_text(self, text):
        count_vector = CountVectorizer(vocabulary=self.features, stop_words="english", token_pattern=r"\b[^\d\W]+\b")
        return count_vector.fit_transform([text]).toarray()

    def predict_text(self, text, classification=Classification.DECISION_TREE):
        vector = self.get_vector_from_text(text)
        return self.predict(vector, classification=classification)

    def predict(self, vector, classification=Classification.DECISION_TREE):
        if classification == Classification.DECISION_TREE:
            return self.decision_tree_classifier.predict(vector)
        elif classification == Classification.SVM:
            return self.svm_classifier.predict(vector)
