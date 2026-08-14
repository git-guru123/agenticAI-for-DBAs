import os
import openai
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
load_dotenv()

loaders = [
    ##duplicate document on purpose
    PyPDFLoader("deeplearning/docs/MachineLearning-Lecture01.pdf"),
    PyPDFLoader("deeplearning/docs/MachineLearning-Lecture01.pdf"),
    PyPDFLoader("deeplearning/docs/MachineLearning-Lecture02.pdf"),
    PyPDFLoader("deeplearning/docs/MachineLearning-Lecture03.pdf")
]
docs = []
for loader in loaders:
    docs.extend(loader.load())
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)
splits = text_splitter.split_documents(docs)
print(len(splits))
###numpy to check dot product between embeddings. dotproduct is from 0 to 1. 
###lower the score lesser the similarity.
from langchain_community.embeddings.openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()
sentence1 = "i like dogs"
sentence2 = "i like canines"
sentence3 = "the weather is ugly outside"
embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)
import numpy as np
# print(np.dot(embedding1,embedding2))
# print(np.dot(embedding2,embedding3))
# print(np.dot(embedding1,embedding3))

from langchain_community import Chroma
persist_directory = 'deeplearning/docs/chroma'
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)
print(vectordb.collection.count)

##Chroma DB
from langchain_community.embeddings import Chroma










