from rag_chain import ask_question

response = ask_question("Do you ship to India?")

print("\nAnswer:\n")
print(response["answer"])

print("\nSources:\n")
print(response["sources"])