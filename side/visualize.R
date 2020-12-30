#! /bin/env Rscript
library(ggplot2)
library(reshape)

problem<-commandArgs(trailingOnly=T)[[1]]
df<-read.csv(problem, header=F)
colnames(df) <- c('user_time', 'processed_clauses', 'age_weight_ratio')
p=strsplit(problem, '/')[[1]]
problem_name = p[[length(p)]]
df$step<-seq(nrow(df))
ggplot(df, aes(x=step, y=processed_clauses)) +
	geom_point(aes(color=age_weight_ratio),size=1,alpha=1) +
	#geom_hline(yintercept=mean(df$initial), color='orange', size=1, alpha=0.4) +
	#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1), expand=c(0,0)) +
	#scale_y_continuous(limits = c(0, NA), expand=c(0,0)) +
	#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1)) +
	#scale_y_continuous(limits = c(0, NA)) +
	ggtitle(problem_name)
ggsave(paste(problem, '.png', sep=''), device='png', width=9, heigh=6)
