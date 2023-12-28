import pandas as pd
import pysam
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# File paths
bam_file = '/home/eblake/Documents/manta/working_manta/Data/Data_to_analysis/G15512.HCC1954.1.COST16011_region.bam'
vcf_file = '/home/eblake/Documents/manta/working_manta/results/Data/candidateSV.vcf'
expected_vcf_file = '/home/eblake/Documents/manta/working_manta/results/Data/somaticSV.vcf'  # Expected results VCF


# Function to get read depth from a BAM file
def get_read_depth(bam_path):
    read_depth = []
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        for pileupcolumn in bam.pileup():
            read_depth.append(pileupcolumn.n)
    return read_depth

# Function to categorize SVs
def categorize_sv(record):
    if 'SVTYPE' in record.info:
        return record.info['SVTYPE']
    return 'Unknown'

# Count SV types for both VCFs
def count_sv_types(vcf_path):
    sv_counts = {}
    with pysam.VariantFile(vcf_path) as vcf:
        for record in vcf:
            sv_type = categorize_sv(record)
            sv_counts[sv_type] = sv_counts.get(sv_type, 0) + 1
    return sv_counts

# Count SVs in both VCF files
sv_counts = count_sv_types(vcf_file)
expected_sv_counts = count_sv_types(expected_vcf_file)

# Get read depth from the BAM file
read_depth_data = get_read_depth(bam_file)

# Plotting SV types for your VCF
plt.figure(figsize=(10, 5))
sns.barplot(x=list(sv_counts.keys()), y=list(sv_counts.values()))
plt.xlabel('SV Type')
plt.ylabel('Count')
plt.title('Counts of Structural Variant Types from manta VCF')
plt.xticks(rotation=45)
plt.savefig('/home/eblake/Documents/manta/working_manta/results/Graphs/sv_counts_manta_vcf.png')
#plt.show()

# Plotting SV types for expected VCF
plt.figure(figsize=(10, 5))
sns.barplot(x=list(expected_sv_counts.keys()), y=list(expected_sv_counts.values()))
plt.xlabel('SV Type')
plt.ylabel('Count')
plt.title('Counts of Structural Variant Types in Expected Results VCF')
plt.xticks(rotation=45)
plt.savefig('/home/eblake/Documents/manta/working_manta/results/Graphs/sv_counts_expected_vcf.png')
#plt.show()


# Plotting read depth
plt.figure(figsize=(12, 6))
plt.plot(read_depth_data, color='blue', linewidth=0.5)
plt.xlabel('Genomic Position')
plt.ylabel('Read Depth')
plt.title('Read Depth Distribution of G15512.HCC1954.1.COST16011_region.bam')
plt.savefig('/home/eblake/Documents/manta/working_manta/results/Graphs/read_depth_bam.png')
#plt.show()



# Convert data to pandas DataFrame for easy handling
sv_counts_df = pd.DataFrame(list(sv_counts.items()), columns=['SV Type', 'Count'])
expected_sv_counts_df = pd.DataFrame(list(expected_sv_counts.items()), columns=['SV Type', 'Count'])
read_depth_df = pd.DataFrame(read_depth_data, columns=['Read Depth'])

# Save DataFrames to CSV (optional)
sv_counts_df.to_csv('/home/eblake/Documents/manta/working_manta/results/Data/sv_counts_manta_vcf.csv', index=False)
expected_sv_counts_df.to_csv('/home/eblake/Documents/manta/working_manta/results/Data/sv_counts_expected_vcf.csv', index=False)
read_depth_df.to_csv('/home/eblake/Documents/manta/working_manta/results/Data/read_depth_bam.csv', index=False)

# Creating a PDF file
pdf = canvas.Canvas("/home/eblake/Documents/manta/working_manta/results/Data/summary_report.pdf", pagesize=letter)
width, height = letter

# Constants for image sizing and positioning
image_width = 400  # Adjust as needed
image_height = 200  # Adjust as needed
margin = 50  # Margin from the bottom of the page

# Adding text and images to PDF
pdf.drawString(100, height - 40, "SV Counts Manta VCF")
pdf.drawImage("/home/eblake/Documents/manta/working_manta/results/Graphs/sv_counts_manta_vcf.png", 100, height - margin - image_height, width=image_width, height=image_height)

pdf.showPage()
pdf.drawString(100, height - 40, "SV Counts Expected VCF")
pdf.drawImage("/home/eblake/Documents/manta/working_manta/results/Graphs/sv_counts_expected_vcf.png", 100, height - margin - image_height, width=image_width, height=image_height)

pdf.showPage()
pdf.drawString(100, height - 40, "Read Depth Distribution")
pdf.drawImage("/home/eblake/Documents/manta/working_manta/results/Graphs/read_depth_bam.png", 100, height - margin - image_height, width=image_width, height=image_height)

# Save PDF
pdf.save()
