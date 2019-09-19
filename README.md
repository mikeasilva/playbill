Playbill Data Analysis
================
Michael Silva
2019-09-19

# Motivation

As part of my CUNY SPS Masters in Data Science training I took a
Business Analytics course. We use Simon Shealther’s *A Modern Approach
to Regression with R* in the class. In chapter 2 he introduces the topic
of simple linear regression. In the excercise section of that chapter he
uses data on gross revenue from broadway shows as collected by playbill.
He gives the following visualization for the week ending 2004-10-17:

![](README_files/figure-gfm/figure-1-1.png)<!-- -->

They say there is a rule of thumb that the previous week’s revenue is a
good predictor of the current week’s. The exercise asks you to examine
this claim with the data. As I worked through this question I was
suprised to find that the the previous week’s revenue really was a good
predictor of the current week’s.

However, something didn’t sit right with me. The conclusion seemed to
defy logic. If the current week’s revenue is predicted by the previous
week’s, then there is basically no change in how much a show makes over
time. That did not make any sense. I began to wonder if the authors
cherry-picked the data for the purpose of the exercise and if the trend
wouldn’t hold if a different week was examined.

# Data Acquisition

I scrapped playbill.com’s website to collect the gross box office
results for all possible years. The data goes back to as far as 1985 and
can continue to be scrapped. At the time of this analysis the data goes
up to 2019-09-15. After exploring the data, I compiled a dataset
matching what the author produced. No data was excluded from my dataset.
In all there is 45450 weeks worth of data.

# Does the Previous Week Predict the Current Week?

So does the previous week’s revenue predict the current week? I looked
deeper into the question. Here’s what I discovered:

The first thing I discovered is that the author threw out data from 5
shows (Brooklyn, I Am My Own Wife, Marc Salem’s Mind Games on Broadway,
Reckless, and Twelve Angry Men). They didn’t explain this nor their
reasoning. So the chart should have looked like this:

![](README_files/figure-gfm/figure-2-1.png)<!-- -->

Hmmm. Now there are 121 times the current or prevous week is zero. Let’s
eliminate these cases from the data set.

``` r
playbill <- playbill %>%
  filter(current_week > 0 & past_week > 0)
```

Now let’s look at the complete dataset. We will look at the rule of
thumb (last week predicts this week) and the linear regression line
(since that is what the textbook is about).

![](README_files/figure-gfm/figure-3-1.png)<!-- -->

There is definately a positive correlation between the previous and
current week’s boxoffice revenue. The regression line (blue line above)
is similar to the rule of thumb line (in red).

# Appendix

## Linear Regression Models

### Textbook Model

This model uses the textbook’s dataset

``` r
textbook <- playbill %>%
  filter(week_ending == "2004-10-17") %>%
  filter(!show %in% excluded) %>%
  lm(current_week ~ past_week, data = .)
summary(textbook)
```

``` 

Call:
lm(formula = current_week ~ past_week, data = .)

Residuals:
   Min     1Q Median     3Q    Max 
-36926  -7525  -2581   7782  35443 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 6.805e+03  9.929e+03   0.685    0.503    
past_week   9.821e-01  1.443e-02  68.071   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 18010 on 16 degrees of freedom
Multiple R-squared:  0.9966,    Adjusted R-squared:  0.9963 
F-statistic:  4634 on 1 and 16 DF,  p-value: < 2.2e-16
```

### Textbook Model (All Datapoints)

``` r
textbook_all <- playbill %>%
  filter(week_ending == "2004-10-17") %>%
  lm(current_week ~ past_week, data = .)
summary(textbook_all)
```

``` 

Call:
lm(formula = current_week ~ past_week, data = .)

Residuals:
   Min     1Q Median     3Q    Max 
-66882 -10036    989  11527  44544 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 2.405e+03  1.010e+04   0.238    0.814    
past_week   9.872e-01  1.636e-02  60.352   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 24890 on 21 degrees of freedom
Multiple R-squared:  0.9943,    Adjusted R-squared:  0.994 
F-statistic:  3642 on 1 and 21 DF,  p-value: < 2.2e-16
```

### All Data Model

This model uses all the data except those observations with zero dollars
in the previous or current week.

``` r
all_data <- playbill %>%
  lm(current_week ~ past_week, data = .)
summary(all_data)
```

``` 

Call:
lm(formula = current_week ~ past_week, data = .)

Residuals:
     Min       1Q   Median       3Q      Max 
-2003649   -35721    -6424    29754  1573960 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 2.456e+04  8.777e+02   27.99   <2e-16 ***
past_week   9.651e-01  1.218e-03  792.18   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 113000 on 45300 degrees of freedom
Multiple R-squared:  0.9327,    Adjusted R-squared:  0.9327 
F-statistic: 6.276e+05 on 1 and 45300 DF,  p-value: < 2.2e-16
```
