import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class StmtClassifier:

	def __init__(self):
		self.clf = Pipeline([('vect', CountVectorizer(lowercase=False)),
							('tfidf', TfidfTransformer()),
							('clf', MultinomialNB())])

	def train(self, stmts, types):
		self.clf.fit(stmts, types)

	def test(self, stmts):
		return self.clf.predict(stmts)

	def classify_stmt(self, stmt):
		sorted_probs = get_stmt_probs(stmt)
		return sorted_probs[0][0]

	# returns list of (type, prob) tuples sorted by prob in ascending order
	def get_stmt_probs(self, stmt):
		probs = self.clf.predict_log_proba(stmt)
		results = []
		for i, p in enumerate(probs):
			results.append((self.clf.classes_[i], p))
		return sorted(results, key=lambda tup: tup[1], reverse=True) # sort by prob