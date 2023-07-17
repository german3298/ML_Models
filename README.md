# ML_Models
<h2>CART_Entrophy_Tree:</h2>

<h3>Model information: </h3>
It's a CART tree. </br>
For the evaluation of the quality of the partition, the concept of impurity and entropy is used.</br>
The quality of a partition is measured by the decrease in impurity (the better the partition is the one that produces the greatest decrease in impurity).</br>
The criterion to determine that a node is terminal is if the maximum possible impurity decrement is too small (less than epsilon).</br>
Epsilon is empirically determined but I recommend a value (at least in the two given databases) of about 0.2.</br>
It also has an added refinement, in which the split, instead of being placed directly on the point, is placed on an average between this point and the next one (more margin, tighter and helps to generalize). </br>
The program uses a partition of 70% for training the model, and the rest for testing it.</br>
The method for comparing the true labels with the predicted labels is a confusion matrix (confus.py).</br>

<h3>Usage:</h3> 
<br>python3 arbol_programa.py database epsilon </br>
Example: python3 arbol_programa.py OCR_14x14 0.2 </br>

<h3>Output: </h3>
Eps = Epsilon (the variable mentioned above)</br>
Ete = Number of errors in the test partition</br>
Ete(%) = Percentage of errors with respect to the total number of test items (estimated error)</br>
Ite (%) = confidence interval (Ete(%) + E, Ete(%) - E) </br>
Asuming that E it's: E = 1.96*sqrt((Ete*(1-Ete))/Nºsamples) </br>

<h3>Given databases: </h3>
1-OCR_14x14:</br> 
		&nbsp&nbsp&nbsp1000 samples = 1000 rows (handwritten digits).</br>
		&nbsp&nbsp&nbspDigits from 0 to 9 -> 10 labels</br>
		&nbsp&nbsp&nbsp1 sample -> 196 columns (features) + last column (label) -> 197 columns</br>
		&nbsp&nbsp&nbsp1 sample -> normalized image 14x14 (196 columns)</br>
2-expressions:</br>
		&nbsp&nbsp&nbsp225 facial expressions represented as 4096-D arrays and classified in 5 labels (1-surprise, 2-happiness, 3-sadness, 4-anguish, 5-disgust).</br>

<h3>Note: </h3>
I know there must be better ways to do the loops or certain operations, but it was my first Python script and I programmed it mostly to understand the model.</br>
