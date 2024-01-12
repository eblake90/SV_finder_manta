import pandas as pd
import pysam
import matplotlib.pyplot as plt
import os
import argparse

# Setting up Argument Parser
parser = argparse.ArgumentParser(description='Process BAM files to analyze read depth.')
parser.add_argument('--bam', required=True, help='Path to the BAM file')
parser.add_argument('--output', required=True, help='Path to the output folder')
args = parser.parse_args()

# File paths
bam_file = args.bam
output_folder = args.output

# Create Graphs and Data folders in the specified output directory
save_graph_path = os.path.join(output_folder, 'Graphs')
save_data_path = os.path.join(output_folder, 'Data')
os.makedirs(save_graph_path, exist_ok=True)
os.makedirs(save_data_path, exist_ok=True)

# Function to get read depth from a BAM file
def get_read_depth(bam_path):
    read_depth = []
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        for pileupcolumn in bam.pileup():
            read_depth.append(pileupcolumn.n)
    return read_depth

# Get read depth data
read_depth_data = get_read_depth(bam_file)

# Calculating statistics
average_read_depth = sum(read_depth_data) / len(read_depth_data) if read_depth_data else 0
lowest_read_depth = min(read_depth_data) if read_depth_data else 0
highest_read_depth = max(read_depth_data) if read_depth_data else 0

# Convert data to pandas DataFrame for easy handling
read_depth_stats_df = pd.DataFrame({
    'Metric': ['Average', 'Lowest', 'Highest'],
    'Value': [average_read_depth, lowest_read_depth, highest_read_depth]
})

# Save read depth statistics to CSV
bam_file_name = os.path.basename(bam_file).split('.')[0]
read_depth_stats_csv_path = os.path.join(save_data_path, f'{bam_file_name}_read_depth_stats.csv')
read_depth_stats_df.to_csv(read_depth_stats_csv_path, index=False)

# Plotting read depth
plt.figure(figsize=(12, 6))
plt.plot(read_depth_data, color='blue', linewidth=0.5)
plt.xlabel('Genomic Position')
plt.ylabel('Read Depth')
plt.title(f'Read Depth Distribution of {bam_file_name}')
read_depth_plot_path = os.path.join(save_graph_path, f'{bam_file_name}_read_depth.png')
plt.savefig(read_depth_plot_path)

print(f"Read depth plot saved at: {read_depth_plot_path}")
print(f"Read depth statistics saved at: {read_depth_stats_csv_path}")
