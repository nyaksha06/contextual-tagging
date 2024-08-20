from transformers import AutoModel , AutoTokenizer
import torch
from .models import Tag


class EmbeddingModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


    def encode(self,text):
        inputs = self.tokenizer(text, return_tensors='pt', padding= True , truncation = True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings.squeeze().tolist()





embedding_model = EmbeddingModel()    


def get_relevant_tags(content , top_n=1):
    content_embedding = embedding_model.encode(content)

    tags =Tag.objects.all()

    similarities = []

    for tag in tags:

        tag_embedding = torch.tensor(tag.embedding)

        similarity = torch.nn.functional.cosine_similarity(
            torch.tensor(content_embedding), tag_embedding,dim=0
        ).item()

        similarities.append((tag.name, similarity))



    sorted_tags = sorted(similarities , key=lambda x:x[1],reverse=True)

    return [tag for tag, _ in sorted_tags[:top_n]]   

