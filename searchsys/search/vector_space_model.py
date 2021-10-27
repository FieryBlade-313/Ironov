from Indexer import *
import pickle
import numpy as np
import os

class VSM:
    def __init__(self):
        self.term_to_idx = {}
        self.all_terms = []
        self.document_frequency = {}
        # print('Loading')

        temp = open('Cache/postingList.data', 'rb')
        self.posting_list = pickle.load(temp)
        temp.close()

        temp = open('Cache/docSet.data', 'rb')
        self.doc_set = pickle.load(temp)
        temp.close()

        # print('Done Loading')

    def log_tf(self,ele):
        if ele:
            return 1 + np.log(ele)
        else:
            return 0

    def create_tdm(self):


        self.all_terms = list(self.posting_list.posting_list.keys())
        self.term_to_idx = {}
        for idx, term in enumerate(self.all_terms):
            self.term_to_idx[term] = idx


        for key, val in self.posting_list.posting_list.items():
            self.document_frequency[key] = val.get_Node_info()[0]

        self.term_document_matrix = np.zeros((1990, 35558))

        for key, value in self.doc_set.posting_list.items():
            doc_terms = value.get_Node_info()[1]
            for k, v in doc_terms.items():
                self.term_document_matrix[key][self.term_to_idx[k]] = v

        print('Document Matrix')
        apply_log_df = np.vectorize(self.log_tf)
        self.term_document_matrix = apply_log_df(self.term_document_matrix)
        for key, val in self.document_frequency.items():
            idx_term = self.term_to_idx[key]
            self.term_document_matrix[:, idx_term] = self.term_document_matrix[:, idx_term] / val
        print(self.term_document_matrix)


    def save_val(self,dir='Cache1'):

        if not os.path.isdir(dir):
            os.mkdir(dir)
            print('Created Cache1')

            print('Saving Term Document Matrix')
            temp = open(dir+'/tdm.data', 'wb')
            pickle.dump(self.term_document_matrix, temp)
            temp.close()

            print('Saving Document Frequency')
            temp = open(dir+'/df.data', 'wb')
            pickle.dump(self.document_frequency, temp)
            temp.close()

            print('Saving All terms')
            temp = open(dir+'/at.data', 'wb')
            pickle.dump(self.all_terms, temp)
            temp.close()

            print('Saving Term to Index ')
            temp = open(dir+'/tdi.data', 'wb')
            pickle.dump(self.term_to_idx, temp)
            temp.close()
        else:
            print('Cache 1 Already present')

vsm = VSM()
# vsm.create_tdm()
vsm.save_val()
