from sentence_transformers import SentenceTransformer, models
import sklearn
import pandas as pd
import numpy as np

def transformerModel(data,path_to_model,seq_length):

    word_embedding_model = models.Transformer(path_to_model,seq_length)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    embeddings = model.encode(data)

    return embeddings

