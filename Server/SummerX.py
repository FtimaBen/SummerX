from nltk.tokenize import RegexpTokenizer
from langchain.llms import OpenAI
from nltk.stem import PorterStemmer

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

import requests

class SummerizX():
  #model parameters
  temperature = 0
  chain_type = 'stuff'
  reviews = None

  def __init__(self, reviews, openai_api_key='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'):
    self.openai_api_key = openai_api_key
    self.reviews = reviews

  def summerize(self):
    if self.reviews == None:
      return

    self.reviewsProcessing()

    return self.generateSummary()

  ###########################################
  # text precessing:
  # remove stop words
  # remove punctuations
  # stemming
  ###########################################
  def reviewsProcessing(self):
    with open("corpora/stopwords/english", 'r') as words:
        stop_words = words.read()
        words.close()

        tokenizer = RegexpTokenizer(r'\w+')

        #remove punctions and tokenize
        self.reviews = [tokenizer.tokenize(review) for review in self.reviews]

        #remove stop words and stem
        st = PorterStemmer()
        self.reviews = [[st.stem(word.lower()) for word in review if word.lower() not in stop_words] for review in self.reviews]

  ###########################################
  # generate sentences from a list of words
  ###########################################
  def generateSummary(self):

    llm = OpenAI(openai_api_key=self.openai_api_key, temperature=self.temperature)
    docs = [Document(page_content=' '.join(s for s in t)) for t in self.reviews]
    summarize = load_summarize_chain(llm, chain_type=self.chain_type).run(docs)

    return summarize