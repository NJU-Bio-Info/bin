######## remove ensembl id version infor #######
# @Author: Kun-Ming Shui
# @Last Update: 2023/11/21

cut_version <- function(genes) gsub(pattern = '\\.[0-9]+', replacement = '', x = genes, perl = TRUE)