# USAGE:
# python convert_parquet.py my_parquet_file.parquet
#
# based on https://chat.openai.com/c/ea3e9401-e7bb-4288-b270-83b0fb327abe
#
# pip install pandas openpyxl pyarrow

import sys
import pandas as pd

# Replace 'your_file.parquet' with the path to your Parquet file
# parquet_file = 'vary_amount_of_training_data__adult_sexual__aps.parquet'
parquet_file = sys.argv[1]

assert parquet_file.endswith(".parquet")

# Read the Parquet file
df = pd.read_parquet(parquet_file)

# Replace 'output_file.xlsx' with the desired output file name
output_file = parquet_file.replace('.parquet', '.xlsx')

# Write to an Excel file
df.to_excel(output_file, index=False)

print(f"Wrote to {output_file}")


