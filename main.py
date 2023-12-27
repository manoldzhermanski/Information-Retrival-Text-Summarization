import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import necessary libraries
import PyPDF2  # For extracting text from PDF files


# Function to extract text from a PDF file
import fitz  # PyMuPDF

def extract_text(file_path):
    # Check if the file is a PDF
    if file_path.lower().endswith('.pdf'):
        try:
            pdf_document = fitz.open(file_path)
            num_pages = pdf_document.page_count

            pdf_text = ''
            for page_num in range(num_pages):
                page = pdf_document.load_page(page_num)
                pdf_text += page.get_text()

            print(pdf_text)

            # Clear the Text widget and insert extracted text
            extracted_text.delete(1.0, tk.END)
            extracted_text.insert(tk.END, pdf_text)

            pdf_document.close()  # Close the PDF document
        except Exception as e:
            # Handle exceptions while reading or extracting text from the PDF
            extracted_text.delete(1.0, tk.END)
            extracted_text.insert(tk.END, f"Error: {e}")
    else:
        # Display a message if a non-PDF file is selected/dropped
        extracted_text.delete(1.0, tk.END)
        extracted_text.insert(tk.END, "Please select/drop a PDF file.")



# Function triggered on drop event
def on_drop(event):
    file_path = event.data.strip('{}')
    extract_text(file_path)


# Function to browse and select a file using filedialog
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        extract_text(file_path)


# Create the main Tkinter window
root = TkinterDnD.Tk()
root.title("Text Extractor")  # Set the window title

# Create a Text widget for displaying the extracted text
extracted_text = tk.Text(root, height=20, width=60)
extracted_text.pack(padx=20, pady=10)
extracted_text.insert(tk.END, "Choose your file by clicking the Browse File button or Drag and Drop the file")

# Enable drop target functionality for the Text widget
extracted_text.drop_target_register(DND_FILES)
extracted_text.dnd_bind('<<Drop>>', on_drop)

# Create a button for browsing files
browse_button = tk.Button(root, text="Browse File", command=browse_file)
browse_button.pack(padx=20, pady=15)  # Place the button in the window

root.mainloop()  # Start the main event loop
