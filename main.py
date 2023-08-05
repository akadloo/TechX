
import requests
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk


def open_link(url):
    webbrowser.open_new(url)

from io import BytesIO


def getNews():
    global search_query
    api_key = "f6194e21b77a4719ae627675582bc833"
    
    # Check if the search_query is not empty
    if not search_query:
        text_frame.config(state="normal")
        text_frame.delete(1.0, "end")
        text_frame.insert("end", "Please enter a search query.")
        text_frame.config(state="disabled")
        return
    
    url = f"https://newsapi.org/v2/everything?q={search_query}&apiKey=" + api_key
    news = requests.get(url).json()

    articles = news.get("articles", [])

    text_frame.config(state="normal")
    text_frame.delete(1.0, "end")

    for i, article in enumerate(articles[:10], 1):
        title = article["title"]
        source = article["source"]["name"].rstrip(".com")
        url = article["url"]

        text_frame.insert("end", f"\n{i}. {title} - {source}\n", f"link_{i}")
        text_frame.insert("end", "   ")
        text_frame.tag_configure(f"link_{i}", font=("Helvetica", 16, "bold"))
        text_frame.tag_bind(f"link_{i}", "<Button-1>", lambda e, link=url: open_link(link))
        text_frame.tag_bind(f"link_{i}", "<Enter>", lambda e, tag=f"link_{i}": text_frame.tag_configure(tag, foreground="blue"))
        text_frame.tag_bind(f"link_{i}", "<Leave>", lambda e, tag=f"link_{i}": text_frame.tag_configure(tag, foreground="black"))

        text_frame.insert("end", "\n\n")

    text_frame.config(state="disabled")

def on_search_query_change(event):
    global search_query
    search_query = search_entry.get()

canvas = tk.Tk()
canvas.geometry("800x600")
canvas.title("Modern News App")

frame = ttk.Frame(canvas, padding="5")
frame.pack(expand=True, fill="both")

title_label = ttk.Label(frame, text="TechX Top 10", font=("Unique", 24), foreground="#333")
title_label.pack(pady=10)

search_query = ""  # Initialize the search_query variable
search_entry = ttk.Entry(frame, font=("Helvetica", 16))
search_entry.pack(side="right", padx=10, pady=5)

# Add a command to the search entry to update search_query
search_entry.bind("<KeyRelease>", on_search_query_change)

button_frame = ttk.Frame(frame)
button_frame.pack(side = "right", padx=10, pady=5)

button = ttk.Button(button_frame, text="Search", command=getNews)
button.pack(pady=5)

canvas_scroll = tk.Scrollbar(frame, orient="vertical")
canvas_scroll.pack(side="right", fill="y")

# Set line spacing to zero and reduce vertical space (pady) here
text_frame = tk.Text(frame, font=("Unique", 16), wrap="word", bg="#D3D3D3", padx=10, pady=5, yscrollcommand=canvas_scroll.set, spacing1=0, spacing3=0)
text_frame.pack(expand=True, fill="both", pady=5)  # Adjust the pady value as needed

canvas_scroll.config(command=text_frame.yview)

canvas.mainloop()
