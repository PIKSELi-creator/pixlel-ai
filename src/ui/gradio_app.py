import gradio as gr
from src.brain.agent import PixlelAgent

agent = PixlelAgent()

def chat(message, history):
    response = agent.invoke(message)
    return response

def launch_ui():
    with gr.Blocks(title="Pixlel AI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🧠 Pixlel AI\n**Думает сам как человек**")
        chatbot = gr.Chatbot(height=600)
        msg = gr.Textbox(placeholder="Спроси меня о чём угодно...", label="Сообщение")
        
        msg.submit(chat, [msg, chatbot], [chatbot, msg])
    
    demo.launch(share=False)