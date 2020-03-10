import sys, pickle, os, random
import numpy as np

## tags, BIO
tag2label = {"N": 0,
             "解剖部位": 1, "手术": 2,
             "药物": 3, "独立症状": 4,
             "症状描述": 5}

def read_corpus(corpus_path):
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_ = [], []
    for line in lines:
        if line != '\n':
            tmp = line.strip().split(' ')
            if (len(tmp) > 1):
                char = tmp[0]
                label = tmp[1]
                sent_.append(char)
                tag_.append(label)
        else:
            data.append((sent_,tag_))
            sent_,tag_ = [],[]

    return data

def sentence2id(sent, word2id):
    sentence_id = []
    for word in sent:
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id


def read_dictionary(vocab_path):
    vocab_path = os.path.join(vocab_path)
    with open(vocab_path,'rb') as fr:
        word2id = pickle.load(fr)
    return word2id


def random_embedding(vocab, embedding_dim):
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab) + 1, embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat

def pad_sequences(sequences, pad_mark=0):
    max_len = max(map(lambda x: len(x), sequences))
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq),max_len))
    return seq_list, seq_len_list

def batch_yield(data, batch_size, word2id, tag2label, shuffle=False):
    if shuffle:
        random.shuffle(data)
    seqs, labels = [], []
    for (sent_, tag_) in data:
        sent_ = sentence2id(sent_, word2id)
        label_ = [tag2label[tag] for tag in tag_]

        if len(seqs) == batch_size:
            yield seqs, labels
            seqs, labels = [], []
        seqs.append(sent_)
        labels.append(label_)
    if len(seqs) != 0:
        yield seqs, labels