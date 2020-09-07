#! /bin/env Rscript
library(ggplot2)
library(reshape)
library(ranger)

stats<-commandArgs(trailingOnly=T)[[1]]
df<-read.csv(stats, header=F)
colnames(df) <-
	c('problem_name','age_prob','proved','init_clauses','init_lengths','init_weights','processed')

max_processed<-aggregate(processed ~ problem_name, df, max)
colnames(max_processed)[2]<-'max_processed'
df<-merge(df,max_processed)
# remove problems never proved
df<-df[df$max_processed > 0,]
# when processed is 0, processed is 2 * max_processed
df$processed<-ifelse(df$processed > 0, df$processed, 2*df$max_processed)

model <- ranger(
	processed ~ age_prob + init_clauses + init_lengths + init_weights,
	data = df, num.trees=1000, importance = 'impurity')
