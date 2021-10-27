from .ranking import Ranking

class RelevanceFeedback(Ranking):

    def __init__(self):
        super().__init__()
        # print('Done')

    def do_relevance_feedback(self,rel_docs=None,print_docs=False):
        relevant_docs = []
        if rel_docs is None:
            print('RELEVANCE FEEDBACK')
            print('Which documents do you think are relevant: ')
            relevant_docs =  list(map(int,input().split()))
        else:
            relevant_docs =  list(map(int,rel_docs.split()))
        relevant_docs = [x-1 for x in relevant_docs]
        non_relevant_docs = []
        for i in range(self.top_docs):
            if i not in relevant_docs:
                non_relevant_docs.append(i)
        relevant_doc_ids = [self.cosine_scores[i][1] for i in relevant_docs]
        non_relevant_doc_ids = [self.cosine_scores[i][1] for i in non_relevant_docs]

        print('Relevant Documents',relevant_doc_ids)
        print('Non Relevant Documents',non_relevant_doc_ids)
        beg = self.term_document_matrix[0,:]

        alpha = 1
        beta = 0.75
        gamma = 0.15

        relevant_sum = self.term_document_matrix[relevant_doc_ids[0],:]
        for i in range(1,len(relevant_doc_ids)):
            relevant_sum+= self.term_document_matrix[relevant_doc_ids[i],:]
        non_relevant_sum = self.term_document_matrix[non_relevant_doc_ids[0],:]
        for i in range(1,len(non_relevant_doc_ids)):
            non_relevant_sum+= self.term_document_matrix[non_relevant_doc_ids[i],:]
        print('Query before relevance feedback')
        print(self.q_vector[0,:])

        self.q_vector[0,:] = alpha*self.q_vector[0,:] + beta*(1/len(relevant_docs))*relevant_sum - gamma*(1/len(non_relevant_docs))*non_relevant_sum

        print('Query after relevance feedback')
        print(self.q_vector[0,:])

        self.cosine_scores = self.get_cosine_scores(self.q_vector[0,:])

        print('Search Results after relevance feedback: ')
        if print_docs:
            return self.print_retrieved_docs(print_docs)
        else:
            self.print_retrieved_docs(print_docs)

# if __name__ == '__main__':

#     rel_fed = RelevanceFeedback()

#     print('Enter Query: ')
#     query = input()

#     rel_fed.do_ranking(query)
#     rel_fed.print_retrieved_docs()
#     rel_fed.do_relevance_feedback()