import os

import gradio as gr
from llama_index.core import load_index_from_storage, PromptTemplate, StorageContext
from llama_index.core.agent import ReActAgent
from llama_index.core.agent.workflow import AgentStream, ToolCallResult
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI


USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not (USERNAME and PASSWORD):
    raise Exception("Missing USERNAME and/or PASSWORD environment variable(s).")

with open("./app/prompts/tool_metadata.md", encoding="utf-8") as tool_metadata_file:
    llm = GoogleGenAI("gemini-2.5-flash")

    agent = ReActAgent(
        tools=[
            QueryEngineTool(
                load_index_from_storage(
                    StorageContext.from_defaults(persist_dir="./app/index"),
                    embed_model=GoogleGenAIEmbedding(),
                ).as_query_engine(llm, similarity_top_k=4),
                ToolMetadata(tool_metadata_file.read(), "index"),
            )
        ],
        llm=llm,
    )

with open("./app/prompts/prompt_template.md", encoding="utf-8") as prompt_template_file:
    agent.update_prompts(
        {
            "react_header": PromptTemplate(
                f"{prompt_template_file.read()}\n{agent.get_prompts()['react_header'].get_template()}"
            )
        }
    )


async def _chat(message: str, history: list[dict[str, str | None]]) -> str:
    handler = agent.run(
        message,
        [ChatMessage(message["content"], role=message["role"]) for message in history],
    )

    print("=" * 192)

    async for event in handler.stream_events():
        if isinstance(event, AgentStream):
            print(event.delta, end="", flush=True)
        elif isinstance(event, ToolCallResult):
            print(f"\nTool Call Result: {event.tool_output}")

    print()

    return str(await handler)


async def chat(message: str, history: list[dict[str, str | None]]) -> str:
    try:
        return await _chat(message, history)
    except Exception as exception:
        print("=" * 192, exception, sep="\n")

        return "Error."


chat_interface = gr.ChatInterface(
    chat,
    type="messages",
    title="Aqui é o Alfred, faça suas perguntas!",
    save_history=True,
)
chat_interface.saved_conversations.secret = "secret"
chat_interface.launch(auth=(USERNAME, PASSWORD))
