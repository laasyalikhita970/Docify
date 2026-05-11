from tkinter import *
from tkinter import filedialog

from ocr import extract_text
from database import save_document
from search import search_documents

root = Tk()
root.title("Docify - Smart Document Search")
root.geometry("900x600")


# TOP FRAME (Buttons)
top_frame = Frame(root)
top_frame.pack(pady=10)


# TEXT AREA
text_box = Text(root, wrap=WORD)
text_box.pack(fill=BOTH, expand=True, padx=10, pady=10)


# UPLOAD FUNCTION
def upload_file():
    file_path = filedialog.askopenfilename()

    text = extract_text(file_path)

    filename = file_path.split("/")[-1]

    save_document(filename, text)

    text_box.delete(1.0, END)
    text_box.insert(END, text)


# SEARCH FUNCTION
def search_data():
    keyword = search_entry.get().lower()

    results = search_documents(keyword)

    text_box.delete(1.0, END)

    if results:
        for r in results:
            filename = r[0]
            content = r[1]

            # Highlight logic (simple version)
            highlighted = content.replace(
                keyword,
                f"[{keyword.upper()}]"
            )

            text_box.insert(END, f"FILE: {filename}\n\n")
            text_box.insert(END, highlighted[:500])
            text_box.insert(END, "\n\n----------------------\n\n")
    else:
        text_box.insert(END, "No results found")


# BUTTONS
Button(top_frame, text="Upload File", command=upload_file).grid(row=0, column=0, padx=10)
Button(top_frame, text="Clear", command=lambda: text_box.delete(1.0, END)).grid(row=0, column=3, padx=10)
search_entry = Entry(top_frame, width=40)
search_entry.grid(row=0, column=1, padx=10)

Button(top_frame, text="Search", command=search_data).grid(row=0, column=2, padx=10)


root.mainloop()