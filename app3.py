import streamlit as st
import pandas as pd
from datetime import date

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Informasi Data Kelas",
    page_icon="🏫",
    layout="wide"
)

# Custom Styling (CSS)
st.markdown("""
    <style>
    .main-title {
        color: #1a365d;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #718096;
        font-size: 14px;
        margin-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inisialisasi Session State (Database Dinamis)
if 'data_kelas' not in st.session_state:
    st.session_state['data_kelas'] = pd.DataFrame([
        {"Nama Kelas": "Kelas VII-A", "Wali Kelas": "Bp. Joko Susilo, S.Pd."},
        {"Nama Kelas": "Kelas VII-B", "Wali Kelas": "Ibu Sri Rahayu, M.Pd."},
        {"Nama Kelas": "Kelas VIII-A", "Wali Kelas": "Ibu Anita, S.Si."},
        {"Nama Kelas": "Kelas IX-A", "Wali Kelas": "Bp. Bambang, M.Pd."}
    ])

if 'data_siswa' not in st.session_state:
    st.session_state['data_siswa'] = pd.DataFrame([
        {"NIS": "2425001", "NISN": "242550011", "Nama Lengkap": "Ahmad Fauzi", "Kelas": "Kelas VII-A", "L/P": "L", "Tempat, Tanggal Lahir": "Jember, 12 Maret 2013", "Alamat": "Jl. Merdeka No. 45, Jember", "Nama Wali": "Budi Santoso", "Kontak": "0812-3456-7890"},
        {"NIS": "2425002", "NISN": "242550022", "Nama Lengkap": "Bunga Lestari", "Kelas": "Kelas VII-A", "L/P": "P", "Tempat, Tanggal Lahir": "Jember, 12 Maret 2013", "Alamat": "Jl. Merdeka No. 45, Jember", "Nama Wali": "Siti Rahma", "Kontak": "0812-3456-7891"},
        {"NIS": "2425003", "NISN": "242550033", "Nama Lengkap": "Candra Wijaya", "Kelas": "Kelas VII-A", "L/P": "L", "Tempat, Tanggal Lahir": "Jember, 15 April 2013", "Alamat": "Jl. Merdeka No. 12, Jember", "Nama Wali": "Hendra Wijaya", "Kontak": "0812-3456-7892"},
        {"NIS": "2425004", "NISN": "242550044", "Nama Lengkap": "Dwi Saputra", "Kelas": "Kelas VII-B", "L/P": "L", "Tempat, Tanggal Lahir": "Jember, 18 April 2013", "Alamat": "Jl. Mawar No. 05, Jember", "Nama Wali": "Agus Saputra", "Kontak": "0812-3456-7893"},
        {"NIS": "2425005", "NISN": "242550055", "Nama Lengkap": "Eka Putri", "Kelas": "Kelas VII-B", "L/P": "P", "Tempat, Tanggal Lahir": "Jember, 14 April 2013", "Alamat": "Jl. Anggrek No. 08, Jember", "Nama Wali": "Rahmat Hidayat", "Kontak": "0812-3456-7894"}
    ])

# Inisialisasi Data Absensi & Nilai
if 'data_absensi' not in st.session_state:
    st.session_state['data_absensi'] = pd.DataFrame(columns=["Tanggal", "Kelas", "NIS", "Nama Lengkap", "Status"])

if 'data_nilai' not in st.session_state:
    st.session_state['data_nilai'] = pd.DataFrame(columns=["Mata Pelajaran", "Kelas", "NIS", "Nama Lengkap", "Tugas", "UTS", "UAS", "Nilai Akhir"])

def get_opsi_kelas():
    if not st.session_state['data_kelas'].empty and "Nama Kelas" in st.session_state['data_kelas'].columns:
        return st.session_state['data_kelas']["Nama Kelas"].tolist()
    return ["Kelas VII-A"]

# 3. Sidebar Navigasi
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/Logo-Tut-Wuri-Handayani-PNG-Warna.png?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", width=100)
    st.markdown("### **SMPN 7 JEMBER**")
    st.caption("Sistem Akademik")
    st.divider()
    
    menu = st.radio(
        "Menu Utama",
        ["Data Kelas (Dashboard)", "Kelola Kelas & Wali Kelas", "Tambah Data Siswa", "Edit / Hapus Siswa", "Input Absensi", "Input Nilai", "Import / Export Excel"],
        index=0
    )

# 4. Header Utama
st.markdown('<h1 class="main-title">SISTEM INFORMASI DATA KELAS</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tahun Ajaran 2026/2027</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 1: DATA KELAS (DASHBOARD)
# ---------------------------------------------------------
if menu == "Data Kelas (Dashboard)":
    col_f1, col_f2, col_s = st.columns([2, 2, 3])
    
    list_kelas = ["Semua Kelas"] + get_opsi_kelas()
    with col_f1:
        pilih_kelas = st.selectbox("Pilih Kelas", list_kelas)
    
    with col_f2:
        if pilih_kelas == "Semua Kelas":
            wali_terpilih = "Semua Wali Kelas"
        else:
            match_wali = st.session_state['data_kelas'][st.session_state['data_kelas']["Nama Kelas"] == pilih_kelas]["Wali Kelas"].values
            wali_terpilih = match_wali[0] if len(match_wali) > 0 else "Belum Ditentukan"
        st.text_input("Wali Kelas", value=wali_terpilih, disabled=True)
        
    with col_s:
        cari_nama = st.text_input("🔍 Cari Siswa...", placeholder="Ketik NIS, NISN, atau Nama...")

    # Filter Data Siswa
    df_filtered = st.session_state['data_siswa'].copy()
    if pilih_kelas != "Semua Kelas":
        df_filtered = df_filtered[df_filtered["Kelas"] == pilih_kelas]
        
    if cari_nama and not df_filtered.empty:
        df_filtered = df_filtered[
            df_filtered["Nama Lengkap"].astype(str).str.contains(cari_nama, case=False, na=False) |
            df_filtered["NIS"].astype(str).str.contains(cari_nama, case=False, na=False) |
            df_filtered["NISN"].astype(str).str.contains(cari_nama, case=False, na=False)
        ]

    # Card Statistik
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.metric("Total Siswa", len(df_filtered))
    with col_c2:
        st.metric("Laki-laki", len(df_filtered[df_filtered["L/P"] == "L"]) if "L/P" in df_filtered.columns else 0)
    with col_c3:
        st.metric("Perempuan", len(df_filtered[df_filtered["L/P"] == "P"]) if "L/P" in df_filtered.columns else 0)
    with col_c4:
        st.metric("Wali Kelas", wali_terpilih)

    st.write("")
    
    # Tabel Data Utama
    if not df_filtered.empty:
        df_tampil = df_filtered.reset_index(drop=True)
        df_tampil.index = df_tampil.index + 1
        df_tampil.index.name = "No"
        st.dataframe(df_tampil, use_container_width=True)
    else:
        st.warning("Data siswa tidak ditemukan.")

    st.caption(f"Menampilkan {len(df_filtered)} data siswa.")
    st.divider()

    btn_col1, btn_col2, _ = st.columns([2, 2, 6])
    with btn_col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Unduh CSV/Excel", data=csv_data, file_name=f"Data_Siswa_{pilih_kelas}.csv", mime="text/csv", use_container_width=True)
    with btn_col2:
        if st.button("🖨️ Cetak / Pratinjau", use_container_width=True):
            st.info("Gunakan Ctrl + P untuk mencetak halaman ini dari browser.")

# ---------------------------------------------------------
# MENU 2: KELOLA KELAS & WALI KELAS
# ---------------------------------------------------------
elif menu == "Kelola Kelas & Wali Kelas":
    st.subheader("🏫 Manajemen Kelas dan Wali Kelas")
    
    tab_list, tab_tambah, tab_edit, tab_hapus = st.tabs([
        "📋 Daftar Kelas & Wali Kelas", 
        "➕ Tambah Kelas Baru", 
        "📝 Edit Kelas & Wali Kelas", 
        "🗑️ Hapus Kelas"
    ])
    
    with tab_list:
        df_k = st.session_state['data_kelas'].copy()
        if not df_k.empty:
            df_k.index = df_k.index + 1
            df_k.index.name = "No"
            st.dataframe(df_k, use_container_width=True)
        else:
            st.info("Belum ada data kelas.")

    with tab_tambah:
        with st.form("form_tambah_kelas_key", clear_on_submit=True):
            nama_kelas_baru = st.text_input("Nama Kelas Baru", placeholder="Contoh: Kelas VII-C")
            nama_wali_baru = st.text_input("Nama Wali Kelas", placeholder="Contoh: Bp. Ahmad, S.Pd.")
            btn_tambah_k = st.form_submit_button("➕ Simpan Kelas Baru")
            
            if btn_tambah_k:
                if nama_kelas_baru and nama_wali_baru:
                    if nama_kelas_baru in get_opsi_kelas():
                        st.error("Nama kelas sudah ada!")
                    else:
                        baru = pd.DataFrame([{"Nama Kelas": nama_kelas_baru, "Wali Kelas": nama_wali_baru}])
                        st.session_state['data_kelas'] = pd.concat([st.session_state['data_kelas'], baru], ignore_index=True)
                        st.success(f"Berhasil menambahkan **{nama_kelas_baru}**!")
                        st.rerun()
                else:
                    st.error("Mohon lengkapi Nama Kelas dan Nama Wali Kelas!")

    with tab_edit:
        opsi_k_edit = get_opsi_kelas()
        if opsi_k_edit:
            kelas_pilihan_edit = st.selectbox("Pilih Kelas yang Ingin Diubah", opsi_k_edit, key="sel_edit_k")
            df_curr_k = st.session_state['data_kelas']
            row_edit = df_curr_k[df_curr_k["Nama Kelas"] == kelas_pilihan_edit].iloc[0]
            
            with st.form("form_edit_kelas_key"):
                edit_nama_k = st.text_input("Nama Kelas", value=row_edit["Nama Kelas"])
                edit_wali_k = st.text_input("Nama Wali Kelas", value=row_edit["Wali Kelas"])
                btn_simpan_k = st.form_submit_button("🔄 Perbarui Kelas & Wali Kelas")
                
                if btn_simpan_k:
                    idx = df_curr_k[df_curr_k["Nama Kelas"] == kelas_pilihan_edit].index[0]
                    st.session_state['data_kelas'].loc[idx] = [edit_nama_k, edit_wali_k]
                    if edit_nama_k != kelas_pilihan_edit:
                        st.session_state['data_siswa'].loc[st.session_state['data_siswa']["Kelas"] == kelas_pilihan_edit, "Kelas"] = edit_nama_k
                    st.success("Data berhasil diperbarui!")
                    st.rerun()

    with tab_hapus:
        opsi_k_hapus = get_opsi_kelas()
        if opsi_k_hapus:
            kelas_pilihan_hapus = st.selectbox("Pilih Kelas yang Ingin Dihapus", opsi_k_hapus, key="sel_hapus_k")
            st.warning(f"Apakah Anda yakin ingin menghapus **{kelas_pilihan_hapus}**?")
            if st.button("❌ Ya, Hapus Kelas Ini"):
                st.session_state['data_kelas'] = st.session_state['data_kelas'][st.session_state['data_kelas']["Nama Kelas"] != kelas_pilihan_hapus].reset_index(drop=True)
                st.success("Kelas berhasil dihapus!")
                st.rerun()

# ---------------------------------------------------------
# MENU 3: TAMBAH DATA SISWA
# ---------------------------------------------------------
elif menu == "Tambah Data Siswa":
    st.subheader("➕ Form Tambah Siswa Baru")
    
    with st.form("form_tambah_siswa_key", clear_on_submit=True):
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            nis = st.text_input("NIS", placeholder="Contoh: 2425006")
            nisn = st.text_input("NISN", placeholder="Contoh: 242550066")
            nama = st.text_input("Nama Lengkap")
            kelas = st.selectbox("Kelas", get_opsi_kelas())
            gender = st.radio("Jenis Kelamin", ["L", "P"], horizontal=True)
            
        with col_input2:
            ttl = st.text_input("Tempat, Tanggal Lahir", placeholder="Jember, 12 Maret 2013")
            alamat = st.text_area("Alamat Lengkap")
            wali = st.text_input("Nama Wali / Orang Tua")
            kontak = st.text_input("Kontak Orang Tua", placeholder="0812-xxxx-xxxx")
            
        submit = st.form_submit_button("💾 Simpan Data Siswa")
        
        if submit:
            if nis and nama:
                data_baru = {
                    "NIS": nis,
                    "NISN": nisn,
                    "Nama Lengkap": nama,
                    "Kelas": kelas,
                    "L/P": gender,
                    "Tempat, Tanggal Lahir": ttl,
                    "Alamat": alamat,
                    "Nama Wali": wali,
                    "Kontak": kontak
                }
                st.session_state['data_siswa'] = pd.concat([st.session_state['data_siswa'], pd.DataFrame([data_baru])], ignore_index=True)
                st.success(f"Berhasil menambahkan siswa: **{nama}**!")
            else:
                st.error("Mohon isi minimal NIS dan Nama Lengkap!")

# ---------------------------------------------------------
# MENU 4: EDIT / HAPUS SISWA
# ---------------------------------------------------------
elif menu == "Edit / Hapus Siswa":
    st.subheader("⚙️ Kelola Data Siswa")
    
    df = st.session_state['data_siswa']
    if df.empty:
        st.warning("Belum ada data siswa.")
    else:
        daftar_nis = df["NIS"].astype(str).tolist()
        nis_terpilih = st.selectbox("Pilih NIS Siswa", daftar_nis)
        data_siswa_selected = df[df["NIS"].astype(str) == nis_terpilih].iloc[0]
        
        tab_edit_s, tab_hapus_s = st.tabs(["📝 Edit Data Siswa", "🗑️ Hapus Siswa"])
        
        with tab_edit_s:
            with st.form("form_edit_siswa_key"):
                c1, c2 = st.columns(2)
                opsi_k = get_opsi_kelas()
                idx_k = opsi_k.index(data_siswa_selected["Kelas"]) if data_siswa_selected["Kelas"] in opsi_k else 0
                
                with c1:
                    edit_nisn = st.text_input("NISN", value=data_siswa_selected["NISN"])
                    edit_nama = st.text_input("Nama Lengkap", value=data_siswa_selected["Nama Lengkap"])
                    edit_kelas = st.selectbox("Kelas", opsi_k, index=idx_k)
                    edit_gender = st.radio("L/P", ["L", "P"], index=0 if data_siswa_selected["L/P"] == "L" else 1, horizontal=True)
                with c2:
                    edit_ttl = st.text_input("Tempat, Tanggal Lahir", value=data_siswa_selected["Tempat, Tanggal Lahir"])
                    edit_alamat = st.text_area("Alamat", value=data_siswa_selected["Alamat"])
                    edit_wali = st.text_input("Nama Wali", value=data_siswa_selected["Nama Wali"])
                    edit_kontak = st.text_input("Kontak", value=data_siswa_selected["Kontak"])
                
                btn_simpan_edit = st.form_submit_button("🔄 Perbarui Data Siswa")
                
                if btn_simpan_edit:
                    idx = df[df["NIS"].astype(str) == nis_terpilih].index[0]
                    st.session_state['data_siswa'].loc[idx] = [nis_terpilih, edit_nisn, edit_nama, edit_kelas, edit_gender, edit_ttl, edit_alamat, edit_wali, edit_kontak]
                    st.success("Data siswa berhasil diperbarui!")
                    st.rerun()

        with tab_hapus_s:
            st.warning(f"Apakah Anda yakin ingin menghapus siswa **{data_siswa_selected['Nama Lengkap']}** (NIS: {nis_terpilih})?")
            if st.button("❌ Ya, Hapus Siswa Ini"):
                st.session_state['data_siswa'] = df[df["NIS"].astype(str) != nis_terpilih].reset_index(drop=True)
                st.success("Data siswa berhasil dihapus!")
                st.rerun()

# ---------------------------------------------------------
# MENU 5: INPUT ABSENSI (FITUR BARU)
# ---------------------------------------------------------
elif menu == "Input Absensi":
    st.subheader("📅 Input Absensi Harian Siswa")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        tgl_absensi = st.date_input("Tanggal Absensi", date.today())
    with col_a2:
        kelas_absensi = st.selectbox("Pilih Kelas", get_opsi_kelas(), key="abs_kelas")
        
    df_siswa_abs = st.session_state['data_siswa'][st.session_state['data_siswa']["Kelas"] == kelas_absensi]
    
    if df_siswa_abs.empty:
        st.warning("Belum ada siswa di kelas ini.")
    else:
        with st.form("form_absensi"):
            st.write(f"Daftar Siswa {kelas_absensi} - Tanggal: {tgl_absensi}")
            hasil_absensi = []
            
            for index, row in df_siswa_abs.iterrows():
                col_s1, col_s2 = st.columns([3, 2])
                with col_s1:
                    st.write(f"**{row['Nama Lengkap']}** (NIS: {row['NIS']})")
                with col_s2:
                    status = st.selectbox("Status", ["Hadir", "Sakit", "Izin", "Alpa"], key=f"abs_{row['NIS']}")
                hasil_absensi.append({"Tanggal": str(tgl_absensi), "Kelas": kelas_absensi, "NIS": row['NIS'], "Nama Lengkap": row['Nama Lengkap'], "Status": status})
                
            simpan_abs = st.form_submit_button("💾 Simpan Absensi")
            if simpan_abs:
                df_abs_baru = pd.DataFrame(hasil_absensi)
                st.session_state['data_absensi'] = pd.concat([st.session_state['data_absensi'], df_abs_baru], ignore_index=True)
                st.success("Absensi berhasil disimpan!")

    st.divider()
    st.markdown("### 📋 Riwayat Absensi")
    st.dataframe(st.session_state['data_absensi'], use_container_width=True)

# ---------------------------------------------------------
# MENU 6: INPUT NILAI (FITUR BARU)
# ---------------------------------------------------------
elif menu == "Input Nilai":
    st.subheader("📝 Input Nilai Siswa")
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        mapel = st.selectbox("Mata Pelajaran", ["Matematika", "Bahasa Indonesia", "IPA", "IPS", "Bahasa Inggris", "PAI", "PJOK"])
    with col_n2:
        kelas_nilai = st.selectbox("Pilih Kelas", get_opsi_kelas(), key="nil_kelas")
        
    df_siswa_nil = st.session_state['data_siswa'][st.session_state['data_siswa']["Kelas"] == kelas_nilai]
    
    if df_siswa_nil.empty:
        st.warning("Belum ada siswa di kelas ini.")
    else:
        with st.form("form_nilai"):
            st.write(f"Input Nilai {mapel} - {kelas_nilai}")
            hasil_nilai = []
            
            for index, row in df_siswa_nil.iterrows():
                st.write(f"**{row['Nama Lengkap']}** ({row['NIS']})")
                c_n1, c_n2, c_n3 = st.columns(3)
                with c_n1:
                    n_tugas = st.number_input("Nilai Tugas", min_value=0, max_value=100, value=80, key=f"tug_{row['NIS']}")
                with c_n2:
                    n_uts = st.number_input("Nilai UTS", min_value=0, max_value=100, value=80, key=f"uts_{row['NIS']}")
                with c_n3:
                    n_uas = st.number_input("Nilai UAS", min_value=0, max_value=100, value=80, key=f"uas_{row['NIS']}")
                
                n_akhir = round((n_tugas * 0.3) + (n_uts * 0.3) + (n_uas * 0.4), 2)
                hasil_nilai.append({"Mata Pelajaran": mapel, "Kelas": kelas_nilai, "NIS": row['NIS'], "Nama Lengkap": row['Nama Lengkap'], "Tugas": n_tugas, "UTS": n_uts, "UAS": n_uas, "Nilai Akhir": n_akhir})
                st.divider()
                
            simpan_nil = st.form_submit_button("💾 Simpan Data Nilai")
            if simpan_nil:
                df_nil_baru = pd.DataFrame(hasil_nilai)
                st.session_state['data_nilai'] = pd.concat([st.session_state['data_nilai'], df_nil_baru], ignore_index=True)
                st.success("Data Nilai berhasil disimpan!")

    st.divider()
    st.markdown("### 📊 Rekapitulasi Nilai Siswa")
    st.dataframe(st.session_state['data_nilai'], use_container_width=True)

# ---------------------------------------------------------
# MENU 7: IMPORT / EXPORT EXCEL
# ---------------------------------------------------------
elif menu == "Import / Export Excel":
    st.subheader("📁 Import & Export Data Excel/CSV")
    
    st.markdown("### 1. Unggah File Excel/CSV")
    uploaded_file = st.file_uploader("Pilih file Excel (.xlsx) atau CSV (.csv)", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_imported = pd.read_csv(uploaded_file)
            else:
                df_imported = pd.read_excel(uploaded_file)
                
            st.write("Pratinjau Data:")
            st.dataframe(df_imported.head())
            
            if st.button("📥 Timpa Semua Data Siswa"):
                st.session_state['data_siswa'] = df_imported
                st.success("Data siswa berhasil diperbarui dari file!")
                st.rerun()
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

    st.divider()
    st.markdown("### 2. Ekspor Semua Data Siswa")
    csv_all = st.session_state['data_siswa'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Seluruh Data Siswa (CSV)",
        data=csv_all,
        file_name="Seluruh_Data_Siswa.csv",
        mime="text/csv"
    )
