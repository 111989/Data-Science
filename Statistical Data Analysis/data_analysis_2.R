Call:
lm(formula = SAT ~ Price + merit_aided)
Residuals:
 Min 1Q Median 3Q Max 
-330.43 -80.15 -3.39 77.16 305.51 
Coefficients: Estimate Std. Error t value Pr(>|t|) 
(Intercept) 9.858e+02 1.296e+01 76.063 <2e-16 ***
Price 3.443e-03 3.219e-04 10.699 <2e-16 ***
merit_aided 3.387e+01 4.647e+01 0.729 0.466 
---
Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
Residual standard error: 113.4 on 642 degrees of freedom
 (61 observations deleted due to missingness)
Multiple R-squared: 0.1883, Adjusted R-squared: 0.1857 
F-statistic: 74.44 on 2 and 642 DF, p-value: < 2.2e-16
Call:
lm(formula = Earn ~ SAT + ACT)
Residuals:
 Min 1Q Median 3Q Max 
-15689.4 -3542.0 -278.7 3132.2 24360.7 
Coefficients:
 Estimate Std. Error t value Pr(>|t|) 
(Intercept) 15508.123 1801.657 8.608 < 2e-16 ***
SAT 15.154 4.374 3.464 0.000564 ***
ACT 511.855 173.103 2.957 0.003211 ** 
---
Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
Residual standard error: 5572 on 703 degrees of freedom
Multiple R-squared: 0.3152, Adjusted R-squared: 0.3132 
F-statistic: 161.8 on 2 and 703 DF, p-value: < 2.2e-16
Call:
lm(formula = SAT ~ merit_aided + Price_with_aid)
Residuals:
 Min 1Q Median 3Q Max 
-302.81 -81.69 -11.83 70.82 364.69 
Coefficients:
 Estimate Std. Error t value Pr(>|t|) 
(Intercept) 1.003e+03 1.402e+01 71.510 < 2e-16 ***
merit_aided 3.195e+01 5.078e+01 0.629 0.53 
Price_with_aid 5.357e-03 6.581e-04 8.139 2.07e-15 ***
---
Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
Residual standard error: 117.1 on 642 degrees of freedom
 (61 observations deleted due to missingness)
Multiple R-squared: 0.133, Adjusted R-squared: 0.1303 
F-statistic: 49.24 on 2 and 642 DF, p-value: < 2.2e-16
Call:
lm(formula = Price_with_aid ~ merit_aided + Price)
Residuals:
 Min 1Q Median 3Q Max -19036.1 -2285.0 199.8 2317.9 16857.7 
Coefficients:
 Estimate Std. Error t value Pr(>|t|) 
(Intercept) 3.753e+03 4.348e+02 8.631 <2e-16 ***
merit_aided 1.381e+04 1.559e+03 8.859 <2e-16 ***
Price 4.250e-01 1.080e-02 39.357 <2e-16 ***
---
Signif. codes: 0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
Residual standard error: 3803 on 642 degrees of freedom
 (61 observations deleted due to missingness)
Multiple R-squared: 0.7859, Adjusted R-squared: 0.7852 
F-statistic: 1178 on 2 and 642 DF, p-value: < 2.2e-16
> step(fit_before_no_NA,direction="backward")
Start: AIC=10901.54
y ~ x1 + x2 + x3 + x4 + x5 + x6 + x7
 Df Sum of Sq RSS AIC
- x2 1 8692 1.5209e+10 10900
- x5 1 4549300 1.5213e+10 10900
- x7 1 7964289 1.5217e+10 10900
<none> 1.5209e+10 10902
- x3 1 214221235 1.5423e+10 10908
- x6 1 339325275 1.5548e+10 10914
- x4 1 1175270813 1.6384e+10 10947
- x1 1 1309537107 1.6518e+10 10952
Step: AIC=10899.54
y ~ x1 + x3 + x4 + x5 + x6 + x7
 Df Sum of Sq RSS AIC
- x5 1 4544792 1.5213e+10 10898
- x7 1 8044855 1.5217e+10 10898
<none> 1.5209e+10 10900
- x6 1 343336237 1.5552e+10 10912
- x3 1 756775161 1.5966e+10 10929
- x4 1 1203814650 1.6413e+10 10946
- x1 1 1336748902 1.6546e+10 10952
Step: AIC=10897.73
y ~ x1 + x3 + x4 + x6 + x7
 Df Sum of Sq RSS AIC
- x7 1 14124811 1.5228e+10 10896
<none> 1.5213e+10 10898
- x6 1 338898169 1.5552e+10 10910
- x3 1 783856540 1.5997e+10 10928
- x1 1 1336485748 1.6550e+10 10950- x4 1 1731663593 1.6945e+10 10965
Step: AIC=10896.32
y ~ x1 + x3 + x4 + x6
 Df Sum of Sq RSS AIC
<none> 1.5228e+10 10896
- x6 1 327506009 1.5555e+10 10908
- x3 1 770046199 1.5998e+10 10926
- x1 1 1517503539 1.6745e+10 10955
- x4 1 1763550039 1.6991e+10 10965
Call:
lm(formula = y ~ x1 + x3 + x4 + x6, data = DATA_noNA)
Coefficients:
(Intercept) x1 x3 x4 x6 
21916.8537 7966.0722 494.8219 0.2746 -5997.2193
> shapiro.test(y.res)
Shapiro-Wilk normality test
data: y.res
W = 0.96031, p-value = 3.851e-12
