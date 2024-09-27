


from sentence_transformers import CrossEncoder



class Reranker:

    def __init__(self,model_name):
        self.cross_encoder = CrossEncoder(model_name)


    def predict(self,pairs):
        return self.cross_encoder.predict(pairs)