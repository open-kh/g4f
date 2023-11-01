import json
from pydoc import doc
from g4f import ChatCompletion, models, Provider
from perplexity import Perplexity
import time
# from ...g4f.Provider.perplexity import Perplexity

ai = Perplexity()

question = "Do you have boyfriend with girlfriend together"

# doct = ""
# docs = []
# for res in ai.search(question):
#     response = eval(f"{res}")
#     text = ""
#     if ('text' in response) and ('answer' not in response):
#         response["answer"] = response['text']
#         docs.append(response["answer"])

#     if 'answer' in response:
#         text = response['answer']
#         docs.append(text)
#     elif 'chunks' in response:
#         text = "".join(response['chunks'])
#         docs.append(text)
#     else:
#         break
#         docs.append(response)
#         # print(response)
#         print(docs)

#     print(text[len(doct):])
#     doct = text


for response in ChatCompletion.create(
                                model='concise',
                                provider= Provider.PerplexityAI,
                                messages=[{"role": "user", "content": question}],
                                temperature=0.1,
                                stream=True
                            ):
    # doc_len = len(doc["chunks"])
    # content = "".join(doc["chunks"][-(doc_len-count):] if doc_len > count else doc["chunks"])
    print(response, end="", flush=True)
    # count = doc_len
    time.sleep(0.1)

    # if doc["status"] is "completed":
    #     data = {
    #         "status": doc.status,
    #         "uuid": doc.uuid,
    #         "media_items": doc.media_items,
    #         "query_str": doc.query_str,
    #     }
    #     print(json.dumps(a, separators=(',', ':')))
# print(json.dumps(doct))
ai.close()
# perplexity.close()