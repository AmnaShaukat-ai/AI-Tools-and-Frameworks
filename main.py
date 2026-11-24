
# ==================================================
# STEP 1: IMPORT LIBRARIES
# ==================================================

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain.tools import tool


# ==================================================
# STEP 2: LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# STEP 3: INITIALIZE AI MODEL
# ==================================================

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# ==================================================
# STEP 4: INITIALIZE EMBEDDING MODEL
# ==================================================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ==================================================
# STEP 5: CREATE RAG PROMPT TEMPLATE
# ==================================================

rag_prompt = ChatPromptTemplate.from_template("""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

If the answer is not available in the context, say you don't have that information.
""")


# ==================================================
# STEP 6: PREPARE KNOWLEDGE DOCUMENTS
# ==================================================

documents = [
    Document(
        page_content="MoinSystems provides AI automation services.",
        metadata={"source": "services.txt", "category": "services"}
    ),

    Document(
        page_content="MoinSystems develops customer support chatbots.",
        metadata={"source": "chatbot.txt", "category": "chatbots"}
    ),

    Document(
        page_content="MoinSystems builds RAG applications using vector databases.",
        metadata={"source": "rag.txt", "category": "RAG"}
    )
]

print("Total documents:", len(documents))


# ==================================================
# STEP 7: GENERATE EMBEDDINGS
# ==================================================

vectors = embeddings.embed_documents(
    [doc.page_content for doc in documents]
)

print("Total Embeddings:", len(vectors))
print("First Vector dimensions:", len(vectors[0]))


# ==================================================
# STEP 8: CREATE CHROMA VECTOR DATABASE
# ==================================================

vector_store = Chroma(
    collection_name="moinsystems_knowledge",
    embedding_function=embeddings
)

vector_store.add_documents(documents)

print("Documents stored successfully!")


# ==================================================
# STEP 9: CREATE RETRIEVER
# ==================================================

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

query = "Does MoinSystems provide web hosting"

results = vector_store._similarity_search_with_relevance_scores(
    query,
    k = 3
)

threshold = 0.5

for doc, scores in results:
    if scores >= threshold:
       print("Accepted",  doc.page_content)
       print("Relevance", scores)

    else:
        print("Rejected", doc.page_content)
        print("Relevance", scores)
    
# ==================================================
# STEP 10: FILTERED RETRIEVER
# ==================================================

def filtered_retriever(query):

    results = vector_store._similarity_search_with_relevance_scores(
        query,
        k = 3
    )
    
    accepted_docs = []

    threshold = 0.5

    for doc, score in results:
        if  score >= threshold:
           accepted_docs.append(doc)
    return accepted_docs
# ==================================================
# STEP 11: RETRIEVE RELEVANT DOCUMENTS
# ==================================================


results = filtered_retriever(query)
print("Accepted Documents :", len(results))

for doc in results:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)


# ==================================================
# STEP 11: CONVERT RETRIEVED DOCUMENTS INTO CONTEXT
# ==================================================

context = "\n".join(
    doc.page_content for doc in results
)

print("Retrieved context:")
print(context)


# ==================================================
# STEP 12: CONNECT RAG COMPONENTS
# ==================================================

parser = StrOutputParser()

answer_chain = (
    rag_prompt
    | model 
    | parser
)

# ==================================================
# STEP 13: GENERATE FINAL ANSWER
# ==================================================

results = filtered_retriever(query)

if len(results) == 0:
    print("Sorry, I couldn't find relevant information in our knowledge base.")
else: 
    context = "\n".join(
    doc.page_content for doc in results
)

response = answer_chain.invoke({ 
    "context" : context,
    "question" : query

})

@tool
def check_order(order_id : int) -> str:

    """Check the delivery status of a customer order."""

    if order_id == 105:
        return "Your order is Shipped"

    else: 
        return "Your Order not Found"


print("Tool name:", check_order.name)
print("Tool description:", check_order.description)
print("Tool arguments:", check_order.args)

result = check_order.invoke({"order_id" : 105})
print("Tool Result :", result)


# ==================================================
# STEP 14: SEARCH PRODUCTS
# ==================================================

@tool

def search_product(product_name : str) -> str:
    """ Serach for a product in the Store"""

    if product_name.lower() == "laptop":
       return "Laptop is available"

    else: 
        return "The product not found"

tools = [check_order, search_product]
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke(
    "Where is my order 105?"
)

print(response)

tool_call = response.tool_calls[0]
tool_result = check_order.invoke(
    tool_call["args"]
)

print("Tool result:", tool_result)

tool_message = ToolMessage(
    content = tool_result,
    tool_call_id = tool_call["id"]
)

final_response = model_with_tools.invoke([
    response,
    tool_message
])

print("Final AI Response :")
print(final_response.content)


agent = create_agent(
    model,
    tools = [check_order, search_product],
    system_prompt= "You are a customer support assistant. Use tools when needed"
)

result = agent.invoke({
    "messages" : [{"role" : "user", "content" : "Check my order 105 and also tell me if a laptop is available"}

]
                       
})

print("\nAgent Response: ")
print(result["messages"][-1].content)