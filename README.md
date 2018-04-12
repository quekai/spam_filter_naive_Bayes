# spam_filter_naive_bayes
###spam filter use naive-bayes

####使用最大似然估计
判断 P(spam) 和 P(ham) 的大小
化简可得：  
    只要比较 P(S)+\prod P(S|W) 和 P(H)+\prod P(H|W) 的大小  
    P(S)， P(H) 是先验概率 (在程序中我设定为0.5)  
####为避免乘积的下溢出问题，取log，比较大小

####计算频数时，我选用伯努利方法，即只判断单词在邮件中是否出现

####频数为0时，会引发计算错误，我把频数默认值设为1:  
    使用defaultdict(lambda: 1) ，当查询未设定value或字典中没有的key时可以返回1  
    例如：dict[('who','ham')] = 20 已设定频数，  
          当要查询dict['who','spam'] 时， 由于改值未设定，会返回1  
          意思是该词是spam邮件特征的可能性很低  
          （网上也有直接设定这种情况下P(S|W)为0.4的，读者可自行考虑） 

####此外，当P(S|W) 或 P(H|W) 为 1时，也会出现计算错误，在这里我把频数 = spam邮件数 或 ham邮件数 的情况减一
