
import numpy as np
import torch

import sacrebleu
import pyter
from bert_score import score
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.metrics import confusion_matrix

'''
args: ndarray[float]
'''
def classification_metrics(preds, labels):
    try: # Multi Label
        accuracy = accuracy_score(y_true=labels, y_pred=preds, average='weighted')
    except: # Bin Label
        accuracy = accuracy_score(y_true=labels, y_pred=preds)
    try: # Multi Label
        recall = recall_score(y_true=labels, y_pred=preds, average='weighted')
    except: # Bin Label
        recall = recall_score(y_true=labels, y_pred=preds)
    try: # Multi Label
        precision = precision_score(y_true=labels, y_pred=preds, average='weighted')
    except: # Bin Label
        precision = precision_score(y_true=labels, y_pred=preds)
    try: # Multi Label
        f1_macro = f1_score(y_true=labels, y_pred=preds, average='macro')
        f1_micro = f1_score(y_true=labels, y_pred=preds, average='micro')
    except: # Bin Label
        f1_macro = f1_score(y_true=labels, y_pred=preds, average='macro')
        f1_micro = f1_score(y_true=labels, y_pred=preds, average='micro')
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1_micro": f1_micro, "f1_macro": f1_macro}

'''
args: List[str]
'''
def bleu_score(hyp,ref):
    corpus_bleu = sacrebleu.corpus_bleu(hyp, [ref])  
    return corpus_bleu.score

def ter_score(hyp,ref):
    ter_scores=[]
    for h,r in zip(hyp,ref):
        s = pyter.ter(h.split(), r.split())
        ter_scores.append(s)
    corpus_ter = np.mean(np.array(ter_scores))
    return corpus_ter

def bert_score(hyp,ref):
    if torch.cuda.is_available():
        Precision, Recall, F1 = score(hyp, ref, lang="others", verbose=True, device=torch.cuda.current_device())
    else:
        Precision, Recall, F1 = score(hyp, ref, lang="others", verbose=True)
    Precision = np.mean(Precision.numpy().tolist())
    Recall = np.mean(Recall.numpy().tolist())
    F1 = np.mean(F1.numpy().tolist())
    return Precision, Recall, F1

def selfbleu_score(hyp):
    self_bleu = 0
    hyp_ = np.array(hyp)
    for idx in range(len(hyp)):
        # [True, True, True, True, False, True, False, True, True, True] を作れば良いという方針
        rev_idx = np.arange(len(hyp))
        bool_idx = np.ones(len(hyp), dtype=bool)
        bool_idx[idx] = False
        rev_idx = rev_idx[bool_idx]
        for rev in rev_idx:
            tmp_score = sacrebleu.sentence_bleu(hyp_[idx], hyp_[rev])
            self_bleu += tmp_score.score
    self_bleu /= len(hyp)*(len(hyp)-1)
    return self_bleu


if __name__ == "__main__":
    multi_preds = [ [0.001, 0.002, 0.003],
                    [0.999, 0.888, 0.777],
                    [0.123, 0.321, 0.213]]
    multi_preds = np.argmax(multi_preds, axis=1)
    multi_labels = np.array([2,1,0])

    
    bi_preds = [[0.001, 0.002],
                [0.999, 0.888],
                [0.123, 0.321]]
    bi_preds = np.argmax(bi_preds, axis=1)
    bi_labels = np.array([1,1,0])

    print(f"Multi: {classification_metrics(multi_preds, multi_labels)}")
    print(f"Binary: {classification_metrics(bi_preds, bi_labels)}")

    
    
    hyp = ["Abcde",
        "Applications of Natural Language Processing in the Real World",
        "As the accuracy of learning has improved and a common language of vectors has been created, an environment has been created in which information from other media (such as images) and language can be handled in an integrated manner in the neural world."]

    ref=["Abcde",
        "Utilization of natural language processing in the real world",
        "With the improvement of learning accuracy and the creation of a common language called vectors, we have created an environment in which information from other media (images, etc.) and language information can be handled in an integrated manner in the neural world."]
    print(f"BLEU: {bleu_score(hyp,ref)}")
    print(f"TER: {ter_score(hyp,ref)}")
    print(f"BERTScore: {bert_score(hyp,ref)}")
    print(f"selfBLEU: {selfbleu_score(hyp)}")




