import unittest
from unittest.mock import patch, Mock
from utils.extract import scrape_all_pages
from requests.exceptions import RequestException

url_dummy = "http://dummy-url"
contoh_html = '''
<div class="collection-card">
    <h3 class="product-title">Baju</h3>
    <div class="price-container">100.00</div>
    <p>Rating: 4.5</p>
    <p>Colors: 3</p>
    <p>Size: L</p>
    <p>Gender: Male</p>
</div>
'''

class TestExtract(unittest.TestCase):
    """Pengujian fungsi dari modul extract."""

    @patch('utils.extract.requests.get')
    def test_ekstraksi_data(self, mock_get): 
        """Mengujikan kasus ketika data berhasil diambil dari halaman HTML."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = contoh_html * 50  # simulasi 50 produk sama
        mock_get.return_value = mock_response

        hasil = scrape_all_pages(url_dummy)
        self.assertIsInstance(hasil, list)
        self.assertEqual(len(hasil), 50)
        self.assertEqual(hasil[0]['title'], 'Baju')

    @patch('utils.extract.requests.get')
    def test_gagal_akses_url(self, mock_get):
        """Mengujikan kasus saat terjadi kegagalan koneksi saat mengambil data."""
        mock_get.side_effect = RequestException("Connection error")

        with self.assertRaises(Exception) as context:
            scrape_all_pages(url_dummy)

        self.assertIn('Gagal mengakses', str(context.exception))

    @patch('utils.extract.requests.get')
    def test_tidak_ada_produk_ditemukan(self, mock_get):
        """Mengujikan hasil ketika halaman tidak mengandung produk apa pun."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No products here!</body></html>'
        mock_get.return_value = mock_response

        hasil = scrape_all_pages(url_dummy)
        self.assertIsInstance(hasil, list)
        self.assertEqual(len(hasil), 0)

if __name__ == '__main__':
    unittest.main()
