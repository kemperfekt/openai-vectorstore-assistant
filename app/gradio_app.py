import gradio as gr
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "DEIN_API_KEY")

VECTOR_STORE_ID = "DEINE_VECTOR_STORE_ID"
ASSISTANT_ID = "DEINE_ASSISTANT_ID"

def init_thread():
    return openai.beta.threads.create()

thread = init_thread()

def frage_beantworten(user_input):
    try:
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
        )
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "Keine Antwort erhalten 😕"
    except Exception as e:
        return f"❌ Fehler: {str(e)}"

with gr.Blocks(title="Dokumenten-Assistent") as demo:
    gr.Markdown("# 🤖 Dokumenten-Assistent")
    gr.Markdown("Stelle Fragen zu deinen hochgeladenen Dateien.")
    chat = gr.ChatInterface(fn=frage_beantworten)

demo.launch()
