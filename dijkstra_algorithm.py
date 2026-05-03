import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# =============================================================
# PROGRAM OPTIMASI RUTE TERPENDEK - DIJKSTRA
# Ahmad Hanif Abiyyu Khrisna (NRP : 2125640006)
# Untuk NRP Belakang 6 (Node A ke Node G)
# =============================================================

def program_dijkstra():
    # // 1. DEFINISI STRUKTUR GRAF (Berdasarkan Page 3).
    # // Format: 'Node': {'Tetangga': Jarak}
    graf = {
        'A': {'C': 1, 'B': 2, 'D': 10},
        'B': {'A': 2, 'D': 1, 'F': 7},
        'C': {'A': 1, 'D': 4, ' E': 8},
        'D': {'A': 10, 'B': 1, 'C': 4, 'E': 5, 'F': 5},
        'E': {'C': 8, 'D': 5, 'G': 2},
        'F': {'B': 7, 'D': 5, 'G': 3},
        'G': {'E': 2, 'F': 3}
    }

    # // 2. INISIALISASI VARIABEL
    start, end = 'A', 'G'
    nodes = list(graf.keys())
    jarak = {node: float('inf') for node in nodes}
    jarak[start] = 0
    parent = {node: None for node in nodes}
    dikunjungi = []
    antrian = nodes.copy()
    
    # // List untuk menyimpan history langkah demi langkah (untuk Tabel)
    log_tabel = []

    # // 3. PROSES ITERASI ALGORITMA
    print(f"Mencari rute terpendek dari {start} ke {end}...\n")
    
    while antrian:
        # // Cari node dengan jarak terkecil di antrian
        node_skrg = min(antrian, key=lambda n: jarak[n])
        
        # // Simpan kondisi saat ini ke log sebelum diproses
        log = {'Iterasi': len(dikunjungi) + 1, 'Node_Aktif': node_skrg}
        for n in nodes:
            log[n] = f"{jarak[n]}({parent[n]})" if jarak[n] != float('inf') else "inf"
        log_tabel.append(log)

        if node_skrg == end: break
        
        antrian.remove(node_skrg)
        dikunjungi.append(node_skrg)

        # // Update Jarak Tetangga (Relaksasi Edge)
        for tetangga, bobot in graf[node_skrg].items():
            if tetangga in antrian:
                baru = jarak[node_skrg] + bobot
                if baru < jarak[tetangga]:
                    jarak[tetangga] = baru
                    parent[tetangga] = node_skrg

    # // 4. MENYUSUN RUTE KEMBALI
    rute = []
    curr = end
    while curr:
        rute.insert(0, curr)
        curr = parent[curr]

    # // 5. OUTPUT TABEL KE KONSOL
    df = pd.DataFrame(log_tabel)
    print("--- TABEL RIWAYAT PERHITUNGAN (DIJKSTRA TABLE) ---")
    print(df.to_string(index=False))

    # // 6. VISUALISASI GRAFIK
    G = nx.Graph()
    for u, neighbors in graf.items():
        for v, w in neighbors.items():
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42) # Layout agar rapi
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_weight='bold')
    
    # // Gambar label bobot pada garis
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # // Highlight rute terpendek dengan warna merah
    edges_rute = list(zip(rute, rute[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_rute, width=3, edge_color='red')

    plt.title(f"Rute Terpendek: {' -> '.join(rute)} (Jarak: {jarak[end]})")
    plt.show()

# Jalankan Program
program_dijkstra()