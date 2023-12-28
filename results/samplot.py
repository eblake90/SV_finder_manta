import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def run_samplot(vcf_path, bam_path, output_dir, tag):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(vcf_path, 'r') as vcf_file:
        for line in vcf_file:
            if line.startswith('#'):
                continue  # Skip header lines

            columns = line.strip().split('\t')
            chrom, pos, sv_id, ref, alt, _, _, info = columns[:8]
            info_dict = {k: v for k, v in (field.split('=') for field in info.split(';') if '=' in field)}

            sv_type = info_dict.get('SVTYPE', 'UNK')
            end = info_dict.get('END', pos)

            # Constructing samplot command
            output_file = f"{output_dir}/{tag}_{sv_id}_{chrom}_{pos}_{end}.png"
            cmd = [
                "samplot", "plot",
                "-n", sv_id,
                "-b", bam_path,
                "-o", output_file,
                "-c", chrom,
                "-s", pos,
                "-e", end,
                "-t", sv_type
            ]

            # Run samplot command
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)

# Define paths
candidate_vcf_path = "/home/eblake/Documents/manta/working_manta/results/Data/candidateSV.vcf"
somatic_vcf_path = "/home/eblake/Documents/manta/working_manta/results/Data/somaticSV.vcf"
bam_path = "/home/eblake/Documents/manta/working_manta/Data/Data_to_analysis/G15512.HCC1954.1.COST16011_region.bam"
output_dir = "/home/eblake/Documents/manta/working_manta/results/Data/samplot_output"

# Run for both VCF files
run_samplot(candidate_vcf_path, bam_path, output_dir, "candidate")
run_samplot(somatic_vcf_path, bam_path, output_dir, "somatic")


