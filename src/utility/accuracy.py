Accuracy1 = 0.8217626136213932
Accuracyx = 0.7967329732578052
Accuracy2 = 0.839942036622316
mean_acc = (Accuracy1+Accuracy2+Accuracyx)/3
n_H = mean_acc/Accuracy1
n_A = mean_acc/Accuracy2
n_D = mean_acc/Accuracyx
p_H = (mean_acc + n_H)/2
p_A = (mean_acc + n_A)/2
p_D = (mean_acc + n_D)/2