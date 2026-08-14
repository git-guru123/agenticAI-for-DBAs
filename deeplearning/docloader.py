import os
import openai
import sys
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_community.document_loaders import PyPDFLoader

###loading PDf'S ####
loader = PyPDFLoader("deeplearning/docs/ml-overview_notes.pdf")
pages = loader.load()
print(loader.headers)
#print(pages.metadata)
length = len(pages)
# print(length)

#####Loading from Youtube audio ##
##this is not working but getting error yt_dlp.utils.DownloadError: ERROR: Postprocessing: ffprobe and ffmpeg not found. Please install or provide the path using --ffmpeg-location
# url="https://www.youtube.com/watch?v=4pUYfY-b5CQ"
# save_dir="deeplearning/docs/youtube"
# loader = GenericLoader(
#     YoutubeAudioLoader([url],save_dir),
#     OpenAIWhisperParser()
# )
# docs = loader.load()

####web base loader
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://github.com/basecamp/once-campfire/blob/main/SECURITY.md")
docs = loader.load()
# print(docs[0].page_content[:500])


###loadint data from NotionDb
os.environ["USER_AGENT"] = "MyFoodApp/1.0 (contact@example.com)"
from langchain_community.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("deeplearning/docs/NotionDB")
docs1 = loader.load()
#print(docs1[0].page_content[0:200])
print(docs1)










