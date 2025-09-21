import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup

# URL Ohara
iframe_url = "https://ohara.ai/mini-apps/1fb875a3-9722-46a0-8991-9669576739d2"

# Tinggi total yang diinginkan untuk komponen yang ditampilkan
component_height = 800

def get_modified_html(url):
    """
    Mengambil konten HTML dari URL, menghapus elemen bottom yang tidak diinginkan,
    dan mengembalikan HTML yang sudah dimodifikasi.
    """
    try:
        # Mengambil konten dari URL pihak ketiga
        response = requests.get(url)
        response.raise_for_status()  # Angkat kesalahan untuk kode status yang buruk (4xx atau 5xx)

        # Menggunakan BeautifulSoup untuk mem-parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen bottom yang tidak diinginkan
        # Sesuaikan selector ini jika struktur elemen berubah
        element_to_hide = soup.select_one("div.absolute.bottom-0.left-1\\/4.z-10.-translate-x-1\\/2")
        
        # Hapus elemen tersebut dari pohon DOM
        if element_to_hide:
            element_to_hide.decompose()
            st.write("Elemen bottom berhasil dihapus.")
        else:
            st.warning("Peringatan: Elemen bottom tidak ditemukan dengan selector yang diberikan.")

        # Atasi potensi masalah dengan path relatif (misalnya gambar, CSS)
        # Langkah ini opsional, tapi disarankan
        for tag in soup.find_all(src=True):
            if tag['src'].startswith('/'):
                tag['src'] = url.rstrip('/') + tag['src']
        for tag in soup.find_all(href=True):
            if tag['href'].startswith('/'):
                tag['href'] = url.rstrip('/') + tag['href']

        # Mengembalikan HTML yang sudah dimodifikasi sebagai string
        return str(soup)

    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan saat mengambil data: {e}")
        return None

# Ambil HTML yang sudah dimodifikasi
modified_html = get_modified_html(iframe_url)

if modified_html:
    # Tampilkan konten HTML yang sudah dimodifikasi langsung
    # Menggunakan st.components.v1.html() dengan konten yang sudah dibersihkan
    components.html(modified_html, height=component_height, scrolling=True)
