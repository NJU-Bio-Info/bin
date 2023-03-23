#!/usr/local/bin/Rscript

#--
#@Author: Kun-Ming Shui, School of Life Sciences, Nanjing University (NJU).
#@Contribution list: ...

suppressMessages(library(argparse))
suppressMessages(library(ggplot2))
suppressMessages(library(patchwork))
suppressMessages(library(pheatmap))
suppressMessages(library(tidyr))
suppressMessages(library(dplyr))
suppressMessages(library(purrr))
suppressMessages(library(forcats))

parser <- ArgumentParser(prog = 'deeptools2r.R',
			 description = 'This tool can help you visualize deeptools computeMatrix output in R.',
			 epilog = 'Kun-Ming Shui, skm@smail.nju.edu.cn')

parser$add_argument('--version', '-v', action = 'version', version = '%(prog)s 1.0.0')
parser$add_argument('--input', '-i', nargs = '+', help = 'the complexHeatmap output file, multiple files should be separated by spaced.', required = TRUE)
parser$add_argument('--output', '-o', help = 'the output file name, "deeptools2r.out.pdf" by default.', default = 'deeptool2r.out.pdf')
parser$add_argument('--averageType', '-t', help = 'the type of stastics should be used for the profile, "mean" by default.', default = 'mean', choices = c('mean', 'max', 'min', 'median', 'sum'))
parser$add_argument('--plotType', help = 'the plot type for profile, "line" by default.', default = 'line', choices = c('line', 'heatmap', 'both'))
parser$add_argument('--colors', nargs = '+', help = 'the colors used for plot lines, multiple colors should be separated by spaced and should be equal with group information size, "None" by default.', default = NULL, required = FALSE)
parser$add_argument('--group', '-g', nargs = '+', help = 'group information for INPUT FILE, an important function of this tool is to combine profile data from forward and reverse strand. For example, if you have the file list: r1.fwd.tab r1.rev.tab r2.tab, you should pass "-g r1_f r1_r r2" to this argument. All in all, profile data from one sample but different strand should be taged with same group but different strand.', required = TRUE)
parser$add_argument('--startLabel', help = '[Only for scale-regions mode] Label shown in the plot for the start of the region, "TSS" by default.', default = 'TSS', required = FALSE)
parser$add_argument('--endLabel', help = '[Only for scale-regions mode] Label shown in the plot for the end of the region, "TES" by default.', default = 'TES', required = FALSE)
parser$add_argument('--refPointLabel', help = '[Only for reference-point mode] Label shown in the plot for the center of the region', default = 'center', required = FALSE)
parser$add_argument('--yMax', help = 'Maximum value for Y-axis, NA by default.', type = 'double', default = NULL, required = FALSE)
parser$add_argument('--yMin', help = 'Minimum value for Y-axis, NA by default.', type = 'double', default = NULL, required = FALSE)
parser$add_argument('--width', help = 'Width value for line plot, 0.7 by default', type = 'double', default = 0.7, required = FALSE)
parser$add_argument('--plotHeight', help = 'Plot height in inch, 5 by default.', default = 5, type = 'double', required = FALSE)
parser$add_argument('--plotWidth', help = 'Plot width in inch, 7 by default.', default = 7, type = 'double', required = FALSE)

args <- parser$parse_args()

groups <- args$group
FILES <- args$input

#--group information
if(length(groups) != length(FILES)) stop('The group information does not equal with sample number.')
#-group level
gp.level <- sapply(groups, FUN = function(group){
	if(grepl(group, pattern = '[f|r]$')){
		str_list <- strsplit(group, split = "_", fixed = T)
		return(paste(str_list[[1]][1:(length(str_list[[1]])-1)], collapse = "_"))
	}else{
		return(group)
	}
})
gp.level <- unique(gp.level)

#--load data
data <- lapply(FILES, FUN = function(FILE){
	       tmp <- read.table(file = FILE, header = FALSE, sep = "\t", skip = 3)
	       gp <- groups[FILES == FILE]
	       gp.info <- ifelse(grepl(gp, pattern = '_[r|f]$'), 
				 gp %>% strsplit(., split = '_', fixed = TRUE) %>% unlist() %>% .[1:(length(.)-1)] %>% paste(., collapse = '_'),
				 gp)
	       tmp %>% mutate(group = rep(gp.info, nrow(tmp)))
})
data <- purrr::reduce(data, rbind)

#--tidy data
data <- data %>% 
  group_by(group) %>% 
  summarise_all(args$averageType, na.rm = TRUE) %>% 
  pivot_longer(cols = starts_with('V'), names_to = 'index', values_to = 'signal')

#--label
label.info <- read.table(file = FILES[1], comment.char = "", nrows = 2, fill = TRUE)
#-downstream
dw.size <- label.info[2, ] %>% 
	grep(pattern = 'downstream', value = T) %>% 
	gsub(pattern = '#', replacement = "") %>% 
	strsplit(split = ':', fixed = T) %>% 
	sapply('[[', 2) %>% 
	as.numeric()
#-upstream
up.size <- label.info[2, ] %>% 
	grep(pattern = 'upstream', value = T) %>% 
	gsub(pattern = '#', replacement = "") %>% 
	strsplit(split = ':', fixed = T) %>% 
	sapply('[[', 2) %>% 
	as.numeric()
#-body
bd.size <- label.info[2, ] %>% 
	grep(pattern = 'body', value = T) %>% 
	gsub(pattern = '#', replacement = "") %>% 
	strsplit(split = ':', fixed = T) %>% 
	sapply('[[', 2) %>% 
	as.numeric()
#-bin
binSize <- label.info[2, ] %>%
	grep(pattern = 'size', value = T) %>%
	gsub(pattern = '#', replacement = "") %>%
	strsplit(split = ':', fixed = T) %>%
	sapply('[[', 2) %>%
	as.numeric()

#--plot
line_plot <- data %>%
	mutate(index = fct_relevel(index, paste0('V', 1:((up.size + bd.size + dw.size)/binSize))),
	       group = fct_relevel(group, gp.level)) %>%
	ggplot(., aes(x = index, y = signal)) +
	geom_line(aes(group = group, color = group), linewidth = args$width) +
	xlab(label = 'Position') +
	ylab(label = 'Signal') +
	theme_classic() +
	theme(axis.text = element_text(family = 'sans', color = 'black'),
	      axis.ticks = element_line(color = 'black'),
	      axis.title = element_text(family = 'sans', face = 'bold'))

#-label
if(bd.size != 0){
	startLabel <- ifelse(is.null(args$startLabel), 'TSS', args$startLabel)
	endLabel <- ifelse(is.null(args$endLabel), 'TSS', args$endLabel)
	breakPoints <- c('V1', paste0('V', c(up.size/binSize, (up.size + bd.size)/binSize)), paste0('V', (up.size + bd.size + dw.size)/binSize))
	line_plot <- line_plot + 
		scale_x_discrete(breaks = breakPoints, labels = c(paste0("-", up.size/1000, ' kb'), startLabel, endLabel, paste0(dw.size/1000, ' kb')))
}else{
	refPointLabel <- ifelse(is.null(args$refPointLabel), 'center', args$refPointLabel)
	breakPoints <- c('V1', paste0('V', up.size/binSize), paste0('V', (up.size + dw.size)/binSize))
	line_plot <- line_plot +
		scale_x_discrete(breaks = breakPoints, labels = c(paste0("-", up.size/1000, ' kb'), refPointLabel, paste0(dw.size/1000, ' kb')))
}

#--Y-region
if(!is.null(args$yMin) && !is.null(args$yMax)){
	line_plot <- line_plot + 
		coord_cartesian(ylim = c(args$yMin, args$yMax))
}

#--colors
if(!is.null(args$colors) && (length(args$colors) == length(gp.level))){
	line_plot <- line_plot + 
		scale_color_manual(values = args$colors)
}else if(!is.null(args$colors) && (length(args$colors) != length(gp.level))){
	print("Warning: Your color number doesn't match group number, use default set instead!")
}

plot <- line_plot
ggsave(filename = args$output, plot = plot, width = args$plotWidth, height = args$plotHeight, units = 'in')

cat(paste0('Finished at ', date(), '!\n'))
q(save = 'no')
