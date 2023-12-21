from src.models.base import BaseJobSimilarity
import wget
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from navec import Navec
from razdel import tokenize
import pymorphy2


class NavecJobSimilarity(BaseJobSimilarity):
    """
    Extracts job title from resumes and generates embeddings for them.
    """

    def __init__(self):
        if not os.path.exists("navec_hudlit_v1_12B_500K_300d_100q.tar"):
            wget.download(
                "https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar"
            )
        self.navec = Navec.load("navec_hudlit_v1_12B_500K_300d_100q.tar")
        self.embedding_dim = 300
        self.morph = pymorphy2.MorphAnalyzer()

    def find_similarity(self, word1, word2):
        resume_emb = self.get_sentence_embedding(word1)
        vacancy_emb = self.get_sentence_embedding(word2)
        try:
            return cosine_similarity([resume_emb], [vacancy_emb])[0][0]
        except:
            return 0

    def tokenizer_razdel(self, text):
        navec_words = []
        tokens = [_.text for _ in list(tokenize(text))]
        for word in [self.morph.parse(_)[0].normal_form for _ in tokens]:
            try:
                self.navec[word]
                navec_words.append(word)
            except:
                pass
        return navec_words

    def get_sentence_embedding(self, sentence):
        words = self.tokenizer_razdel(sentence)
        sentence_len = len(words)
        embedding = np.zeros(self.embedding_dim)
        for word in words:
            self.navec[word.lower()]
            embedding += self.navec[word.lower()]
        return embedding / sentence_len
