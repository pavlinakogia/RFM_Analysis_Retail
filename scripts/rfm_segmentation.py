import pandas as pd
import os

# 1. Φόρτωση των scored δεδομένων
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_path, 'data', 'rfm_scored.csv')
rfm = pd.read_csv(input_path, index_col='Customer ID')

# 2. Ορισμός του Segmentation Map (Standard RFM Segments)
# Χρησιμοποιούμε Regex (Regular Expressions) για να αντιστοιχίσουμε τα R και F scores
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# 3. Εφαρμογή του Segmentation
# Συνδυάζουμε το R_Score και F_Score ως string
rfm['segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str)
rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

# 4. Αποθήκευση του τελικού αποτελέσματος
output_path = os.path.join(base_path, 'data', 'rfm_final.csv')
rfm.to_csv(output_path)

print("✅ Το Segmentation ολοκληρώθηκε!")
# Δείξε πόσους πελάτες έχουμε σε κάθε κατηγορία
print(rfm['segment'].value_counts())