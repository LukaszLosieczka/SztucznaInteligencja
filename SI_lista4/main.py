import pickle
from text_classification import TextClassification, Classification


def string_from_txt(path):
    file = open(path, "r")
    return file.read()


def preprocessing():
    print("Starting preprocessing")
    txt_classifier = TextClassification("booksummaries/booksummaries.txt", "\t", 6, 7, "\n")
    txt_classifier.load_data(500)
    index = 1
    for genre in txt_classifier.books.keys():
        print(f"{index}. {genre}: {len(txt_classifier.books[genre])}")
        index += 1
    txt_classifier.feature_selection()
    print("Finished preprocessing")
    return txt_classifier


def save_text_classification(txt_classifier):
    with open('text_classification_data.pkl', 'wb') as output:
        pickle.dump(txt_classifier, output, pickle.HIGHEST_PROTOCOL)


def load_text_classification():
    print("Starting loading text_classification from file")
    with open('text_classification_data.pkl', 'rb') as inp:
        result = pickle.load(inp)
        print("Finished loading text_classification from file")
        return result


if __name__ == '__main__':
    # text_classifier = preprocessing()
    # save_text_classification(text_classifier)
    text_classifier = load_text_classification()
    text_classifier.train_svm_classifier()
    text_classifier.train_decision_tree_classifier()
    save_text_classification(text_classifier)

    print(f"Score SVM: {round(text_classifier.test_classifier(Classification.SVM), 2)}")
    print(f"Score Decision Tree: {round(text_classifier.test_classifier(Classification.DECISION_TREE), 2)}")
