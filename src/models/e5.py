from src.models.base import BaseJobSimilarity
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F
from torch import Tensor
import numpy as np

class E5(BaseJobSimilarity):

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
        self.model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')

    def average_pool(self, last_hidden_states: Tensor,
                     attention_mask: Tensor) -> Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

    def find_similarity(self, sent1: str, sent2: str) -> float:
        # Tokenize the input texts
        batch_dict = self.tokenizer([sent1, sent2], max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**batch_dict)
        embeddings = self.average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        # normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        scores = (embeddings @ embeddings.T) * 100
        scores = scores.tolist()
        scores = np.divide(scores, 100)
        if scores[0][1] < 0.8:
            return 0
        elif scores[0][1] > 0.9:
            return 1
        else:
            return (scores[0][1]-0.8)*10

    def make_predictions_e5(self, evaluation_data):
        evaluation_data["prediction"] = evaluation_data.apply(lambda x: self.e5_sts(x["Резюме"], x["Вакансия"]), axis=1)
        return evaluation_data