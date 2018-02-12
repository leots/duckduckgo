import duckduckgo

results = duckduckgo.search('test', max_results=2)
for res in results:
    print(res)
