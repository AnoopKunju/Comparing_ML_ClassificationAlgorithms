# -*- coding: utf-8 -*-
"""Comparing_Classification_Algorithm_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t45DYmkhb80dfBNdduoNEyi8e62Qdp1W

# Question 1
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
import xgboost as xgb

import warnings #suppressing future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data = pd.read_csv('/content/bank-additional-full.csv', sep= ';')
print("Shape of data : {}".format(data.shape))
print("Name of columns : {}".format(list(data.columns)))
data.head()

"""***Data Preprocessing***"""

#converting the target column to binary 
data['y'] = data.y.apply(lambda x:0 if x=='no' else 1)
display(data.head())
data.info()

#grouping basic- 9y,6y,4y into a single category 
data.education.replace(['basic.9y', 'basic.6y', 'basic.4y'], 'basic', inplace=True)
data['education'].unique()

#creating dummies
df = pd.get_dummies(data) 
display(df.head())

df.info()

# We observe that the categorical-columns consist of unknown data which is redundant
# so droping them before modeling
df.drop(list(df.filter(regex = '_unknown')), axis = 1, inplace = True)

"""***Data Scaling and Spliting*** """

#sliplting data and target
X = df.drop('y',axis = 1)
y = df['y']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state = 42,stratify= y)

#scaling the data using Standard Scalar
stdscaler = StandardScaler()
X_train_scal = stdscaler.fit_transform(X_train)
X_test_scal = stdscaler.fit_transform(X_test)

"""* **LOGISITIC REGRESSION** """

logReg = LogisticRegression(max_iter = 200,random_state= 42)
logReg.fit(X_train_scal,y_train)
y_pred_logReg = logReg.predict(X_test_scal)
#confusion matrix
confusion_mat_logReg= confusion_matrix(y_test, y_pred_logReg)
confusion_logReg = pd.DataFrame(confusion_mat_logReg, index=['Deposit Refused','Deposit Accepted'], columns=['Predicted Refusal','Predicted Acceptance'])
#classifcaiton report
cls_logReg =classification_report(y_test, y_pred_logReg,output_dict=True)

confusion_logReg

"""* **RANDOM FOREST** """

randF= RandomForestClassifier(random_state=42, n_estimators= 50) 
randF.fit(X_train_scal,y_train)
y_pred_randF =randF.predict(X_test_scal)
#confusion matrix
confusion_mat_randF= confusion_matrix(y_test, y_pred_randF)
confusion_randF = pd.DataFrame(confusion_mat_randF, index=['Deposit Refused','Deposit Accepted'], columns=['Predicted Refusal','Predicted Acceptance'])
#classifcaiton report
cls_randF =classification_report(y_test, y_pred_randF,output_dict=True)

confusion_randF

"""* **DECISION TREES**"""

decTree= DecisionTreeClassifier(random_state= 42)
decTree.fit(X_train_scal,y_train)
y_pred_decTree =decTree.predict(X_test_scal)
#confusion matrix
confusion_mat_decTree= confusion_matrix(y_test, y_pred_decTree)
confusion_decTree = pd.DataFrame(confusion_mat_decTree, index=['Deposit Refused','Deposit Accepted'], columns=['Predicted Refusal','Predicted Acceptance'])
#classifcaiton report
cls_decTree =classification_report(y_test, y_pred_decTree,output_dict=True)

confusion_decTree

"""* **XGBOOST**"""

xgb= xgb.XGBClassifier(max_depth = 10)
xgb.fit(X_train_scal,y_train)
y_pred_xgb =xgb.predict(X_test_scal)

#confusion matrix
confusion_mat_xgb= confusion_matrix(y_test, y_pred_xgb)
confusion_xgb = pd.DataFrame(confusion_mat_xgb, index=['Deposit Refused','Deposit Accepted'], columns=['Predicted Refusal','Predicted Acceptance'])
#classifcaiton report
cls_xgb =classification_report(y_test, y_pred_xgb,output_dict=True)

confusion_xgb

#function for creating a table with all metrics for easy comparison
def compare_metrics():
    metric_table = pd.DataFrame({'Logistic Regression':[cls_logReg['accuracy'],
                                                        cls_logReg['macro avg']['precision'],
                                                        cls_logReg['macro avg']['recall'],
                                                        cls_logReg['macro avg']['f1-score'],
                                                        cls_logReg['macro avg']['support']],
                                                                              
                                      'Random Forest':[cls_randF['accuracy'],
                                                      cls_randF['macro avg']['precision'],
                                                      cls_randF['macro avg']['recall'],
                                                      cls_randF['macro avg']['f1-score'],
                                                      cls_randF['macro avg']['support']],
                                 
                                      'Decision Tree':[cls_decTree['accuracy'],
                                                      cls_decTree['macro avg']['precision'],
                                                      cls_decTree['macro avg']['recall'],
                                                      cls_decTree['macro avg']['f1-score'],
                                                      cls_decTree['macro avg']['support']],
                                       
                                      'XGBoost':[cls_xgb['accuracy'],
                                                cls_xgb['macro avg']['precision'],
                                                cls_xgb['macro avg']['recall'],
                                                cls_xgb['macro avg']['f1-score'],
                                                cls_xgb['macro avg']['support']]},
                                      
                                      index=['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Support'])
    
    metric_table['Best Algorithm'] = metric_table.idxmax(axis=1)
    
    return(metric_table)

compare_metrics()

"""
## **Comparing the Algorithms**

***Comparison Table for metrics***
<table style="width: 611px; height: 166px;" border="1">
<tbody>
<tr style="height: 40px;">
<td style="width: 94px; height: 40px;">&nbsp;</td>
<td style="width: 103px; height: 40px;"><strong>Logistic Regression</strong></td>
<td style="width: 104.333px; height: 40px;"><strong>Random Forest</strong></td>
<td style="width: 81.6667px; height: 40px;"><strong>Decision Tree</strong></td>
<td style="width: 84px; height: 40px;"><strong>XGBoost</strong></td>
<td style="width: 143px; height: 40px;"><strong>Best Algorithm&nbsp;</strong></td>
</tr>
<tr style="height: 20px;">
<td style="width: 94px; height: 20px;"><strong>Accuracy</strong></td>
<td style="width: 103px; height: 20px;">&nbsp;0.911548</td>
<td style="width: 104.333px; height: 20px;">&nbsp;0.911953</td>
<td style="width: 81.6667px; height: 20px;">&nbsp;0.877640</td>
<td style="width: 84px; height: 20px;">&nbsp;0.909606</td>
<td style="width: 143px; height: 20px;">Random Forest</td>
</tr>
<tr style="height: 20px;">
<td style="width: 94px; height: 20px;"><strong>Precision</strong></td>
<td style="width: 103px; height: 20px;">&nbsp;0.801012</td>
<td style="width: 104.333px; height: 20px;">&nbsp;0.797810</td>
<td style="width: 81.6667px; height: 20px;">&nbsp;0.699454</td>
<td style="width: 84px; height: 20px;">&nbsp;0.777767</td>
<td style="width: 143px; height: 20px;">Logistic Regression</td>
</tr>
<tr style="height: 20px;">
<td style="width: 94px; height: 20px;"><strong>Recall</strong></td>
<td style="width: 103px; height: 20px;">&nbsp;0.696461</td>
<td style="width: 104.333px; height: 20px;">&nbsp;0.707351</td>
<td style="width: 81.6667px; height: 20px;">&nbsp;0.719376</td>
<td style="width: 84px; height: 20px;">&nbsp;0.744914</td>
<td style="width: 143px; height: 20px;">&nbsp;XGBoost</td>
</tr>
<tr style="height: 20.2px;">
<td style="width: 94px; height: 20.2px;"><strong>F1 Score</strong></td>
<td style="width: 103px; height: 20.2px;">&nbsp;0.733741</td>
<td style="width: 104.333px; height: 20.2px;">&nbsp;0.741425</td>
<td style="width: 81.6667px; height: 20.2px;">&nbsp;0.708651</td>
<td style="width: 84px; height: 20.2px;">&nbsp;0.759855</td>
<td style="width: 143px; height: 20.2px;">&nbsp;XGBoost</td>
</tr>
<tr style="height: 20px;">
<td style="width: 94px; height: 20px;"><strong>Support</strong></td>
<td style="width: 103px; height: 20px;">12357.000000</td>
<td style="width: 104.333px; height: 20px;">12357.000000</td>
<td style="width: 81.6667px; height: 20px;">12357.000000</td>
<td style="width: 84px; height: 20px;">12357.000000</td>
<td style="width: 143px; height: 20px;">&nbsp;Logistic Regression</td>
</tr>
</tbody>
</table>
<p><br /><br /></p>  
    
***Comparison Table for Confusion Matrix***
    
<p>&nbsp;</p>
<table style="height: 423px; width: 550px; margin-left: auto; margin-right: auto;" border="1">
<tbody>
<tr style="height: 187px;">
<td style="width: 272.889px; height: 187px;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; LOGISITIC REGRESSION</strong>
<table class="dataframe" style="width: 238px;" border="1">
<thead>
<tr>
<th style="width: 74px;">&nbsp;</th>
<th style="width: 78px;">Predicted Refusal</th>
<th style="width: 84px;">Predicted Acceptance</th>
</tr>
</thead>
<tbody>
<tr>
<th style="width: 74px;">Deposit Refused</th>
<td style="width: 78px;">10681</td>
<td style="width: 84px;">284</td>
</tr>
<tr>
<th style="width: 74px;">Deposit Accepted</th>
<td style="width: 78px;">809</td>
<td style="width: 84px;">583</td>
</tr>
</tbody>
</table>
</td>
<td style="width: 275.556px; height: 187px;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;RANDOM FOREST</strong><br />
<table class="dataframe" style="height: 117px; width: 251px;" border="1">
<thead>
<tr>
<th style="width: 75px;">&nbsp;</th>
<th style="width: 79.2222px;">Predicted Refusal</th>
<th style="width: 94.7778px;">Predicted Acceptance</th>
</tr>
</thead>
<tbody>
<tr>
<th style="width: 75px;">Deposit Refused</th>
<td style="width: 79.2222px;">10652</td>
<td style="width: 94.7778px;">313</td>
</tr>
<tr>
<th style="width: 75px;">Deposit Accepted</th>
<td style="width: 79.2222px;">775</td>
<td style="width: 94.7778px;">617</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr style="height: 187px;">
<td style="width: 272.889px; height: 187px;"><strong><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; DECISION TREES</strong></strong>
<table class="dataframe" style="width: 240.444px;" border="1">
<thead>
<tr>
<th style="width: 71px;">&nbsp;</th>
<th style="width: 76px;">Predicted Refusal</th>
<th style="width: 91.4444px;">Predicted Acceptance</th>
</tr>
</thead>
<tbody>
<tr>
<th style="width: 71px;">Deposit Refused</th>
<td style="width: 76px;">10128</td>
<td style="width: 91.4444px;">837</td>
</tr>
<tr>
<th style="width: 71px;">Deposit Accepted</th>
<td style="width: 76px;">675</td>
<td style="width: 91.4444px;">717</td>
</tr>
</tbody>
</table>
</td>
<td style="width: 275.556px; height: 187px;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;XGBOOST</strong><br />
<table class="dataframe" style="height: 117px; width: 251px;" border="1">
<thead>
<tr>
<th style="width: 75px;">&nbsp;</th>
<th style="width: 79.2222px;">Predicted Refusal</th>
<th style="width: 94.7778px;">Predicted Acceptance</th>
</tr>
</thead>
<tbody>
<tr>
<th style="width: 75px;">Deposit Refused</th>
<td style="width: 79.2222px;">104999</td>
<td style="width: 94.7778px;">466</td>
</tr>
<tr>
<th style="width: 75px;">Deposit Accepted</th>
<td style="width: 79.2222px;">651</td>
<td style="width: 94.7778px;">741</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
    
<br><br>
*From the above observation of metrics and confusion matrix we can conclude that **XGBoost Algorithm** has performed better than other 3 algorithms*
<br><br> """

