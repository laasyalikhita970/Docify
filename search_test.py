from search import search_documents

keyword = input("Enter keyword to search: ")

results = search_documents(keyword)

print("\nSearch Results:\n")

for r in results:
    print("File:", r[0])
    print("Content:", r[1][:200])  # first 200 chars
    print("-" * 40)