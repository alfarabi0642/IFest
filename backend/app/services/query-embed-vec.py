from openai import AzureOpenAI

deployment = "text-embedding-3-large"
client = AzureOpenAI(
    api_key="47bYCKK9oQRkv9c9o6SaOHvKlRF3g0bqM1CO1DrWthtjVYpymjksJQQJ99BIACHYHv6XJ3w3AAAAACOGVQy1",
    api_version="2023-05-15",
    azure_endpoint="https://embbedder-resource.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
)

def get_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        input=text,
        model=deployment
    )
    
    return response.data[0].embedding

