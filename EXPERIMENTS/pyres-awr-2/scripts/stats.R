#! /bin/env Rscript
library(ggplot2)
library(reshape)

problem<-commandArgs(trailingOnly=T)[[1]]
df<-read.csv(problem, header=F)
colnames(df) <- c('age_prob', 'proved', 'processed', 'resolutions', 'initial', 'proof_length')
p=strsplit(problem, '/')[[1]]
df$proof_length <- factor(df$proof_length)
problem_name = p[[length(p)]]
ggplot(df, aes(x=age_prob, y=processed)) +
	geom_point(aes(color=proof_length),size=0.8,alpha=0.5) +
	#geom_hline(yintercept=mean(df$initial), color='orange', size=1, alpha=0.4) +
	#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1), expand=c(0,0)) +
	#scale_y_continuous(limits = c(0, NA), expand=c(0,0)) +
	scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1)) +
	scale_y_continuous(limits = c(0, NA)) +
	ggtitle(problem_name)
ggsave(paste(problem, '.png', sep=''), device='png', width=9, heigh=6)
