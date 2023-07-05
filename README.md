### Introduction

Predicting students’ academic performance is a very old area of study, with lasting interest. This is because a student’s academic success is vital for communities to develop and continue succeeding. With the rise in adoption of e-learning platforms and in general more data being collected online on peoples’ internet usage, we can take advantage of high computing power nowadays to process and analyse this data, and use it to make predictions on students’ performance. To predict a students' performance however, you need data to base your predictions on, which is another challenge. What data is useful in predicting a student’s performance, the factors best influence students’ academic performance? So the accuracy of our prediction is hindered or helped by the attributes we consider. Prior investigation and experiments can be done to determine which features influence students' academic success in order gather data on the best predictors for student success to ensure better predictions. 

Using data analysis techniques, we can plot correlation of certain features to the student’s academic performance, to determine which features are more correlated with our target we wish to predict. Once we have determined our set of attributes, we can feed in the information we have collected on these attributes to a Machine Learning Algorithm in to create a model which can take in new data and predict the student’s performance. 

The software in this repository allows a user to test the effectiveness of different algorithms in predicting students' grades based on a dataset that they possess. They can also cleanse the dataset with-in the application aswell as provide meta-data of attributes and perform some transformations on the data as required.



### User Guide:


To be able to run the software, you need to have the latest version of Python installed on to your system.

1). Loading In Dataset	

	Click the “Select file…” button,
	select your file type in the drop down,
	find your file, click to highlight it,
	click Open to load the highlighted file.
	
2). Viewing correlations between attributes
	
	Click the "View correlations" button 
	A window will open showing a heatmap of the correlations between the attributes in the dataset.
	Click the magnifying glass icon on the toolbar on the button, and then draw a rectangle on the heatmap to select a region to zoom into.
	Click the back button to go back to the previous view.
	Click the forward button to go forward to the succeeding view.
	Click the home button to go back to the original view of the heatmap.

3). Defining meta-data

	Click the "Define meta-data…" button,
	If an attribute is numeric, you can specify whether it is ordinal or not.
	For each attribute enter valid ranges,
	If the attribute is categorical, enter comma separated values,
	If the attribute is numeric, enter the valid range specifying the inclusive lower-bound, succeeded the word “to”, and then the inclusive upper bound.
	Click the “Confirm Definitions” button to confirm and save the values.
	Close the window.



4). Select cleansing parameters

	Click the “Cleansing Parameters” button,
	Set the percentage of missing values required in a column in order for it to be dropped, by sliding the slider from left to right, from 0% to 100% respectively.
	Select the averaging method to fill in missing values with. Select either the mean, median or mode.
	Click the “Set Parameters” button to confirm and save the values.
	Close the window.

5). Selecting the label

	From the “Select label” drop down, select your label.

6). Selecting features

	Click the “Select Features…” button,
	Select the features you wish to consider by checking the box next to the feature name.
	Click the “Confirm Selection” button to confirm and save the selected features.

7). Selecting the algorithm

	From the “Select algorithm” drop down, select your algorithm.

8). Class Definitions for a numeric label and a classification algorithm

	Click the “Define Classes…” button,
	Enter the lower bound in the first textbox, the upper bound in the second textbox and the name of the class in the third box,
	Click the “+ class” button to add the class,
	Once finished adding classes close the window.
	Note that if you click the “Define Classes…” button again, it will erase previous class definitions and you will have to define new classes.


9). View algorithm performance

	Click the “Train and Test Model” button,
	Use the scroll bar to scroll through the results.
