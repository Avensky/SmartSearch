from llama_cpp import Llama
# from llama_cpp import LlamaTokenizer

# tokenizer = LlamaTokenizer()
# max_context_tokens = 1500  # or however many your model supports minus generation space
# context_tokens = tokenizer.encode(context)

# if len(context_tokens) > max_context_tokens:
#     context_tokens = context_tokens[:max_context_tokens]
#     context = tokenizer.decode(context_tokens)
    
# Load the GGUF model (adjust path as needed)

llm = Llama(
    model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8  # Adjust based on your CPU
)
# Final Step: Replace Your LLM
# llm = Llama(model_path="./models/custom-trained-model.gguf", n_ctx=2048)


def ask_llm(context: str, question: str) -> str:
    prompt = f"""[INST] Use the following context to answer the question.

Context:
{context}

Question:
{question}
[/INST]"""

    # Truncate prompt if it exceeds token window
    max_total_tokens = 2048
    max_response_tokens = 512
    max_prompt_tokens = max_total_tokens - max_response_tokens

    # Estimate token length (assumes ~4 characters per token, conservative)
    if len(prompt) > max_prompt_tokens * 4:
        prompt = prompt[:max_prompt_tokens * 4]

    # Generate completion
    response = llm(
        prompt,
        max_tokens=max_response_tokens,
        stop=["</s>", "Question:", "Context:"]
    )
    response = llm(prompt, max_tokens=1024, stop=["</s>"])
    return response["choices"][0]["text"].strip()
