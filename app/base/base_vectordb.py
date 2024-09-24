from app.embeddings.loader import EmLoader

class BaseVectorDB():

    def load_embeddings_function(self):
        return EmLoader(self.embeddings).load_embclass().load_emb()