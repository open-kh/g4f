import json
from g4f import ChatCompletion, models, Provider

question = "Hello, How are you?"
for response in ChatCompletion.create(
                                    model='concise',
                                    provider= Provider.PerplexityAI,
                                    messages=[{"role": "user", "content": question}],
                                    temperature=0.1,
                                    stream=True
                                ):
    print(response, end="", flush=True)
    # doc_len = len(doc["chunks"])
    # content = "".join(doc["chunks"][-(doc_len-count):] if doc_len > count else doc["chunks"])
    # count = doc_len
    # if doc["status"] is "completed":
        # data = {
        #     "status": doc.status,
        #     "uuid": doc.uuid,
        #     "media_items": doc.media_items,
        #     "query_str": doc.query_str,
        # }
        # print(json.dumps(a, separators=(',', ':')))

# perplexity.close()