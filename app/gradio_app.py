import gradio as gr
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "DEIN_API_KEY")

VECTOR_STORE_ID = "DEINE_VECTOR_STORE_ID"
ASSISTANT_ID = "DEINE_ASSISTANT_ID"

def init_thread():
    return openai.beta.threads.create()

thread = init_thread()

def frage_beantworten(user_input, history):
    try:
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id="asst_gD8e064WP15q6ks3inNaDtW2",
        )
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "Keine Antwort erhalten 😕"
    except Exception as e:
        return f"❌ Fehler: {str(e)}"


with gr.Blocks(title="Nasenblick-KI") as demo:
    gr.Markdown("# 🤖 Nasenblick-KI")
    gr.Markdown("Stelle Fragen zur Erziehung deines Hundes.")
    chat = gr.ChatInterface(fn=frage_beantworten)

demo.launch()
