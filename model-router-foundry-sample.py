import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

user_messages = [
    "Capital of West Bengal?",
    "Implement a lock-free queue in Rust.",
    #"Use a embedding model and convert cat into its vector equivalent",
    #"Solve the differential equation dy/dx + 2xy = x, given y(0) = 0. Provide the solution in terms of the error function if necessary.",
    "2*409237252425267829083018031801380913013813-99",
    ""
]

for user_content in user_messages:
    response = client.chat.completions.create(
        stream=True,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": user_content,
            }
        ],
        max_tokens=10000,
        # temperature=0.7,
        # top_p=0.95,
        # frequency_penalty=0.0,
        # presence_penalty=0.0,
        model=deployment,
    )

    model_router_model = None
    for update in response:
        if update.choices:
            print(update.choices[0].delta.content or "", end="")
            if update.model:
                model_router_model = update.model

    print(f"\nmodel used by Model Router: {model_router_model}\n")

client.close()