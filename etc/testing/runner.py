import json
from g4f.Provider import (PerplexityAI)

perplexity = PerplexityAI()
question = "Hello, What is your name"
answer = perplexity.search(question)
count = 0
for doc in answer:
    print(doc)
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

perplexity.close()