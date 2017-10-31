# Title
## See the cover - buy the book

# Abstract
<!--A 150 word description of the project idea, goals, dataset used. What story you would like to tell and why? What's the motivation behind your project? -->
It is known that color and emotion are strongly related <sup>[1](#1)</sup>. The goal of this project is to analyze the imact of this link on the book preferences. We will analyze the link between the cover of the book and the quality of it's content. <!--Are some books not popular just because of their neutral appearance. -->

For this purpose we will use the dataset with book details including reviews from Amazon. We will use the reviews received by the reader, the colors and shapes that appear on the cover and eventually the images that appear in the book. We will analyze if there are different trends that appear for different book categories and if the trends have a period of duration. We will also take in account the usefulness of the reviews, i.e. only the helpful reviews will be considered. 

With this analyzis we can find out if we can judge the book by its cover or in which category of books we can judge the book only by it's visual appearance. 

# Research questions
<!--A list of research questions you would like to address during the project. -->

* The variation and importance of the visual decoration of books in different categories 
* Are cover trends a real thing

# Dataset

<!-- List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant. -->

We are going to use mainily the [Amazon reviews dataset](http://jmcauley.ucsd.edu/data/amazon/) provided by the team. Reviews and rating are freely accessible and links to an unique identifier provided by Amazon ([Amazon Standard Identification Number](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number)). However, product metadata are on request (an email is already on the way). Thus, we did not get hand on book metadata content and the sample is about a retail product. From there, we learned that our main raw material (the covers) are not part of the dataset. They are linked from the metadata description: we need to scrape them. It raises somes concerns: 
*cover image provided by Amazon*: will they be correctly labeled (distinction of picture of the inside and picture of the cover) and will they be easily scrapeable (if we are constantly blocked, we are going to need either to reduce our ambitions or find some workaround).
If this is not the case, we found we could use images from [OpenLibrary](https://openlibrary.org/) <sup>[2](#2)</sup> which requires some join process.

Image features are already available for the different books, which are on request as well. We could use this data but we will need some prior knowledge on the feature generation process in order to be able to include it in our data analysis. 

Other option is to process the images by ourselves. 

This process could take times. Also, working with images always involve some expensive computations thus we have to plan our work accordingly (if we want to use unsupervised classification or image similarity indices). For instance, we also expect a large work about duplicates detection (multiple edition, same cover, multiple priting version but same cover).

# A list of internal milestones up until project milestone 2

* (if needed) Put in place a reliable and autonomous scraping process (should not stop without we know) to get as much image as possible
* Analyse if image processing on our side is needed and if it is the case define the type of analyzis to be performed 
* Find paper and research about image similariy, and "trend" classification to find if it is possible
* skim through the dataset to find if duplicate is a real issue (if it skew all our answer or not)
* decide if we need to only keep a segment of the data (only Business books, polar books, etc.) if computations are too expensive


# Questions for TAa
Add here some questions you have for us, in general or project-specific.

<a name="1">1</a>: NAz, K. A. Y. A., and Helena Epps. "Relationship between color and emotion: A study of college students." College Student J 38.3 (2004): 396.

<a name="2">2</a>: An idea from http://cs229.stanford.edu/proj2015/127_report.pdf

# Other research

* B. K. Iwana, S. T. Raza Rizvi, S. Ahmed, A. Dengel, and S. Uchida, "Judging a Book by its Cover," arXiv preprint arXiv:1610.09204 (2016).

