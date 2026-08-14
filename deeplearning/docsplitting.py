import os
import openai
import sys
from dotenv import load_dotenv
load_dotenv()
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
chunk_size = 26
chunk_overlap = 4
r_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,)
c_splitter = CharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)

text1 = 'abcdefghijklmnopqrstuvwxyz'

# print(r_splitter.split_text(text1))
# print(c_splitter.split_text(text1))

text2 = 'abcdefghijklmnopqrstuvwxyzabcdefghinkkwlmnfo'
# print(r_splitter.split_text(text2))
# print(c_splitter.split_text(text2))

##
text3 = ' a b c d e f g h i j k l m n o p q r s t u v w x y z '
r_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
c_splitter = CharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
# print(r_splitter.split_text(text3))
# print(c_splitter.split_text(text3))
docs = CharacterTextSplitter.split_documents

text4="""Core Experience and Technical Expertise:


With over 20 years of experience as a Database Engineer, I specialize in the design, construction, and operation of 

large-scale, mission-critical database platforms. My technical foundation is rooted in RDBMS internals—specifically 

PostgreSQL, Oracle, and MySQL—with deep expertise in replication protocols, query optimization, Write-Ahead Logging (WAL),

and index access methods. My proficiency extends across a diverse ecosystem comprising NoSQL and Graph databases like 

Neo4J and MongoDB, as well as cloud-native solutions such as CosmosDB, Synapse Analytics, and BigQuery. Beyond core 

database management, I have successfully expanded into software engineering, building scalable backend services and multi-cloud PostgreSQL clusters using CloudNativePG on OpenShift and Kubernetes, complemented by robust data visualization and monitoring platforms like Grafana.

Current Focus and AI Integration:


Currently, my work is centered at the intersection of database architecture and Generative AI. I am primarily focused on
building production-grade Retrieval-Augmented Generation (RAG) pipelines and developing autonomous AI agents using the 
Agents SDK, Langchain frameworks, and MCP integrations across various data sources. A significant portion of my daily
operations involves optimizing RAG performance through hybrid search strategies and embedding refinements to reduce 
token consumption and operational costs. I am also gaining extensive production experience in deploying and managing vector databases at scale, including Pinecone, ChromaDB, and PostgreSQL Vector, ensuring these systems power reliable,enterprise-grade AI automation platforms. """


# print(len(text4))
c_splitter = CharacterTextSplitter(chunk_size=450, chunk_overlap=0,separator='')
r_splitter = RecursiveCharacterTextSplitter(chunk_size=150,chunk_overlap=0,separators=".")

##

#print(c_splitter.split_text(text4))
#print(r_splitter.split_text(text4))

#######token splitter

text_splitter = TokenTextSplitter(chunk_size=1,chunk_overlap=0)
text5 = "foo bar bazzyfoo"
# print(text_splitter.split_text(text5))

##prints metadata of the document. 
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("deeplearning/docs/ml-overview_notes.pdf")
pages = loader.load()
docs = text_splitter.split_documents(pages)
# print(docs[0])
print(pages[0].metadata)

#####markdown head splitter to adding more content to the metadata
from langchain_text_splitters import MarkdownHeaderTextSplitter
markdown_document = """#Title\n\n \
##Chapter 1 \n\n \
Hi This is guru  \n\n
##Chapter 2\n\n \
Hi This is Molly"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


