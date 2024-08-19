from openai import OpenAI

client = OpenAI(
    api_key="fake-api-key",
    base_url="http://127.0.0.1:8000",
)

chat_stream = client.chat.completions.create(
    model="mock-gpt-model",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chat_chunk in chat_stream:
    print(chat_chunk.choices[0].delta.content or "")

chat_completion = client.chat.completions.create(
    model="mock-gpt-model",
    messages=[{"role": "user", "content": "Say this is a test"}],
)
print(chat_completion.choices[0].message.content)

stream = client.completions.create(
    model="mock-gpt-model",
    prompt="Say this is a test",
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].text or "")

completion = client.completions.create(
    model="mock-gpt-model",
    prompt="Say this is a test",
)
print(completion.choices[0].text)
