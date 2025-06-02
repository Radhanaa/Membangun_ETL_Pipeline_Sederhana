import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from utils.load import load_data_to_csv, load_data_to_gsheet

class TestLoad(unittest.TestCase):
    """Pengujian tingkat lanjut terhadap proses pemuatan data ke CSV dan Google Sheets."""

    def setUp(self):
        """Menyiapkan DataFrame dummy untuk pengujian."""
        self.dummy_df = pd.DataFrame({
            'title': ['Baju A', 'Baju B'],
            'price': [100000, 150000],
            'rating': [4.5, 4.0],
            'colors': [3, 2],
            'size': ['L', 'M'],
            'gender': ['Male', 'Female'],
            'timestamp': pd.to_datetime(['2025-01-01', '2025-01-02'])
        })

    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    def test_simpan_ke_csv(self, mock_makedirs, mock_to_csv):
        """Mengujikan fungsi penyimpanan CSV ke file default 'product.csv'."""
        load_data_to_csv(self.dummy_df)

        # Pastikan direktori dibuat jika belum ada
        mock_makedirs.assert_called_once()

        # Pastikan file CSV disimpan ke file yang benar tanpa index
        mock_to_csv.assert_called_once_with('product.csv', index=False)

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.build')
    def test_simpan_ke_google_sheet_sukses(self, mock_build, mock_credentials):
        """Mengujikan fungsi pemuatan ke Google Sheet ketika tidak terjadi error."""

        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheet

        load_data_to_gsheet(self.dummy_df)

        # Cek apakah build dipanggil dengan benar
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.return_value)

        # Pastikan metode update spreadsheet dipanggil
        mock_sheet.values().update.assert_called_once()
        args, kwargs = mock_sheet.values().update.call_args

        # Validasi nilai yang dikirim ke Google Sheets (harus list of strings)
        body = kwargs.get('body', {})
        self.assertIsInstance(body.get('values', [])[0][0], str)

    @patch('utils.load.Credentials.from_service_account_file', side_effect=Exception("Auth error"))
    def test_gagal_autentikasi_gsheet(self, mock_cred):
        """Mengujikan kegagalan saat autentikasi ke Google Sheet API."""

        with patch('builtins.print') as mock_print:
            load_data_to_gsheet(self.dummy_df)
            mock_print.assert_any_call("❌ Gagal memuat data: Auth error")


if __name__ == '__main__':
    unittest.main()
