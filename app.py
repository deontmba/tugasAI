import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Ekstraktor Warna Dominan",
    page_icon="🎨",
    layout="centered" # Tata letak konten di tengah halaman
)

st.title("🎨 Ekstraktor Warna Dominan dari Gambar")
st.markdown("Unggah sebuah gambar untuk mendapatkan palet warna dengan **lima warna paling dominan**.")

# --- Bagian Pengunggah File ---
uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Menampilkan gambar yang diunggah
    st.image(uploaded_file, caption="Gambar yang Diunggah", use_column_width=True)
    st.write("---") # Garis pemisah
    st.write("Menganalisis warna dominan, harap tunggu...")

    try:
        # Buka gambar menggunakan Pillow
        img = Image.open(uploaded_file)
        # Pastikan gambar dalam format RGB
        img = img.convert("RGB")

        # Mengubah ukuran gambar untuk pemrosesan yang lebih cepat (opsional)
        # Max dimensi 200 piksel, menjaga rasio aspek
        img.thumbnail((200, 200))

        # Konversi gambar ke array NumPy
        # Meratakan gambar menjadi array 2D piksel (tinggi*lebar, 3)
        img_array = np.array(img).reshape(-1, 3)

        # --- K-Means Clustering untuk menemukan warna dominan ---
        n_colors = 5 # Kita ingin 5 warna dominan
        # Gunakan n_init='auto' atau nilai integer yang sesuai.
        # 'auto' adalah default di scikit-learn >= 1.2
        # Jika Anda menggunakan versi lama, gunakan n_init=10
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto') # Atau n_init=10 untuk versi lama
        kmeans.fit(img_array)

        # Dapatkan pusat cluster (warna dominan)
        dominant_colors_rgb = kmeans.cluster_centers_.astype(int)

        # --- Menampilkan Palet Warna ---
        st.subheader("Palet Warna Dominan")

        # Buat figure dan axes untuk palet warna menggunakan Matplotlib
        # Ukuran figure disesuaikan dengan jumlah warna
        fig, ax = plt.subplots(1, n_colors, figsize=(n_colors * 1.5, 3))
        # Mengatur warna latar belakang figure agar cocok dengan Streamlit
        fig.set_facecolor("#f0f2f6") # Warna latar belakang Streamlit

        for i, color_rgb in enumerate(dominant_colors_rgb):
            # Konversi RGB ke Hex
            hex_color = '#%02x%02x%02x' % tuple(color_rgb)
            rgb_string = f"({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"

            # Menambahkan persegi untuk menampilkan warna
            ax[i].add_patch(plt.Rectangle((0, 0), 1, 1, color=hex_color))
            # Menambahkan teks Hex di bawah warna
            ax[i].text(0.5, -0.2, hex_color.upper(), ha='center', va='top', transform=ax[i].transAxes, fontsize=10, color='black')
            # Menambahkan teks RGB di bawah Hex
            ax[i].text(0.5, -0.4, rgb_string, ha='center', va='top', transform=ax[i].transAxes, fontsize=8, color='grey')
            # Menyembunyikan sumbu
            ax[i].axis('off')

        plt.tight_layout() # Penyesuaian layout agar rapi
        st.pyplot(fig) # Tampilkan plot Matplotlib di Streamlit

        st.markdown("---")
        st.markdown("##### Detail Warna:")
        # Menampilkan warna dominan dengan nilai Hex dan RGB
        for i, color_rgb in enumerate(dominant_colors_rgb):
            hex_color = '#%02x%02x%02x' % tuple(color_rgb)
            rgb_string = f"RGB: ({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"
            # Menggunakan HTML untuk menampilkan kotak warna kecil
            st.write(f"- <span style='background-color:{hex_color}; padding: 5px; border-radius: 3px;'>&nbsp;&nbsp;&nbsp;&nbsp;</span> **{hex_color.upper()}** ({rgb_string})", unsafe_allow_html=True)

    except Exception as e:
        # Penanganan kesalahan jika ada masalah dalam memproses gambar
        st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        st.info("Pastikan file yang diunggah adalah gambar yang valid (JPG, JPEG, PNG, atau WEBP).")

st.markdown("---")
st.markdown("Dibuat dengan ❤️ menggunakan [Streamlit](https://streamlit.io/)")