# CPSC325TwitterTickerAnalyzer
The app is available at https://project-381921.wl.r.appspot.com as long as I continue hosting it.
There is only 4GB of memory allocated to the BERT cloud function. If you recieve a message on the application stating "max memory limit reached" the cloud function has exceeded 4GB and has not returned a prediction.
The final prediction is using a KNN classifier on the tensor data returned from the BERT model.
The functions that are fun in the cloud function are under /spare_files/Bert_Model.py.
