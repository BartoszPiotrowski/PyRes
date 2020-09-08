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

test.probs <- sample(df$problem_name, 30)
df.test<-df[df$problem_name %in% test.probs,]
df.train<-df[!(df$problem_name %in% test.probs),]

#ggplot(df, aes(x=age_prob, y=processed, color=problem_name)) +
#	geom_point(aes(color=proved), size=0.4,alpha=0.7) +
#	geom_smooth(size=0.3, alpha=0.3, se=F) +
#	scale_y_log10() +
#	theme(legend.position="none")
#	#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1), expand=c(0,0)) +
#	#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1)) +
#	#scale_y_continuous(limits = c(0, NA)) +
#ggsave(paste(stats, '.png', sep=''), device='png', width=24, heigh=16)

model <- ranger(
	processed ~ age_prob + init_clauses + init_lengths + init_weights,
	data = df.train, num.trees=1000, importance = 'impurity')

df.test$predicted_processed<-predict(model, df.test)$predictions

for (prob in test.probs){
	df.prob<-df.test[df.test$problem_name==prob,]
	df.prob<-melt(df.prob,
				  id.vars=c("age_prob", "proved"),
				  measure.vars=c("processed", "predicted_processed"))
	ggplot(df.prob, aes(x=age_prob, y=value)) +
		geom_point(aes(color=variable, shape=proved)) +
		#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1), expand=c(0,0)) +
		#scale_x_continuous(limits=c(0,1), breaks = seq(0,1,0.1)) +
		#scale_y_continuous(limits = c(0, NA)) +
	ggsave(paste(stats, '_', prob, '.png', sep=''), device='png', width=24, heigh=16)
}
