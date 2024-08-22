# # gradio_frontend.py

# import gradio as gr
# import requests

# # FastAPI backend URL
# API_URL = "http://localhost:8000"

# def generate_text(input_text, max_length):
#     try:
#         # Make a POST request to the FastAPI backend
#         response = requests.post(
#             f"{API_URL}/generate",
#             json={"text": input_text, "max_length": max_length}
#         )
        
#         # Check if the request was successful
#         response.raise_for_status()
        
#         # Extract the generated text from the response
#         result = response.json()["generated_text"]
#         return result
#     except requests.RequestException as e:
#         return f"Error: Unable to connect to the backend. {str(e)}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Create Gradio interface
# iface = gr.Interface(
#     fn=generate_text,
#     inputs=[
#         gr.Textbox(label="Input Text"),
#         gr.Slider(minimum=10, maximum=500, step=10, label="Max Length", value=100)
#     ],
#     outputs=gr.Textbox(label="Generated Text"),
#     title="Text Generation Chatbot",
#     description="Enter some text and the model will generate a continuation."
# )

# Launch the Gradio interface
# iface.launch()

import gradio as gr
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"
# def generate_response(message, history):
#     try:
#         # Combine the current message with the last message from history for context
#         context = history[-1][1] + " " + message if history else message
        
#         # Make a POST request to the FastAPI backend
#         response = requests.post(
#             f"{API_URL}/generate",
#             json={"text": context, "max_length": 150}  # Adjust max_length as needed
#         )
        
#         # Check if the request was successful
#         response.raise_for_status()
        
#         # Extract the generated text from the response
#         result = response.json()["generated_text"]
        
#         # Return only the newly generated part
#         return result[len(context):].strip()
#     except requests.RequestException as e:
#         return f"Error: Unable to connect to the backend. {str(e)}"
#     except Exception as e:
#         return f"Error: {str(e)}"

def generate_response(input_text, max_length=100):
    try:
        # Make a POST request to the FastAPI backend
        response = requests.post(
            f"{API_URL}/generate",
            json={"text": input_text, "max_length": max_length}
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Extract the generated text from the response
        result = response.json()["generated_text"]
        return result
    except requests.RequestException as e:
        return f"Error: Unable to connect to the backend. {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface with components
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Conversation")
    msg = gr.Textbox(label="Type your message here")
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        user_message = history[-1][0]
        # bot_message = generate_response(user_message, history[:-1])\
        bot_message = generate_response(user_message, 100)
        history[-1][1] = bot_message
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch()