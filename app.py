import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(
    page_title="Ekstraktor Warna Dominan",
    page_icon="🎨",
    layout="centered" 
)

st.title("🎨 Ekstraktor Warna Dominan dari Gambar yang di Upload")
st.markdown("**Petunjuk penggunaan:** unggah sebuah gambar untuk mendapatkan palet warna dengan **lima warna paling dominan**.")

uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Gambar yang Diunggah", use_container_width=True)
    st.write("---")
    st.write("Menganalisis warna dominan, harap tunggu...")

    try:
        img = Image.open(uploaded_file)
        img = img.convert("RGB")

        img.thumbnail((200, 200))


        img_array = np.array(img).reshape(-1, 3)

        n_colors = 5 
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
        kmeans.fit(img_array)

        dominant_colors_rgb = kmeans.cluster_centers_.astype(int)

        st.subheader("Palet Warna Dominan")

        fig, ax = plt.subplots(1, n_colors, figsize=(n_colors * 1.5, 3))
        fig.set_facecolor("#f0f2f6")

        for i, color_rgb in enumerate(dominant_colors_rgb):
            hex_color = '#%02x%02x%02x' % tuple(color_rgb)
            rgb_string = f"({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"

            ax[i].add_patch(plt.Rectangle((0, 0), 1, 1, color=hex_color))
            ax[i].text(0.5, -0.2, hex_color.upper(), ha='center', va='top', transform=ax[i].transAxes, fontsize=10, color='black')
            ax[i].text(0.5, -0.4, rgb_string, ha='center', va='top', transform=ax[i].transAxes, fontsize=8, color='grey')
            ax[i].axis('off')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("---")
        st.markdown("##### Detail Warna:")
        for i, color_rgb in enumerate(dominant_colors_rgb):
            hex_color = '#%02x%02x%02x' % tuple(color_rgb)
            rgb_string = f"RGB: ({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"
            st.write(f"- <span style='background-color:{hex_color}; padding: 5px; border-radius: 3px;'>&nbsp;&nbsp;&nbsp;&nbsp;</span> **{hex_color.upper()}** ({rgb_string})", unsafe_allow_html=True)

    except Exception as e:
        # Penanganan kesalahan jika ada masalah dalam memproses gambar
        st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        st.info("Pastikan file yang diunggah adalah gambar yang valid (JPG, JPEG, PNG, atau WEBP).")

st.markdown("---")