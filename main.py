from utils.extract import scrape_all_pages 
from utils.transform import transform_dataset
from utils.load import load_data_to_csv, load_data_to_gsheet

url = "https://fashion-studio.dicoding.dev"
products = scrape_all_pages(url, max_pages=50, delay=1)

cleaned_data = transform_dataset(products)

# Simpan ke CSV
load_data_to_csv(cleaned_data)

# Upload ke Google Sheets
load_data_to_gsheet(cleaned_data)
