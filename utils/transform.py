import pandas as pd
import numpy as np
from datetime import datetime

def transform_dataset(raw_products):
    """Membersihkan dan mentransformasi data produk menjadi DataFrame terstruktur."""
    
    toRP = 16000  # Kurs dolar ke rupiah
    df = pd.DataFrame(raw_products)

    # Cek jika kosong atau tidak memiliki kolom 'price'
    if df.empty or 'price' not in df.columns:
        return df

    # --- 1. Hapus produk invalid ---
    if 'title' in df.columns:
        df = df[df['title'].notna()]  # Hapus nilai NaN pada title
        df = df[~df['title'].str.lower().str.contains('unknown', na=False)]  # Hapus unknown
        df = df[df['title'].str.strip() != '']  # Hapus title kosong
        df['title'] = df['title'].str.replace(r'\s+\d+$', '', regex=True)  # Hapus angka di akhir judul

    # --- 2. Bersihkan kolom numerik ---
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)
    df['colors'] = df['colors'].replace(r'[^0-9]', '', regex=True).replace('', np.nan)

    # --- 3. Bersihkan kolom deskriptif ---
    if 'size' in df.columns:
        df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    if 'gender' in df.columns:
        df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    # --- 4. Transformasi tipe data ---
    df['price'] = df['price'].astype(float) * toRP  # Konversi ke Rupiah
    df['rating'] = df['rating'].apply(lambda x: float(str(x)[:str(x).find('.')+2]) if '.' in str(x) else float(x))
    df['rating'] = df['rating'].astype(float)
    df['colors'] = df['colors'].astype(int)

    # --- 5. Hapus nilai null & duplikat ---
    df.dropna(subset=['rating', 'colors', 'price', 'title'], inplace=True)
    df.drop_duplicates(inplace=True)

    # --- 6. Tambahkan timestamp ---
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].dt.tz_localize('Asia/Jakarta')

    return df
