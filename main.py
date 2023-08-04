import requests
import tkinter as tk
from tkinter import ttk
import webbrowser

def open_link(url):
    webbrowser.open_new(url)

def getNews():
    api_key = "f6194e21b77a4719ae627675582bc833"
    url = "https://newsapi.org/v2/everything?q=apple&apiKey=" + api_key
    news = requests.get(url).json()

    articles = news["articles"]

    label.config(state="normal")
    label.delete(1.0, "end")

    for i, article in enumerate(articles[:10], 1):
        title = article["title"]
        source = article["source"]["name"].rstrip(".com")
        url = article["url"]
        label.insert("end", f"{i}. {title} - {source}\n", f"link_{i}")
        label.tag_bind(f"link_{i}", "<Button-1>", lambda e, link=url: open_link(link))
        label.tag_bind(f"link_{i}", "<Enter>", lambda e, tag=f"link_{i}": label.tag_configure(tag, foreground="blue"))
        label.tag_bind(f"link_{i}", "<Leave>", lambda e, tag=f"link_{i}": label.tag_configure(tag, foreground="black"))

    label.config(state="disabled")

canvas = tk.Tk()
canvas.geometry("800x600")
canvas.title("TechX")
canvas.config(bg="white")

frame = ttk.Frame(canvas, padding="20")
frame.pack(expand=True, fill="both")

title_label = ttk.Label(frame, text="Top 10 News Articles", font=("Unique", 24), foreground="#333")
title_label.pack(pady=10)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

button = ttk.Button(button_frame, text="Reload", command=getNews)
button.pack(pady=5)

label = tk.Text(frame, font=("unique", 16), wrap="word", bg="light grey", highlightthickness=0, padx=10, pady=10)
label.pack(expand=True, fill="both", pady=20)

getNews()

canvas.mainloop()
