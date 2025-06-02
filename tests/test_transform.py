import unittest
import pandas as pd
import numpy as np
from utils.transform import transform_dataset

data_input = [
    {
        'title': 'BT-shirt',
        'price': '100.00',
        'rating': 'Rating: 4.5',
        'colors': 'Colors: 3',
        'size': 'Size: L',
        'gender': 'Gender: Male'
    },
    {
        'title': 'Unknown Title',
        'price': '50.00',
        'rating': 'Rating: 3.5',
        'colors': 'Colors: 2',
        'size': 'Size: M',
        'gender': 'Gender: Female'
    },
    {
        'title': 'Pants',
        'price': '',  # Nilai kosong harus dihapus
        'rating': None,  # Nilai null harus dihapus
        'colors': 'Colors: 0',
        'size': 'Size: XL',
        'gender': 'Gender: Female'
    },
    {
        'title': 'Kaos Polos',
        'price': 'Unknown Product',  # Nilai invalid harus dihapus
        'rating': 'Rating: 4.0',
        'colors': 'Colors: 1',
        'size': 'Size: M',
        'gender': 'Gender: Male'
    }
]

class TestTransform(unittest.TestCase):
    """Pengujian fungsi transformasi dan pembersihan data produk."""

    def setUp(self):
        # Memanggil transformasi untuk digunakan di tiap metode pengujian
        self.df = transform_dataset(data_input)

    def test_output_bertipe_dataframe(self):
        self.assertIsInstance(self.df, pd.DataFrame)

    def test_filter_judul_invalid(self):
        # Baris dengan judul mengandung "unknown" harus dihapus
        self.assertFalse(self.df['title'].str.lower().str.contains('unknown').any())

    def test_kolom_timestamp_ada(self):
        self.assertIn('timestamp', self.df.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df['timestamp']))

    def test_tipe_data_kolom_setelah_transformasi(self):
        self.assertTrue(pd.api.types.is_float_dtype(self.df['price']))
        self.assertTrue(pd.api.types.is_float_dtype(self.df['rating']))
        self.assertTrue(pd.api.types.is_integer_dtype(self.df['colors']))

    def test_konversi_harga_ke_rupiah(self):
        # Harga asli '100.00' dikali 16000 jadi 1_600_000
        harga = self.df.loc[self.df['title'] == 'Baju Keren', 'price'].values[0]
        self.assertAlmostEqual(harga, 100.00 * 16000)

    def test_data_duplikat_dihapus(self):
        # Pastikan tidak ada duplikat pada semua kolom
        self.assertFalse(self.df.duplicated().any())

    def test_nilai_null_dihapus(self):
        self.assertFalse(self.df.isnull().any().any())

    def test_hapus_invalid_price(self):
        # Produk dengan price "Unknown Product" sudah terhapus
        self.assertFalse((self.df['price'] == 0).any() or self.df['price'].isnull().any())

    def test_jumlah_baris_akhir(self):
        # Dari 4 input, 2 baris harus terhapus (judul unknown, dan price invalid/null)
        self.assertEqual(len(self.df), 2)

if __name__ == '__main__':
    unittest.main()
