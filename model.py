# imports for data manipulation
import pandas as pd
from numpy import NaN
from numpy import std

# imports for models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

# imports for data prep.
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer


# imports for training and testing.
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# imports for Data Vis
from seaborn import heatmap
from matplotlib.pyplot import show
from matplotlib.pyplot import figure
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error
from statistics import mean




class Model:

    algmap = {
            "Linear Regression": LinearRegression(),
            "Decision Tree Classifier": DecisionTreeClassifier(),
            "Random Forest Classifier": RandomForestClassifier()
        }

    # ----- OBJECT INIT ----- #
    def __init__(self):
        self.df = None
        self.df_attr_meta = None
        self.df_corr = None
        

    # ----- INTERNAL FUNCTIONS ----- #

    # finds and deals with invalid data
    # if a column contains invalid data above the user set threshold in cp drop it
    # else, replace invalid data with the average of the column using user selected method in cp
    def dcleanse(self, cp):
        addcats = []
        for am in self.df_attr_meta:
            
            nanc = 0
            if self.df_attr_meta[am][0] == 1:
                addcats.append(am)
                vv = self.df_attr_meta[am][1].split(",")
                for i in range(len(self.df.index)):
                    v = self.df.iloc[i][am]
                    if v not in vv:
                        self.df.at[i, am] = NaN
                        nanc+=1
            else:
                vr = self.df_attr_meta[am][1].split("to")
                lb, ub = int(vr[0]), int(vr[1])
                for i in range(len(self.df.index)):
                    v = self.df.iloc[i][am]
                    if not lb <= v <= ub:
                        self.df.at[i, am] = NaN
                        nanc+=1

            if nanc >= len(self.df.index) * (cp["th"]/100):
                self.df.drop(am)

            column_av = self.df[am].mode()

            if cp["av"] == "mean":
                column_av = self.df[am].mean()
            elif cp["av"] == "median":
                column_av = self.df[am].median()

            self.df[am].fillna(column_av, inplace=True)

        return addcats


    # prepares the data for training and testing
    # cleanse the data
    # set features and label
    # if the target is categorical and a regression algorithm is being used, return None
    # if the target is numeric and a classification algorithm is being used, create classes according to user input
    # other combinations are standard
    def dprep(self, fs, algn, label, classes, cp):
        
        addcats = []
        #cleanse data
        addcats = self.dcleanse(cp)

        # set features
        X = self.df[fs].copy()

        # set label
        y = self.df[label].copy()
        
        # check if categorical attr. with regression model (continuous attr. with classification model is fine)
        if y.dtype == object:
            if algn.split(' ')[-1] == "Regression":
                return None
        else:
            if algn.split(' ')[-1] == "Classifier":
                if classes is not None and len(classes) != 0:
                    ls = []
                    vs = []
                    for k in classes:
                        v = classes[k]
                        ls.append(k)
                        lbv = int(v[0])-1
                        ubv = int(v[1])
                        if lbv not in vs:
                            vs.append(lbv)
                        if ubv not in vs:
                            vs.append(ubv)
                    
                    self.df["Target"] = pd.cut(x=self.df[label], bins=vs,
                                labels=ls)
                    y = self.df["Target"]
            

        # identify categorical attributes
        cat = list(X.select_dtypes(include=["object"]).columns) + addcats


        # one hot encode; turn categorical data in to ordinal data
        column_trans = make_column_transformer((OneHotEncoder(), cat), remainder="passthrough")
        X_encoded = column_trans.fit_transform(X)

        print(X_encoded.shape)

        return[X_encoded, y]
        
            

    # ----- INTERFACE FUNCTIONS ----- #


    #takes filepath, load in csv at that filepath, creates a pandas dataframe from csv file
    def readin(self, filepath):
        self.df = pd.read_csv(filepath, sep=",", header=0)
        self.prepcorrp() 

    def get_df(self):
        return self.df


    # prepares a dummy dataframe to compute correlations on
    def prepcorrp(self):
        objcats = self.df.select_dtypes(include=["object"]).columns
        self.df_corr = pd.get_dummies(self.df, columns=objcats)

    # plots correlation matrix for dummy dataframe
    def showcorrelations(self):
        if self.df_corr is not None:
            figure(figsize=(14,12))
            heatmap(self.df_corr.corr(), annot=True)
            show()
    

    # set meta-data for dataframe
    def df_set_attr_meta(self, am):
        self.df_attr_meta = am



    # splits prepared data into training and test subsets
    # trains model on training subset
    # tests model on testing subset
    # also does 10 fold cross validation across multiple splits
    # returns accuracy results and other performance metrics based on whether classification or regression algorithm was used
    def tnt(self, algn, fs, label, classes, cp):
        
        pd = self.dprep(fs, algn, label, classes, cp)
        X = pd[0]
        y = pd[1]

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        print(X_train.shape)
        print(X_test.shape)
        print(y_train.shape)
        print(y_test.shape)

        pm = self.algmap.get(algn)
        pm = pm.fit(X_train, y_train)
        y_pred = pm.predict(X_test)
        
        cvss = cross_val_score(self.algmap.get(algn), X, y, cv=10)
        clf_report = None
        clf_conf = None
        reg_mse = None
        if algn.split(" ")[-1] == "Classifier":
            clf_report = classification_report(y_test, y_pred, target_names=classes.keys())
            clf_conf = confusion_matrix(y_test, y_pred)
        else:
            reg_mse = mean_squared_error(y_test, y_pred)

        return [pm.score(X_test, y_test), y_test, y_pred, clf_conf, clf_report, reg_mse, mean(cvss), std(cvss)]
    