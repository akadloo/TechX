import requests
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO

def open_link(url):
    webbrowser.open_new(url)

def getNews():
    api_key = "f6194e21b77a4719ae627675582bc833"
    url = "https://newsapi.org/v2/everything?q=apple&apiKey=" + api_key
    news = requests.get(url).json()

    articles = news["articles"]

    text_frame.config(state="normal")
    text_frame.delete(1.0, "end")

    for i, article in enumerate(articles[:10], 1):
        title = article["title"]
        source = article["source"]["name"].rstrip(".com")
        url = article["url"]
        image_url = article["urlToImage"]
        
        # Download the image and create an ImageTk.PhotoImage object
        response = requests.get(image_url)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        image = image.resize((100, 100))
        image = ImageTk.PhotoImage(image)
        
        # Insert the image and text into the text_frame
        text_frame.image_create("end", image=image)
        text_frame.insert("end", f"\n{i}. {title} - {source}\n", f"link_{i}")
        text_frame.tag_bind(f"link_{i}", "<Button-1>", lambda e, link=url: open_link(link))
        text_frame.tag_bind(f"link_{i}", "<Enter>", lambda e, tag=f"link_{i}": text_frame.tag_configure(tag, foreground="blue"))
        text_frame.tag_bind(f"link_{i}", "<Leave>", lambda e, tag=f"link_{i}": text_frame.tag_configure(tag, foreground="black"))

    text_frame.config(state="disabled")

canvas = tk.Tk()
canvas.geometry("800x600")
canvas.title("Modern News App")

frame = ttk.Frame(canvas, padding="20")
frame.pack(expand=True, fill="both")

title_label = ttk.Label(frame, text="TechX", font=("Unique", 24), foreground="#333")
title_label.pack(pady=10)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

button = ttk.Button(button_frame, text="Reload", command=getNews)
button.pack(pady=5)

canvas_scroll = tk.Scrollbar(frame, orient="vertical")
canvas_scroll.pack(side="right", fill="y")

text_frame = tk.Text(frame, font=("Unique", 16), wrap="word", bg="#D3D3D3", highlightthickness=0, padx=10, pady=10, yscrollcommand=canvas_scroll.set)
text_frame.pack(expand=True, fill="both", pady=20)

canvas_scroll.config(command=text_frame.yview)

getNews()

canvas.mainloop()
