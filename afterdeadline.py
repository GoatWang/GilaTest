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


def predict_top_beam_size(beam_size, bigram):
    curent_prob3 = prob3(tuple(bigram))
    sorted_prob3 = sorted(curent_prob3.items(), key=operator.itemgetter(1), reverse=True)[:beam_size+1]
    return [t for t, v in sorted_prob3]


file = open("test.txt", 'w', encoding='utf8')

def predict_beam(bigram, beam_size=4, sent_length=10, cnt2=cnt2, cnt3=cnt3):
# def predict_beam(bigram, beam_size=4, sent_length=7, cnt2=cnt2, cnt3=cnt3):
    layers_cnt = 0
    current_layer_bigrams = [bigram]
    current_sents_dict = {}
    current_sents_dict[bigram] = list(bigram)
    final_sents = []

    while len(current_layer_bigrams) != 0 and layers_cnt <= sent_length-3:
        print(layers_cnt)
        next_layer_bigrams = []
        next_sents_dict = {}        
        for bigram in current_layer_bigrams:
            current_sents = current_sents_dict[bigram]
            # print(layers_cnt, len(current_sents), bigram, current_sents)
            file.write(str(layers_cnt) + " " + str(len(current_sents)) + " " + str(bigram) + " " + str(current_sents) + "\n")

            current_predicted_terms = predict_top_beam_size(beam_size, tuple(bigram))
            if layers_cnt < sent_length-3:
                for term in current_predicted_terms:
                    next_bigram = (bigram[1], term)
                    next_sent = current_sents + [term]
                    if term != '.':
                        next_layer_bigrams.append(next_bigram)        
                        next_sents_dict[next_bigram] = next_sent
                    else:
                        final_sents.append(next_sent) 
            else:
                final_sents.append(current_sents) 

        current_layer_bigrams = next_layer_bigrams
        current_sents_dict = next_sents_dict
        layers_cnt += 1
    return final_sents


file.write("----------------" + "\n")
file.write("----------------" + "\n")
file.write("----------------" + "\n")
file.write("----------------" + "\n")
file.write("----------------" + "\n")

for sent in predict_beam(('we', 'are')):
    assert sent[-1] == '.' or len(sent) <10
    print(' '.join(sent))
    file.write(' '.join(sent) + "\n")


file.close()