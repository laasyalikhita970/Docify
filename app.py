from tkinter import *
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

from ocr import extract_text
from database import save_document
from search import search_documents


# ROOT WINDOW
root = TkinterDnD.Tk()
root.title("Docify - Smart Document Search")
root.geometry("1100x650")
root.config(bg="#1e1e1e")


# =========================
# FUNCTIONS
# =========================

def upload_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    text = extract_text(file_path)

    filename = file_path.split("/")[-1]

    save_document(filename, text)

    # File analytics
    word_count = len(text.split())
    char_count = len(text)

    file_info.config(
        text=f"File: {filename}\nWords: {word_count}\nCharacters: {char_count}"
    )

    # Add to sidebar
    file_list.insert(END, filename)

    # Show text
    text_box.delete(1.0, END)
    text_box.insert(END, text)

    status_bar.config(text=f"Uploaded: {filename}")


def drop_file(event):
    file_path = event.data.strip("{}")

    text = extract_text(file_path)

    filename = file_path.split("/")[-1]

    save_document(filename, text)

    # File analytics
    word_count = len(text.split())
    char_count = len(text)

    file_info.config(
        text=f"File: {filename}\nWords: {word_count}\nCharacters: {char_count}"
    )

    file_list.insert(END, filename)

    text_box.delete(1.0, END)
    text_box.insert(END, text)

    status_bar.config(text=f"Dropped: {filename}")


def search_data():
    keyword = search_entry.get().lower()

    results = search_documents(keyword)

    text_box.delete(1.0, END)

    if results:
        for r in results:
            filename = r[0]
            content = r[1]

            text_box.insert(END, f"\nFILE: {filename}\n\n")

            start_index = text_box.index(END)

            text_box.insert(END, content[:1000])

            end_index = text_box.index(END)

            # Highlight keyword
            idx = "1.0"
            while True:
                idx = text_box.search(keyword, idx, stopindex=END)

                if not idx:
                    break

                lastidx = f"{idx}+{len(keyword)}c"

                text_box.tag_add("highlight", idx, lastidx)

                idx = lastidx

            text_box.tag_config(
                "highlight",
                background="yellow",
                foreground="black"
            )

            text_box.insert(END, "\n\n-------------------------\n")

        status_bar.config(text=f"Search completed for: {keyword}")

    else:
        text_box.insert(END, "No results found")
        status_bar.config(text="No matching documents")


def clear_text():
    text_box.delete(1.0, END)
    status_bar.config(text="Cleared")


# =========================
# TOP FRAME
# =========================

top_frame = Frame(root, bg="#1e1e1e")
top_frame.pack(fill=X, pady=10)

Button(
    top_frame,
    text="Upload File",
    command=upload_file,
    bg="#2d2d2d",
    fg="white",
    padx=10
).pack(side=LEFT, padx=10)

search_entry = Entry(
    top_frame,
    width=40,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)
search_entry.pack(side=LEFT, padx=10)

Button(
    top_frame,
    text="Search",
    command=search_data,
    bg="#2d2d2d",
    fg="white",
    padx=10
).pack(side=LEFT, padx=5)

Button(
    top_frame,
    text="Clear",
    command=clear_text,
    bg="#2d2d2d",
    fg="white",
    padx=10
).pack(side=LEFT, padx=5)


# =========================
# MAIN FRAME
# =========================

main_frame = Frame(root, bg="#1e1e1e")
main_frame.pack(fill=BOTH, expand=True)


# =========================
# SIDEBAR
# =========================

sidebar = Frame(main_frame, bg="#252526", width=220)
sidebar.pack(side=LEFT, fill=Y)

Label(
    sidebar,
    text="Recent Files",
    bg="#252526",
    fg="white",
    font=("Arial", 12, "bold")
).pack(pady=10)

file_list = Listbox(
    sidebar,
    bg="#1e1e1e",
    fg="white",
    width=30
)

file_list.pack(fill=BOTH, expand=True, padx=10, pady=10)


# =========================
# CONTENT AREA
# =========================

content_frame = Frame(main_frame, bg="#1e1e1e")
content_frame.pack(side=LEFT, fill=BOTH, expand=True)
info_frame = Frame(content_frame, bg="#252526")
info_frame.pack(fill=X, padx=10, pady=5)

file_info = Label(
    info_frame,
    text="No file loaded",
    bg="#252526",
    fg="white",
    anchor="w",
    justify=LEFT,
    font=("Arial", 10)
)

file_info.pack(fill=X, padx=10, pady=5)


# DRAG & DROP AREA
drop_label = Label(
    content_frame,
    text="Drag & Drop Files Here",
    bg="#333333",
    fg="white",
    width=40,
    height=3,
    font=("Arial", 11)
)

drop_label.pack(pady=10)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_file)


# TEXT BOX
text_box = Text(
    content_frame,
    wrap=WORD,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    font=("Consolas", 11)
)

text_box.pack(fill=BOTH, expand=True, padx=10, pady=10)


# =========================
# STATUS BAR
# =========================

status_bar = Label(
    root,
    text="Ready",
    bd=1,
    relief=SUNKEN,
    anchor=W,
    bg="#2d2d2d",
    fg="white"
)

status_bar.pack(side=BOTTOM, fill=X)


# RUN APP
root.mainloop()