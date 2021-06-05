> setwd("~/Desktop/data analysis")
> earnings = read.delim("graduate-earnings.txt", header = TRUE)
> attach(earnings)
> plot(earnings$Price, earnings$Earn, xlab='price', ylab='earning', main='earn and price scatter plot', 
pch=19)
> points(earnings$Price[earnings$Public=="0"], earnings$Earn[earnings$Public=="0"], pch=19, 
col="darkturquoise")
> points(earnings$Price[earnings$Public=="1"], earnings$Earn[earnings$Public=="1"], pch=19, 
col="darkseagreen3")
> legend("topleft", pch=19, col=c("darkturquoise", "darkseagreen3"), c("Private school", "Public 
school"))
> barplot(table(cut(earnings$Price, breaks = seq(0,75000, by = 5000))))
> barplot(table(cut(earnings$Earn, breaks = seq(0,75000, by = 5000))))
> summary(lm(earnings$Earn~earnings$Price))
Call:
lm(formula = earnings$Earn ~ earnings$Price)
Residuals:
 Min 1Q Median 3Q Max 
-16905.1 -4183.1 -921.5 3217.7 30777.6 
Coefficients:
 Estimate Std. Error t value Pr(>|t|) 
(Intercept) 4.042e+04 6.951e+02 58.150 < 2e-16 ***
earnings$Price 1.227e-01 1.544e-02 7.948 7.55e-15 ***
---
Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
Residual standard error: 6446 on 704 degrees of freedom
Multiple R-squared: 0.08234, Adjusted R-squared: 0.08103 
F-statistic: 63.17 on 1 and 704 DF, p-value: 7.552e-15
> splitearnings=split(earnings,earnings$public)
> publicschools=splitearnings[1]
> privateschools=splitearnings[2]
> boxplot(earnings$ratio~earnings$Public, xlab=c("private public"), ylab='earning to price ratio', 
main='earning to price ratio')
