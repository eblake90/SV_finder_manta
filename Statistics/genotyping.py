import argparse
import svtyper.classic as svt

def run_svtyper(input_vcf, input_bam, library_info, output_vcf):
    with open(input_vcf, "r") as inf, open(output_vcf, "w") as outf:
        svt.sv_genotype(
            bam_string=input_bam,
            vcf_in=inf,
            vcf_out=outf,
            min_aligned=20,
            split_weight=1,
            disc_weight=1,
            num_samp=1000000,
            lib_info_path=library_info,
            debug=False,
            alignment_outpath=None,
            ref_fasta=None,
            sum_quals=False,
            max_reads=None,
            max_ci_dist=None
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SVTyper on VCF and BAM files.")
    parser.add_argument('--vcf_path', required=True, help='Path to the VCF file')
    parser.add_argument('--bam_path', required=True, help='Path to the BAM file')
    parser.add_argument('--json_path', required=True, help='Path to the BAM file JSON info')
    parser.add_argument('--output_folder', required=True, help='Path to the output folder')

    args = parser.parse_args()

    output_vcf = os.path.join(args.output_folder, "genotyped_output.vcf")
    run_svtyper(args.vcf_path, args.bam_path, args.json_path, output_vcf)
