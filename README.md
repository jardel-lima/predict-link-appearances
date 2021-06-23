# Predict the Number of Appearances of a Link

This project aims to predict the number of Appearances of any link based on its characteristics. A machine learning model was build to make this prediction and o build the model the following steps were taking.

## Scraper

A Scraper was build to collect information about a base of urls. For each url in this base all links in that page are found end for each one of those we found all links on those as well. It is done until a depth of N.

For each url and link found int the url, the scraper will create a csv file with the following information:

 `<URL_ORIGIN>,LINK,1`

 By the end of the scrapping step we will have a file as the bellow snippet:

 ```
 linka,linkb,1
 linka,linkc,1
 linka,linkd,1
 linkb,linkc,1
 linkb,linkd,1
 ...
 ```

 When the scrapping phase is done the Process Data phase must be execute.

 ### How to use

 Execute the code `/code/scraper/scraper.py` passing as arguments the base with urls to be scraped, the depth of the search and the base output file.

 ## Process Data

 In this phase, all csv file created in the Scrapping Phase will be read and processed to count the number of appearances of each link and save this information in the DataBase.

 For example, using the example data from the scrapping phase, we will have:

 ```
 linkb,1
 linkc,2
 linkd,2
 ```

### How to use

Execute the code `/code/scraper/processdata.py` passing as arguments the base input files crated in the last phase and the SQLite data base where the precess data will be inserted.

 ## Featuring 

 After the Process Data Phase, we will create features based on the urls and insert those info into the Database.

 ### How to use

 To create features for all links found in the scrapping phase, run the code `/code/features/features_db.py` passing the SQLite Database.

 ## Modeling

 With those features we created a Machine Learning Models using Random Forest.

 ### How to Use

 There is a jupyter notebook in the `/code/model` folder. If there are more information in the Database, run it and save the model.

 ## Rest API

 The last part of this project is the rest API. It has two endpoints `/link/features` and `/link/predict_appearances`.

 The first one will build all features of a given link. The second one will use the model build in the modeling phase to predict the number of appearances of a link based on its features.

 ## How to Use

 This API was build using FastAPI, to run it go to the `/code/api` folder and run `uvicorn main:app --reload`. You can use the `/docs` from the API to visualize and test all implemented endpoints.

 You can also use the Dockerfile to build a image with the Fast API.

 Obs: Copy the used database to `/database` folder and the model to `output/model` folders.
