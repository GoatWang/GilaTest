from collections import Counter
import math
import operator

def ngram_probs(filename='raw_sentences.txt'):
    bigram = []
    trigram = []
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            texts = [t.lower() for t in line.split()]
            for i in range(len(texts)-1):
                bigram.append("#$".join(texts[i:i+2]))
            for i in range(len(texts)-2):
                trigram.append("#$".join(texts[i:i+3]))

    bigram_probs = dict([(tuple(i.split("#$")), v) for i, v in dict(Counter(bigram)).items()])
    trigram_probs = dict([(tuple(i.split("#$")), v) for i, v in dict(Counter(trigram)).items()])
    return bigram_probs, trigram_probs
cnt2, cnt3 = ngram_probs()
print(cnt2[('we', 'are')])

def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    cnt2_sum = sum(cnt2.values())
    cnt3_sum = sum(cnt3.values())
    cnt2_prob = cnt2[bigram]/cnt2_sum

    prob = {}
    for i, v in cnt3.items():
        if i[0] == bigram[0] and i[1] == bigram[1]:
            prob[i[2]] = math.log((v/cnt3_sum)/cnt2_prob)
    
    return prob
p = prob3(('we', 'are'))
print(p['family'])


def predict_max(starting, cnt2=cnt2, cnt3=cnt3):
    list_of_words = list(starting)
    while len(list_of_words) < 15 and list_of_words[-1] != '.':
        curent_prob3 = prob3(tuple(list_of_words[-2:]))
        next_word = max(curent_prob3.items(), key=operator.itemgetter(1))[0]
        list_of_words.append(next_word)
    return list_of_words

sent = predict_max(('we', 'are'))
assert sent[-1] == '.' or len(sent) <= 15
print(' '.join(sent))


# def predict_top_beam_size(beam_size, bigram):
#     curent_prob3 = prob3(tuple(bigram))
#     sorted_prob3 = sorted(curent_prob3.items(), key=operator.itemgetter(1), reverse=True)[:beam_size]
#     return [t for t, v in sorted_prob3]


# def next_predict():


# def predict_beam(bigram, beam_size=4, sent_length=10, cnt2=cnt2, cnt3=cnt3):
#     list_of_words = list(bigram)
#     while len(list_of_words) < 15 and list_of_words[-1] != '.':
#         curent_prob3 = prob3(tuple(list_of_words[-2:]))
#         predict_top_beam_size

#         list_of_words.append(next_word)
#     return list_of_sentence

# for sent in predict_beam(('we', 'are')):
#     assert sent[-1] == '.' or len(sent) <10:
#     print(' '.join(sent))
