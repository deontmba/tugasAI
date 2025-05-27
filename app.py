import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import webcolors
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Color Picker dari Gambar", page_icon="🎨", layout="wide")

def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color.upper()

def prep_image(raw_img):
    # Konversi PIL Image ke numpy array
    img = np.array(raw_img)
    
    # Jika gambar memiliki alpha channel (RGBA), ambil hanya RGB saja
    if img.shape[2] == 4:
        img = img[:, :, :3]
    
    # Resize gambar
    modified_img = cv2.resize(img, (600, 400), interpolation=cv2.INTER_AREA)
    
    # Ubah bentuk menjadi 2D array (pixels x RGB)
    # Periksa dulu apakah modified_img memiliki 3 channel
    if len(modified_img.shape) == 3 and modified_img.shape[2] == 3:
        modified_img = modified_img.reshape(-1, 3)
    else:
        st.error("Format gambar tidak didukung. Pastikan gambar berformat RGB.")
        return None
    
    return modified_img

def color_analysis(img, k=5):
    clf = KMeans(n_clusters=k)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    
    # Sort colors by frequency
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    sorted_hex = [hex_colors[i[0]] for i in sorted_counts]
    sorted_rgb = [rgb_colors[i[0]] for i in sorted_counts]
    
    return sorted_hex, sorted_rgb

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_color_name(rgb_color):
    try:
        color_name = webcolors.rgb_to_name(rgb_color)
    except ValueError:
        color_name = closest_color(rgb_color)
    return color_name

# UI
st.title("🎨 Color Picker dari Gambar")
st.markdown("Unggah gambar dan dapatkan 5 warna dominan darinya!")

uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diunggah", use_column_width=True)
    
    with st.spinner("Menganalisis warna..."):
        modified_image = prep_image(image)
        hex_colors, rgb_colors = color_analysis(modified_image)
        
        st.subheader("5 Warna Dominan")
        cols = st.columns(5)
        
        color_names = []
        for i in range(5):
            with cols[i]:
                st.markdown(f'<div style="background-color:{hex_colors[i]}; height:100px; border-radius:10px;"></div>', unsafe_allow_html=True)
                st.code(hex_colors[i])
                color_name = get_color_name((int(rgb_colors[i][0]), int(rgb_colors[i][1]), int(rgb_colors[i][2])))
                color_names.append(color_name)
                st.write(color_name.capitalize())
        
        # Show color palette
        fig, ax = plt.subplots(figsize=(10, 2))
        for i, color in enumerate(hex_colors[:5]):
            ax.add_patch(plt.Rectangle((i/5, 0), 1/5, 1, color=np.array(rgb_colors[i])/255))
        ax.set_xticks([])
        ax.set_yticks([])
        st.pyplot(fig)
        
        # Show color frequencies
        st.subheader("Distribusi Warna")
        fig2, ax2 = plt.subplots()
        ax2.bar(range(5), [count[1] for count in sorted(Counter(color_labels).items(), key=lambda x: x[1], reverse=True)[:5]], 
                color=[np.array(c)/255 for c in rgb_colors[:5]])
        ax2.set_xticks(range(5))
        ax2.set_xticklabels(color_names[:5], rotation=45)
        ax2.set_ylabel("Frekuensi")
        st.pyplot(fig2)

st.markdown("---")
st.markdown("**Tips:** Gunakan gambar dengan warna yang jelas untuk hasil terbaik!")