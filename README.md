# vader-sentiment-analysis
Whilst there are already many amazing and detailed guides out there on how to run sentiment analysis in Python using VADER, TextBlob, etc, there is not much in-depth information online, bar the generic "Hello, World!" examples, on how to deploy sentiment analysis code live, step-by-step, onto the cloud. <br>
So, in this article I've leaned heavier on how to set this all up (opting for Google Cloud), and gone very light on the NLP data analysis techniques side of things.<br>
We still discuss the main tasks such as deriving polarity and compound scores from text corpus so that we can determine whether it is positive, neutral or negative, but the primary goal of this article is to get those completely new to sentiment analysis, Python and Google Cloud in general, a chance at experimenting and getting something basic live.<br>
We start with setting up a simple workflow with VS Code on a local machine using Python and Google Sheets API to read data from GSheets and analyse the corpus using VADER. We then move onto configuring Google Cloud Functions directly from the GCP interface.<br>
<br>Full Python code examples below.

<h2>Read the article 👇</h2>

<h3> Sentiment Analysis on Google Sheets with VADER using Python and Google Cloud Functions</h3>
<p>A Cloud Function recipe for sentiment analysis</p>
📙 https://towardsdatascience.com/sentiment-analysis-on-google-sheets-with-vader-using-python-and-google-cloud-functions-e767985ed27d
<br>
<br>
<ins><h4>Code Examples:</h4></ins>
📌 <strong>Full Python Code (on local)</strong>: https://github.com/Practical-ML/vader-sentiment-analysis/blob/main/local-main.py
<br>
<br>
📌 <strong>Full Python Code (updated for Google Cloud Functions)</strong>: https://github.com/Practical-ML/vader-sentiment-analysis/blob/main/main.py
<br>
<br>
📌 <strong>The requirements.txt for Cloud Functions</strong>: https://github.com/Practical-ML/vader-sentiment-analysis/blob/main/requirements.txt
<br>
<br>
