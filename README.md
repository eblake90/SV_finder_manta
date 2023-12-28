# SV Finder using Manta


<!-- ABOUT THE PROJECT -->
## About The Project

This repository uses manta as an SV caller and visualises the results via graph and samplots.

<!-- GETTING STARTED -->
## Getting Started

The following section helps you get up and running with the project


### Installation


1. Clone the repo
   ```sh
   git clone git@github.com:eblake90/SV_finder_manta.git
   ```
2. Install conda environment
   ```sh
   conda env install -f environment.yml
   
   conda activate SV_finder_manta
   ```
## Running
First make sure you are running in python 2.7.18

## Inputting data for Manta:
```shell
cd /home/eblake/Documents/manta/working_manta/manta

# Locate your bam file that needs analysis (will be added to share folder)
ln -s /home/eblake/Documents/manta/working_manta/Data/Data_to_analysis/G15512.HCC1954.1.COST16011_region.bam 
```
Next go into configManta.py.ini and change the reference "referenceFasta = /../../refgenome.fa" to the path of your reference genome (.fa)
```shell
# Creating a workflow run script by inputting the paths of the following: configManta.py, configManta.py.ini and .bam
/home/eblake/Documents/manta/working_manta/manta/bin/configManta.py --config /home/eblake/Documents/manta/working_manta/manta/bin/configManta.py.ini --bam /home/eblake/Documents/manta/working_manta/Data/Data_to_analysis/G15512.HCC1954.1.COST16011_region.bam
```
If successful the following output will be:
```shell
Successfully created workflow run script.
To execute the workflow, run the following script and set appropriate options:

/home/eblake/Documents/manta/working_manta/manta/MantaWorkflow/runWorkflow.py
```
Run the path:
```shell
/home/eblake/Documents/manta/working_manta/manta/MantaWorkflow/runWorkflow.py
```
After this the following folders will be populated:
```shell
/home/eblake/Documents/manta/working_manta/manta/MantaWorkflow/results/stats
```
## alignmentStatsSummary.txt 
This file provides statistics for a BAM file, detailing the distribution of fragment lengths for paired-end reads, as well as counts of various types of reads including those with low mapping quality (MAPQ).

## svCandidateGenerationStats.tsv 
This file is a detailed report from a structural variant analysis tool, describing the efficiency and results of processing various types of genomic data edges (AllEdges, RemoteEdges, SelfEdges) with statistics on runtime, the number of candidates, junction counts, assembly candidates, and filters applied.

## svCandidateGenerationStats.xml 
This contains detailed statistics about the processing of genomic data edges (both self and remote edges), including time spent on various stages (like candidate determination, assembly, and scoring), counts of different types of edges and junctions, and information on filters applied during the analysis.

## svLocusGraphStats.tsv 
This report summarizes the time spent and characteristics of a structural variant analysis graph, including build time, node and edge counts, and detailed filtering statistics for a genomic sample.

```shell
/home/eblake/Documents/manta/working_manta/manta/MantaWorkflow/results/variants
```
## candidateSmallIndels.vcf.gz 
Subset of the candidateSV.vcf.gz file containing only simple insertion and deletion variants less than the minimum scored variant size (50 by default). Passing this file to a small variant caller will provide continuous coverage over all indel sizes when the small variant caller and manta outputs are evaluated together. Alternate small indel candidate sets can be parsed out of the candidateSV.vcf.gz file if this candidate set is not appropriate.

## candidateSV.vcf.gz
Unscored SV and indel candidates. Only a minimal amount of supporting evidence is required for an SV to be entered as a candidate in this file. An SV or indel must be a candidate to be considered for scoring, therefore an SV cannot appear in the other VCF outputs if it is not present in this file. Note that by default this file includes indels of size 8 and larger. The smallest indels in this set are intended to be passed on to a small variant caller without scoring by manta itself (by default manta scoring starts at size 50).

## diploidSV.vcf.gz
SVs and indels scored and genotyped under a diploid model for the set of samples in a joint diploid sample analysis or for the normal sample in a tumor/normal subtraction analysis. In the case of a tumor/normal subtraction, the scores in this file do not reflect any information from the tumor sample.

## somaticSV.vcf.gz
SVs and indels scored under a somatic variant model. This file will only be produced if a tumor sample alignment file is supplied during configuration

Creating Variant Distribution Plot using VD_plots.py
Prepare the data in path:
```shell
/home/eblake/Documents/manta/working_manta/results/Data
```
Decompress and move files using the follow:
```shell
 python /home/eblake/Documents/manta/SV_finder_manta/results/vcfgz_to_vcf.py
```
### Now comparing the manta SV findings with the expected results (if present):
First go into /home/eblake/Documents/manta/working_manta/results/compareSV.py and change the paths relative to your .bam, results.vcf and expected_results.vcf files
Next run:
``` shell
python /home/eblake/Documents/manta/working_manta/results/compareSV.py
```
Once done you can view the results in the result folder.

## SamPlot
To run samplot use this following:
Go into /home/eblake/Documents/manta/working_manta/results/samplot.py and change the relevent paths of inputs and outputs

```shell
cd samplot
python3.8 -m venv samplot_env
source samplot_env/bin/activate
pip install -r requirements.txt
python setup.py install
samplot --version
python /home/eblake/Documents/manta/working_manta/results/samplot.py
```
The results can be found here:
```shell
/home/eblake/Documents/manta/working_manta/results/Data/samplot_output
```










