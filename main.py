import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import necessary libraries
from tkinter import filedialog  # Import filedialog for browsing files
import PyPDF2  # For extracting text from PDF files
import os  # For path handling

# Function to extract text from a PDF file
def extract_text(file_path):
    if file_path.lower().endswith('.pdf'):  # Check if the file is a PDF
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)

                pdf_text = ''
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()

            extracted_text.delete(1.0, tk.END)
            extracted_text.insert(tk.END, pdf_text)  # Insert extracted text into the Text widget
        except Exception as e:
            extracted_text.delete(1.0, tk.END)
            extracted_text.insert(tk.END, f"Error: {e}")  # Display error if text extraction fails
    else:
        extracted_text.delete(1.0, tk.END)
        extracted_text.insert(tk.END, "Please select/drop a PDF file.")  # Prompt to select a PDF file

# Function to browse for a file using filedialog
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, os.path.normpath(file_path))  # Display the normalized file path
        extract_text(file_path)

# Function triggered on drop event
def on_drop(event):
    file_path = event.data.strip('{}')  # Extract file path and remove curly braces (if present)
    text_display.delete(1.0, tk.END)
    text_display.insert(tk.END, os.path.normpath(file_path))  # Display the normalized file path
    extract_text(file_path)

# Create the main Tkinter window
root = TkinterDnD.Tk()
root.title("Text Extractor")  # Set the window title

# Create a Text widget for displaying the dropped or selected file path
text_display = tk.Text(root, height=1, width=40)
text_display.pack(padx=20, pady=10)

# Enable drag and drop functionality on the Text widget
text_display.drop_target_register(DND_FILES)
text_display.dnd_bind('<<Drop>>', on_drop)

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse File", command=browse_file)
browse_button.pack()

# Create another Text widget for displaying the extracted text
extracted_text = tk.Text(root, height=20, width=60)
extracted_text.pack(padx=20, pady=10)

root.mainloop()  # Start the main event loop
