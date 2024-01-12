# SV Finder using Manta


<!-- ABOUT THE PROJECT -->
## About The Project

This repository uses manta as an SV caller and visualises the results via graph and samplots.

<!-- GETTING STARTED -->
## Getting Started

The following section helps you get up and running with the project

---

# Installation


1. Clone the repo
   ```sh
   git clone git@github.com:eblake90/SV_finder_manta.git
   ```
2. Install conda environment
   ```sh
   conda env install -f environment_py3.yml
   conda env install -f environment_py27.yml
   ```
---   

# Running
First make sure you are running in python 2.7+

## Inputting data for Manta:
```shell
cd /home/eblake/Documents/manta/SV_finder_manta/manta
```

Locate your bam file that needs analysis (will be added to share folder)

``` shell
ln -s /path/to/.bam
```

Next go into configManta.py.ini and change the reference "referenceFasta = /../../refgenome.fa" to the path of your reference genome (.fa)


Creating a workflow run script by inputting the paths of the following: configManta.py, configManta.py.ini and .bam
```shell
/home/eblake/Documents/manta/SV_finder_manta/manta/bin/configManta.py --config /home/eblake/Documents/manta/SV_finder_manta/manta/bin/configManta.py.ini --bam /path/to/.bam
```

If successful the following output will be:
```shell
Successfully created workflow run script.
To execute the workflow, run the following script and set appropriate options:

/home/eblake/Documents/manta/SV_finder_manta/MantaWorkflow/runWorkflow.py
```
Run the path:
```shell
/home/eblake/Documents/manta/SV_finder_manta/MantaWorkflow/runWorkflow.py
```
After this the following folders will be populated:

---
```shell
/home/eblake/Documents/manta/SV_finder_manta/MantaWorkflow/stats
```

### alignmentStatsSummary.txt 
This file provides statistics for a BAM file, detailing the distribution of fragment lengths for paired-end reads, as well as counts of various types of reads including those with low mapping quality (MAPQ).

### svCandidateGenerationStats.tsv 
This file is a detailed report from a structural variant analysis tool, describing the efficiency and results of processing various types of genomic data edges (AllEdges, RemoteEdges, SelfEdges) with statistics on runtime, the number of candidates, junction counts, assembly candidates, and filters applied.

### svCandidateGenerationStats.xml 
This contains detailed statistics about the processing of genomic data edges (both self and remote edges), including time spent on various stages (like candidate determination, assembly, and scoring), counts of different types of edges and junctions, and information on filters applied during the analysis.

### svLocusGraphStats.tsv 
This report summarizes the time spent and characteristics of a structural variant analysis graph, including build time, node and edge counts, and detailed filtering statistics for a genomic sample.

---

```shell
/home/eblake/Documents/manta/SV_finder_manta/MantaWorkflow/variants
```
### candidateSmallIndels.vcf.gz 
Subset of the candidateSV.vcf.gz file containing only simple insertion and deletion variants less than the minimum scored variant size (50 by default). Passing this file to a small variant caller will provide continuous coverage over all indel sizes when the small variant caller and manta outputs are evaluated together. Alternate small indel candidate sets can be parsed out of the candidateSV.vcf.gz file if this candidate set is not appropriate.

### candidateSV.vcf.gz
Unscored SV and indel candidates. Only a minimal amount of supporting evidence is required for an SV to be entered as a candidate in this file. An SV or indel must be a candidate to be considered for scoring, therefore an SV cannot appear in the other VCF outputs if it is not present in this file. Note that by default this file includes indels of size 8 and larger. The smallest indels in this set are intended to be passed on to a small variant caller without scoring by manta itself (by default manta scoring starts at size 50).

### diploidSV.vcf.gz
SVs and indels scored and genotyped under a diploid model for the set of samples in a joint diploid sample analysis or for the normal sample in a tumor/normal subtraction analysis. In the case of a tumor/normal subtraction, the scores in this file do not reflect any information from the tumor sample.

### somaticSV.vcf.gz
SVs and indels scored under a somatic variant model. This file will only be produced if a tumor sample alignment file is supplied during configuration

---
# Usage of Statistics Folder

## compareSV.py

This tool processes VCF (Variant Call Format) and BAM (Binary Alignment Map) files to analyze structural variants (SVs). It provides visualizations of the structural variant types and read depth distributions, as well as saves the data in CSV format.

### Requirements

- Python 3.x
- Libraries: pandas, pysam, matplotlib, seaborn, reportlab

### Installation

Before running the script, ensure you have the required libraries installed. You can install them using pip:

```bash
pip install pandas pysam matplotlib seaborn reportlab
```

### Usage

Run the script from the command line by providing the necessary arguments. Here's the general format to run the script:

```bash
python sv_analysis.py --bam_file <path_to_bam_file> --vcf_file <path_to_vcf_file> [--expected_vcf_file <path_to_expected_vcf>] --output_folder <path_to_output_folder>
```

### Arguments

- `--bam_file`: Path to the BAM file.
- `--vcf_file`: Path to the VCF file.
- `--expected_vcf_file` (optional): Path to the expected results VCF file.
- `--output_folder`: Path to the folder where the output files will be saved.

### Output

The script will create two folders inside the specified output folder:

- `Data`: Contains CSV files with structural variant counts and read depth data.
- `Graphs`: Contains PNG files of the plotted graphs.

A PDF summary report is also generated in the output folder.

### Example

```bash
python sv_analysis.py --bam_file sample.bam --vcf_file sample.vcf --output_folder ./output
```

---

## genotyping.py
This script runs SVTyper to genotype SVs in a VCF file using a BAM file and a JSON library info file.

### How to Run

Use the following command to run the script:

```
python genotyping.py --vcf_path /path/to/vcf --bam_path /path/to/bam --json_path /path/to/json --output_folder /path/to/output/folder
```

- `--vcf_path`: Path to the VCF file.
- `--bam_path`: Path to the BAM file.
- `--json_path`: Path to the BAM file JSON info.
- `--output_folder`: Path to the output folder.

---

## samplot.py
This script runs Samplot for VCF and BAM files and generates output images.

### How to Run

Use the following command to run the script:

```
python run_samplot.py --vcf_path /path/to/.vcf --bam_path /path/to/.bam --output /path/to/outputfolder
```

- Replace `/path/to/.vcf` with the path to the VCF file.
- Replace `/path/to/.bam` with the path to the BAM file.
- Replace `/path/to/outputfolder` with the path to the directory where the output images will be saved.

---

# Usage of Converters

## fasta_to_fa.py
This script converts a FASTA file to an FA file.

### How to Run

```
python fasta_to_fa.py input.fasta output.fa
```

- Replace `input.fasta` with your input FASTA file.
- Replace `output.fa` with your desired output FA file name.


## fastq_to_bam.py
This script aligns reads to an indexed reference genome and processes the output to generate a BAM file.

### How to Run

```
python fastq_to_bam.py --ref_genome my.fa --fastq1 my1.fastq --fastq2 my2.fastq --output /myoutput
```

- `--ref_genome`: Path to the reference genome file (FASTA).
- `--fastq1`: Path to the first FASTQ file.
- `--fastq2`: Path to the second FASTQ file.
- `--output`: Path prefix for output files.

## indexing_ref_genome.py
This script indexes a reference genome and creates a .fa.fai file.

### How to Run

```
python indexing_ref_genome.py --ref_genome ref_genome.fa
```

- `--ref_genome`: Path to the reference genome file (FASTA).


## vcfgz_to_vcf.py
This script is used for unzipping `.vcf.gz` files from a source directory and moving them to a destination directory.

### How to Run

Use the following command to run the script:

```
python unzip_move_vcf.py --source_folder /path/to/source/folder --output_folder /path/to/output/folder
```

- Replace `/path/to/source/folder` with the path to the folder containing `.vcf.gz` files.
- Replace `/path/to/output/folder` with the path where you want the `.vcf` files to be saved.

 python /home/eblake/Documents/manta/SV_finder_manta/Statistics/newcompareSV.py --bam /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_200000rn_42s/output_fake_1000000_50v_150rl_200000rn_42s_sorted.bam --vcf /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_200000rn_42s/vcf/diploidSV.vcf --output /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_200000rn_42s/vcf
python /home/eblake/Documents/manta/SV_finder_manta/Statistics/samplot.py --vcf /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_333333rn_42s/vcf/diploidSV.vcf --bam /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_333333rn_42s/output_fake_1000000_50v_150rl_333333rn_42s_sorted.bam --output /home/eblake/Documents/github/1.1/artificial_ref-g_n_seq_generator/artificial_stuff/output_fake_1000000_50v_150rl_333333rn_42s/vcf/Graphs/samplots
