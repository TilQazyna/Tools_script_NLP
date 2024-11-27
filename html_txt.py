import os
from bs4 import BeautifulSoup
from tqdm import tqdm  # For progress bar

def extract_text_from_div(html_content, class_name):
    """Extracts text from div elements with the specified class name."""
    soup = BeautifulSoup(html_content, 'html.parser')
    div_content = soup.find_all('div', class_=class_name)
    extracted_text = "\n".join([div.get_text(strip=True) for div in div_content])
    return extracted_text

def extract_title_from_html(html_content):
    """Extracts the h1 title with class 'news-title__title' from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tag = soup.find('h1', class_="news-title__title")
    return h1_tag.get_text(strip=True) if h1_tag else 'No title found'

def process_html_files(directory_path, output_dir):
    """Processes all HTML files in a directory, extracts title and text, and saves each file's text to a separate file."""
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the list of HTML files
    html_files = [filename for filename in os.listdir(directory_path) if filename.endswith(".html")]
    
    # Iterate through all files in the directory with a progress bar
    for filename in tqdm(html_files, desc="Processing HTML files"):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
            # Extract title and content
            title = extract_title_from_html(html_content)
            content = extract_text_from_div(html_content, "news-text")
            
            # Create an output file for each HTML file
            output_file = os.path.join(output_dir, filename.replace('.html', '.txt'))
            with open(output_file, 'w', encoding='utf-8') as output_f:
                # Write title and content
                output_f.write(f"{title}\n\n{content}")

# Define the directory containing the HTML files and the output directory for text files
directory_path = r'D:\1 млрд есеп\Bauyrzhan\qazaquni.kz\қоғам'  # Path to the folder containing your HTML files
output_dir = r'D:\1 млрд есеп\Bauyrzhan\qazaquni.kz\қоғам\output'  # Directory where individual text files will be saved

# Run the script
process_html_files(directory_path, output_dir)
