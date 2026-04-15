import pandas as pd
import datetime as dt
import os

# 1. Βρίσκουμε το σωστό μονοπάτι για το αρχείο Excel
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'data', 'online_retail.xlsx') #Δεν είναι πλέον ανεβασμένο γιατί ήταν πολύ μεγάλο αρχείο excel

print("Φόρτωση του Excel... (Επειδή είναι μεγάλο θα πάρει περίπου 1-2 λεπτά)")

try:
    # 2. Διαβάζουμε και τα δύο φύλλα από το ΕΝΑ αρχείο Excel που έχεις
    df_2009 = pd.read_excel(file_path, sheet_name='Year 2009-2010')
    df_2010 = pd.read_excel(file_path, sheet_name='Year 2010-2011')

    # 3. Τα ενώνουμε σε ένα μεγάλο σύνολο
    df = pd.concat([df_2009, df_2010], ignore_index=True)
    print(f"✅ Τα δεδομένα φορτώθηκαν! Συνολικές γραμμές: {len(df)}")

    # 4. Καθαρισμός (όπως και πριν)
    df = df.dropna(subset=['Customer ID'])
    df = df[~df['Invoice'].astype(str).str.contains('C', na=False)]
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

    # 5. Υπολογισμός RFM
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    df['TotalSum'] = df['Quantity'] * df['Price']

    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'nunique',
        'TotalSum': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    # Αποθήκευση του αποτελέσματος σε CSV για να το έχουμε έτοιμο
    output_path = os.path.join(base_path, 'data', 'rfm_output.csv')
    rfm.to_csv(output_path)

    print(f"✅ Το αρχείο RFM δημιουργήθηκε: {output_path}")
    print(rfm.head())

except Exception as e:
    print(f"❌ Κάτι πήγε στραβά: {e}")