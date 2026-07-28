##for laod environments from .env file
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

# response = client.responses.create(
#     model="gpt-4.1",
#     input="Hi My name is Guru and I like river rafting",
# )
print("---Exmaple1 current events ---")
response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search"}],
    input="Who won the FIFA World cup in the year 2026?"
)
print(response.output_text)

print("---Exmaple2 current events ---")
response1 = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search"}],
    input="how do i make chicken 65"
)
print(response1.output_text)


# response1 = client.responses.create(
#     model="gpt-4.1",
#     input="what is my name and what do i like",
#     previous_response_id=response.id,
# )

##print(response.output_text)
#print(f"Assistant:{response.output_text}")
# print(f"Assistant:{response1.output_text}")







