import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class StmtClassifier:

	def __init__(self):
		self.clf = Pipeline([('vect', CountVectorizer(input='content', lowercase=False, binary=True)),
							('tfidf', TfidfTransformer()),
							('clf', MultinomialNB())])

	def train(self, stmts, types):
		self.clf.fit(stmts, types)

	def classify(self, stmt):
		probs = self.clf.predict_proba([stmt])
		p_tuples = sorted(enumerate(probs[0]), key=lambda p:p[1], reverse=True)
		return [self.clf.classes_[p[0]] for p in p_tuples]