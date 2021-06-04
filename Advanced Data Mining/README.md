## Analysis of co-purchased products on Amazon

Large sized graphs are difficult to visualize, as they are computationally very expensive to plot. In such cases, we have to rely on algorithms which help us identify various communities and clusters in the graph, which are difficult to visualize too.

The motivation behind this project was to study the methodology behind how product recommender systems provide relevant product recommendations to users. Most of the Machine Learning methods possess a naïve assumption of falling in a distribution, and it is not possible to use such methods for graph-based recommender systems, where there may be no distribution which can accurately represent the dataset.

The dataset, “Amazon co-purchased products” possesses of the following attributes:

1. Product
2.	Group (Book, Video, DVD, Music)
3.	Sales Rank
4.	Similar products (at most 5 products which are similar to the product)
5.	Similar categories
6.	Reviews
7.	Avg. Rating

As there is no objective ground truth for this problem, due to the scale of the data-points, which cannot be categorized by humans. Therefore, the project was to attempt to evaluate identify communities, and try to evaluate them.

### Prior work

Dimensionality reduction is a major area of research in graph theory, and various methods are used to conduct the same. There are trade-offs when it comes to reducing dimensions, but in many cases, the approximations too give quite good results, close to the reality.

The project included usage of Laplacian Matrix to calculate Eigenvalues and Eigenvectors[1](https://www.cs.cmu.edu/~aarti/Class/10701/readings/Luxburg06_TR.pdf) of the graph, and use them to estimate the optimal number of eigenvectors which explain the most essence of the data quite accurately.

Community detection[2](https://www.pnas.org/content/99/12/7821) is a different approach towards identifying patterns in the data, and the algorithms for detecting communities, such as Girvan Newman Algorithm, are usually used. However, due to the high time complexity of the algorithm <img src="https://latex.codecogs.com/gif.latex?O(E^{2}N)"/> (E: Edges, N: Nodes), community detection was not possible on the dataset due to computational limitations.

Regression models are the most intuitive models in Machine Learning, and it is easy to add and drop features, using Ridge and Lasso regularization terms[3](http://statweb.stanford.edu/~owen/courses/305a/Rudyregularization.pdf).

The following were the models/methods attempted in the project:

1.	Regression: Linear, Ridge, Lasso

2.	Spectral clustering: with and without eigenvalue/eigenvector decomposition

3.	Degree centrality computation[4](https://cs.brynmawr.edu/Courses/cs380/spring2013/section02/slides/05_Centrality.pdf)

4.	Clustering coefficient calculation

5.	Community detection: Girvan Newman algorithm (Failed to implement)

The experiment provided insights about products which possessed higher centrality tendencies, and these measures can be used successfully in marketing[5](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.298.6671&rep=rep1&type=pdf), for methods like influencer products, pyramid marketing, etc.

### Methodology

**A)	Pre-processing:**

The data was in the form of a text, with both nodes/connections, as well as text data which signified the purpose of the product. 
Steps:
I)	Strip ID, ASIN (nodes), Title, Group, Salesrank, Similar products (connections), Categories, Reviews

II)	Remove the stopwords from the Categories, and cleaned the text

III)	Split the data by Group (DVD, Music, Video, Audio), and then combined them. Verified the original count with the concatenated lists count

IV)	Strip the words in the categories of both the product, as well as the similar product. Depending upon how many words are similar in both the cases, the similarity is calculated by:

<img src="https://latex.codecogs.com/gif.latex?Similarity=\frac{Intersection}{Union}"/>

V)	Calculate degree centrality using the following formula:

<img src="https://latex.codecogs.com/gif.latex?Centrality=\frac{\sum_{i=1}^{G}{[C_{D}(n^{*})-C_{D}i]}}{[(N-1)(N-2)]}"/>

Once the above stated variables were calculated, they were all appended to a dictionary.

Following are the visualizations for the attributes:

1.	Average Rating:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/average-rating.png"/>

The average ratings for all the products given as 0 were removed when conducting the regression model, with the assumption that those were the cases when no rating was found, which are outliers for the data.

2. Degree Centrality:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/degree-centrality.png"/>

It is clearly visible that extremely less number of nodes have higher than 0 degree centrality, which means that these nodes are more centred as compared to most of the products.

These are the kind of products that we marketing department need to look out for, because they have the potential to be an influencer or a catalyst product. Other associations are likely because other products are an accessory, or necessary requirement of the product’s functioning.

3. Clustering Coefficient:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/clustering-coefficient.png"/>

A lot of products in the amazon co-purchase dataset have a clustering coefficient higher than 0.2 (judging by the area under the curve, almost 1/6th products), Depending on the clustering coefficient, priority queue for marketing/sales and advertising of products can be built, which is necessary to improve engagements via inorganic growth.

**B) Regression Models:**

To build a regression model, the following attributes were shortlisted:
I)	Average rating

II)	Total reviews

III)	Degree centrality

IV)	Clustering coefficient
 
The regression model is built to predict the Sales Rank (lower rank implies higher sales). Naturally, it is expected that the coefficients are negative, because as the features’ values increase, the model must output a lower rank.

Regularization methods were explored (Lasso and Ridge Regression) to add/subtract features to improve the model’s performance. It is necessary to note that adding features might lead to a decrease in performance too.

**C) Dimensionality Reduction:**

 Due to computational limitations, both NetworkX and Scipy do not support the calculation of all the eigenvectors and eigenvalues in the Laplacian Matrix[6](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html). Therefore, the method implemented was to compute the top k-eigenvalues/eigenvectors. The experiment was conducted till k=200, but for K > 200, memory error was noticed. 

K-means clustering was conducted on 200 eigenvectors, and as expected, most of the elements were clustered to one single group, as the number of books are much higher than number of music, DVDs, and video products.

### Results

**A) Summary Statistics:**

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/summary-statistics.png"/>

**B) Regression Models:**

I) Linear Regression:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/proj-linear-reg.png"/>

II) Ridge Regression:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/proj-ridge-reg.png"/>

III) Lasso Regression:

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/proj-lasso-reg.png"/>

The experiment showed that increase in the value of regularization term is causing a decrease in the R2 value.

Less regularization: <img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/less-reg.png"/>

More regularization: <img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/more-reg.png"/>

**Products with highest clustering coefficient:**

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/clustering-high.png"/>

**Products with highest degree centrality:**

<img src="https://github.com/111989/Data-Science/blob/main/Advanced%20Data%20Mining/images/centrality-high.png"/>

### Conclusion

The key conclusions of the experiment are as follows:

a)	Traditional machine learning algorithms, which take into consideration the probability density estimation, fail to perform well in networks.

b)	Degree centrality and clustering coefficient are good metrics to measure the popularity of a product.

c)	Community detection algorithms are computationally expensive, however, with the proper infrastructure, can be the basis of recommender systems.

