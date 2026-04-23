import pandas as pd
import os

# 1. Βρίσκουμε το αρχείο που φτιάξαμε στο προηγούμενο βήμα
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_path, 'data', 'rfm_output.csv')

# 2. Φόρτωση των δεδομένων
rfm = pd.read_csv(input_path, index_col='Customer ID')

# 3. Υπολογισμός Scores (από 1 έως 5)
# Για το Recency: Το μικρότερο νούμερο είναι το καλύτερο (Label 5)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

# Για το Frequency & Monetary: Το μεγαλύτερο νούμερο είναι το καλύτερο (Label 5)
# Χρησιμοποιούμε rank(method='first') γιατί πολλοί πελάτες μπορεί να έχουν την ίδια συχνότητα (π.χ. 1 αγορά)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# 4. Δημιουργία του RFM Score (π.χ. "555" για τον τέλειο πελάτη)
rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# 5. Υπολογισμός συνολικού Score (για απλή κατάταξη)
rfm['RFM_Total_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

# Αποθήκευση του τελικού πίνακα
output_path = os.path.join(base_path, 'data', 'rfm_scored.csv')
rfm.to_csv(output_path)

print("Το Scoring ολοκληρώθηκε!")
print(rfm.head())
