
from pynput.mouse import Listener
from dotenv import load_dotenv
from PIL import ImageGrab
import pytesseract
import openai
import os

load_dotenv()

GPT_KEY = os.getenv("GPT_KEY")

openai.api_key = GPT_KEY

points = []
image_counter = 0
max_images = 1  

initial_instructions = input("Digite as instruções iniciais: ")

def print_divider():
    print("-" * 50)  # Adiciona uma linha divisória no console

def on_click(x, y, button, pressed):
    global points, image_counter

    if pressed:
        points.append((x, y))
        if len(points) == 2:
            image_counter += 1
            point_a, point_b = points
            left = min(point_a[0], point_b[0])
            top = min(point_a[1], point_b[1])
            right = max(point_a[0], point_b[0])
            bottom = max(point_a[1], point_b[1])

            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            output_filename = f"captured_region_{image_counter}.png"
            screenshot.save(output_filename)
            print_divider()
            print(f"Região capturada e salva como '{output_filename}'.")
            
            extracted_text = pytesseract.image_to_string(screenshot)
            print_divider()
            print("Texto extraído da imagem:")
            print(extracted_text)

            combined_text = initial_instructions + " " + extracted_text
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=combined_text,
                max_tokens=500  
            )
            chat_response = response.choices[0].text
            print_divider()
            print("Resposta do ChatGPT:")
            print(chat_response)

            listener.stop()

with Listener(on_click=on_click) as listener:
    print("Clique em dois pontos para selecionar uma área de recorte. O programa encerrará após 1 captura.")
    listener.join()
