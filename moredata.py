import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
from collections import Counter
import random
import csv

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("gutenberg")

def load_data(filename):
  data = open(filename, "r+")
doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]


stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]    

def map(clean_doc, num_topics):
  topic_map = []
  for doc in clean_doc:
    topic_map.append([])
    for word in doc:
      assignment = random.randint(1, num_topics)
      topic_map[-1].append((word, assignment))
  return topic_map

def t_given_d(doc_map, t):
  t_count = 0
  for word, assignment in doc_map:
    if assignment == t:
      t_count += 1
  final = t_count/len(doc_map)
  return final

def w_given_t(word, topic_map, t):
  words_assigned_to_topic_t = []
  for doc_map in topic_map:
    for item, assignment in doc_map:
      if assignment == t:
        words_assigned_to_topic_t.append(item)
  if(words_assigned_to_topic_t) == []:
    return 0
  t_count = words_assigned_to_topic_t.count(word)
  final = t_count/len(words_assigned_to_topic_t)
  return final

def topic_prob(word, doc_map, topic_map, topic):
  return w_given_t(word, topic_map, topic) * t_given_d(doc_map, topic)

def update(topic_map, num_topics):
  for doc_map in topic_map:
    idx = 0
    for word, assignment in doc_map:
      topic = assignment
      max_topic_prob = 0
      for i in range(1, num_topics + 1):
        prob = topic_prob(word, doc_map, topic_map, i)
        if prob > max_topic_prob:
          max_topic_prob = prob
          topic = i
      doc_map[idx] = (word, topic)
      idx += 1

def output(topic_map, num_topics):
  tuple_list = []
  for doc_map in topic_map:
    for i in range(len(doc_map)):
      tuple_list.append(doc_map[i])
  grouped_by_topic = []
  for topic in range(1, num_topics + 1):
    grouped_by_topic.append([word for word, assignment in tuple_list if assignment == topic])
  topic_breakdowns = []
  for topic in range(1, num_topics+1):
    topic_breakdowns.append(Counter([word for word in grouped_by_topic[topic - 1]]))
  for i in range(len(topic_breakdowns)):
    total = sum(topic_breakdowns[i].values())
    for j in topic_breakdowns[i].keys():
      topic_breakdowns[i][j] = 100 * topic_breakdowns[i][j]/total
  for i in range(len(topic_breakdowns)):
    topic_breakdowns[i] = sorted(topic_breakdowns[i].items(), key = lambda tup: tup[1], reverse=True)
  output = ""
  for topic in range(1, num_topics + 1):
    output += "Topic " + str(topic) +  ": "
    for word, percentage in topic_breakdowns[topic - 1]:
      output += str(round(percentage, 2)) + "% " + word + ", "
    output += "\n"
  return output

def lda(doc_clean, num_topics, passes):
  topic_map = map(doc_clean, num_topics)
  print("random topic map: " + repr(topic_map))
  for i in range(passes):
    update(topic_map, num_topics)
  print("final topic map: " + repr(topic_map))
  
  return output(topic_map, num_topics)

passes = 50
topics = 3 
print(lda(doc_clean, topics, passes))