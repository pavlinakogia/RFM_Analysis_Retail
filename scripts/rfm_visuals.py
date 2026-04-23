import pandas as pd
import matplotlib.pyplot as plt
import squarify
import os

# Φόρτωση δεδομένων
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rfm = pd.read_csv(os.path.join(base_path, 'data', 'rfm_final.csv'))

# Προετοιμασία δεδομένων για το Treemap
df_tree = rfm['segment'].value_counts().reset_index()
df_tree.columns = ['segment', 'count']

# Σχεδιασμός
plt.figure(figsize=(12, 8))
squarify.plot(sizes=df_tree['count'], label=df_tree['segment'], alpha=0.8,
              color=plt.cm.Spectral(df_tree.index / float(len(df_tree))))

plt.title("RFM Customer Segments Treemap", fontsize=18)
plt.axis('off')

# Αποθήκευση
output_path = os.path.join(base_path, 'outputs', 'rfm_treemap.png')
plt.savefig(output_path)
plt.show()

print(f"Το Treemap σώθηκε στο: {output_path}")
