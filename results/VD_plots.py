import matplotlib.pyplot as plt
import pandas as pd

# Function to parse VCF file and extract variant types
def parse_vcf(file_path):
    variant_types = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                parts = line.split('\t')
                info = parts[7]
                svtype = [x.split('=')[1] for x in info.split(';') if 'SVTYPE' in x]
                if svtype:
                    variant_types.append(svtype[0])
    return variant_types

# Path to your VCF file
vcf_path = '/home/eblake/Documents/manta/working_manta/results/Data/candidateSV.vcf'

# Parse the VCF file
variant_types = parse_vcf(vcf_path)

# Create a DataFrame
df = pd.DataFrame(variant_types, columns=['Variant Type'])

# Plotting
plt.figure(figsize=(10, 6))
df['Variant Type'].value_counts().plot(kind='bar')
plt.title('Distribution of Variant Types')
plt.xlabel('Variant Type')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()
