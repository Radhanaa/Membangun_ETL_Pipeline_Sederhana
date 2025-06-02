import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

def load_data_to_csv(df, output_path='product.csv'):
    """
    Menyimpan DataFrame hasil transformasi ke file CSV.

    Parameter:
    - df (pd.DataFrame): DataFrame yang akan disimpan.
    - output_path (str): Path lengkap ke file tujuan penyimpanan CSV.
    """

    # Simpan DataFrame ke CSV tanpa index
    df.to_csv(output_path, index=False)
    print(f"✅ Data berhasil disimpan ke {output_path}")



# Konfigurasi spreadsheet
SERVICE_ACCOUNT_FILE = 'google-sheet-api.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1P1hOG0RRmT8zujKOa7GYgyYBFoJ1sjRtANUnN7PdXgc'
RANGE_NAME = 'Sheet1!A2'  # Mulai dari baris kedua (baris pertama untuk header)

# Fungsi utama untuk load
def load_data_to_gsheet(df: pd.DataFrame):
    """Mengirim data hasil transformasi ke Google Spreadsheet."""
    try:
        # Autentikasi ke Google Sheets API
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Ubah DataFrame ke list of lists
        values = df.astype(str).values.tolist()  # Ubah semua ke string agar aman disimpan di spreadsheet

        body = {
            'values': values
        }

        # Tulis ke spreadsheet
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("✅ Data berhasil dimuat ke Google Spreadsheet!")
    except Exception as e:
        print(f"❌ Gagal memuat data: {e}")

