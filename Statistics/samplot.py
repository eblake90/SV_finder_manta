import subprocess
import os
import argparse

def run_samplot(vcf_path, bam_path, output_dir, tag):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(vcf_path, 'r') as vcf_file:
        for line in vcf_file:
            if line.startswith('#'):
                continue

            columns = line.strip().split('\t')
            chrom, pos, sv_id, ref, alt, _, _, info = columns[:8]
            info_dict = {k: v for k, v in (field.split('=') for field in info.split(';') if '=' in field)}

            sv_type = info_dict.get('SVTYPE', 'UNK')
            end = info_dict.get('END', pos)

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

            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Samplot for VCF and BAM files.')
    parser.add_argument('--vcf', required=True, help='Path to the VCF file')
    parser.add_argument('--bam', required=True, help='Path to the BAM file')
    parser.add_argument('--output', required=True, help='Path to the output directory')
    args = parser.parse_args()

    run_samplot(args.vcf, args.bam, args.output, "output")
