import pickle
import numpy as np

class Ranking:

    def __init__(self,n=15):
        self.top_docs = n

        # print('Loading')
        temp = open('search/Cache1/at.data', 'rb')
        self.all_terms = pickle.load(temp)
        temp.close()

        temp = open('search/Cache1/tdi.data', 'rb')
        self.term_to_idx = pickle.load(temp)
        temp.close()

        temp = open('search/Cache1/df.data', 'rb')
        self.document_frequency = pickle.load(temp)
        temp.close()

        temp = open('search/Cache1/tdm.data', 'rb')
        self.term_document_matrix = pickle.load(temp)
        temp.close()

        # print('Done Loading')

    def log_tf(self,ele):
        if ele:
            return float(1 + np.log(ele))
        else:
            return 0.0

    def cosine_similarity(self,vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def get_cosine_scores(self,query):
        cosine_scores = [(self.cosine_similarity(self.term_document_matrix[i, :], query), i) for i in
                         range(self.term_document_matrix.shape[0])]
        cosine_scores.sort(key=lambda x: x[0], reverse=True)
        return cosine_scores

    def do_ranking(self,query):

        query_terms = query.strip().split()
        q_vector = np.zeros((1, 35558))

        for word in query_terms:
            if word in self.all_terms:
                q_vector[0][self.term_to_idx[word]] += 1

        apply_log_df = np.vectorize(self.log_tf)
        q_vector = apply_log_df(q_vector)
        for word in self.all_terms:
            q_vector[0][self.term_to_idx[word]] = q_vector[0][self.term_to_idx[word]] / self.document_frequency[word]

        self.q_vector = q_vector
        self.cosine_scores = self.get_cosine_scores(self.q_vector[0, :])

    def print_retrieved_docs(self,print_doc=False):
        if print_doc is False:
            print('Search Results: ')
            for ele in self.cosine_scores[:self.top_docs]:
                print(ele[1], ele[0])
        else:
            return [(ele[1], ele[0]) for ele in self.cosine_scores[:self.top_docs]]

# if __name__ == '__main__':
#     rank = Ranking()
#     print('Enter Query: ')
#     query = input()

#     rank.do_ranking(query)
#     rank.print_retrieved_docs()

