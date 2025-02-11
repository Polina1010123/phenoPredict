import pandas as pd
import gzip
import io

# loading data
with gzip.open('../data/data.MAF001.snps.vcf.recode.inputated.vcf.gz', 'rt') as f:
    lines = [line for line in f if line.startswith('#CHROM')]
header = pd.read_csv(io.StringIO(''.join(lines)), sep='\t')
columns = header.columns.tolist()

data = pd.read_csv('../data/data.MAF001.snps.vcf.recode.inputated.vcf.gz', comment = "#", sep = "\t", names=columns)
data_run = pd.read_csv('../data/run_ids.txt', sep='\t')
data_samples = pd.read_csv('../data/samples.list.txt', sep='\t', header = None)
data_csv = pd.read_csv("../data/41477_2022_1190_MOESM3_ESM.csv", sep = "\t", header=1)

# merging input data
data_merge = data_csv.merge(data_run, left_on='Inbred line name', right_on='Run title', how='outer')
name_samples = data_samples[0].to_list()
data_filtered = data_merge[data_merge['Accession'].isin(name_samples)]
data_phenotype = data_filtered[['Accession', 'Heterotic group']]
data_snp = data.iloc[:, 9:]
data_snp.index = data.iloc[:, 0]
data_snp = data_snp.T
data_snp.index.name = 'Accession'
data_snp_phenotype = data_snp.merge(data_phenotype, on="Accession", how="left")