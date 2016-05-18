from collections import defaultdict


class Lexicon:
    """"Simple default implementation of a lexicon, which scores word,
    tag pairs with a smoothed estimate of P(tag|word)/P(tag)."""

    # Builds a lexicon from the observed tags in a list of training trees.
    def __init__(self, train_trees):
        self.word_to_tag_counters = defaultdict(float)
        self.total_tokens = 0.0
        self.total_word_types = 0.0
        self.tag_counter = defaultdict(float)
        self.word_counter = defaultdict(float)
        self.type_tag_counter = defaultdict(float)

        for train_tree in train_trees:
            words = train_tree.get_yield()
            tags = train_tree.get_pre_terminal_yield()
            for position in xrange(len(words)):
                word = words[position]
                tag = tags[position]
                self.tally_tagging(word, tag)

    def tally_tagging(self, word, tag):
        if not self.is_known(word):
            self.total_word_types += 1
            self.type_tag_counter[tag] += 1

        self.total_tokens += 1
        self.tag_counter[tag] += 1
        self.word_counter[word] += 1
        self.word_to_tag_counters[(word, tag)] += 1

    def is_known(self, word):
        return word in self.word_counter.keys()

    def get_all_tags(self):
        return self.tag_counter.keys()

    # Returns a smoothed estimate of P(word|tag)
    def score_tagging(self, word, tag):
        p_tag = self.tag_counter[tag] / self.total_tokens
        c_word = self.word_counter[word]
        c_tag_and_word = self.word_to_tag_counters[(word, tag)]
        if c_word < 10: # rare or unknown
            c_word += 1
            c_tag_and_word += self.type_tag_counter[tag] / self.total_word_types

        p_word = (1.0 + c_word) / (self.total_tokens + self.total_word_types)
        p_tag_given_word = c_tag_and_word / c_word
        return p_tag_given_word / p_tag * p_word
