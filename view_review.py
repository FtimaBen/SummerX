from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

import requests
import json

class SummerizX():
  #model parameters 
  temperature = 0.2
  chain_type = 'stuff'

  def __init__(self, url, openai_api_key='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', rainforest_api_key='C85C514238954FCA9F8E5510D1DED6A5'):
    self.url = url
    self.openai_api_key = openai_api_key
    self.rainforest_api_key = rainforest_api_key
  
  def summerize(self):
    reviews, product = self.loadAmazonReviews()
    reviews, reviews_2 = self.reviewsProcessing(reviews)
    summary_1, summary_2 = self.generateSummary(reviews, reviews_2)

    return product, summary_1, summary_2

  ###########################################
  #load the reviews using the rainforest api
  ###########################################
  def loadAmazonReviews(self):
    # set up the request parameters
    params = {
      'api_key': self.rainforest_api_key,
      'type': 'reviews',
      'url': self.url
    }

    # make the http GET request to Rainforest API
    api_result = requests.get('https://api.rainforestapi.com/request', params)

    #review object
    reviews = api_result.json()

    return reviews.get('reviews'), reviews.get('product').get('title')

  ###########################################
  # text precessing: 
  # remove stop words
  # remove punctuations
  # stemming
  ###########################################
  def reviewsProcessing(self, reviews):

    #keep only the reviews body
    reviews_2 = reviews = [review.get('body') for review in reviews]

    with open("corpora/stopwords/english", 'r') as words:
        stop_words = words.read()
        words.close()

        tokenizer = RegexpTokenizer(r'\w+')

        #remove punctions and tokenize
        reviews = [tokenizer.tokenize(review) for review in reviews]

        #remove stop words and stem
        st = PorterStemmer()
        reviews = [[st.stem(word.lower()) for word in review if word.lower() not in stop_words] for review in reviews]

        return reviews, reviews_2


  ###########################################
  # generate sentences from a list of words
  ###########################################
  def generateSummary(self, reviews, reviews_2):
    llm = OpenAI(openai_api_key=self.openai_api_key, temperature=self.temperature)

    docs_1 = [Document(page_content=' '.join(s for s in t)) for t in reviews]
    docs_2 = [Document(page_content=' '.join(s for s in t)) for t in reviews_2]

    summarize_1 = load_summarize_chain(llm, chain_type=self.chain_type).run(docs_1)
    summarize_2 = load_summarize_chain(llm, chain_type=self.chain_type).run(docs_2)

    return summarize_1, summarize_2
