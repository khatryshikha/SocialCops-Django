# SocialCops-Django

## Important Links:


Postman Collection of all the endpoints with valid request/responses :
https://documenter.getpostman.com/view/5364090/Rztpp75A

GitHub Repository Link : https://github.com/khatryshikha/SocialCops-Django


## Introduction 


The solution set of Rest API endpoints to pause/stop/terminate the long-running task once triggered which require long time and resources on the servers. It is a set of 3 APIs-
1. [API for Upload CSV ](#1-api-for-uploading-csv-file)
2. [API to Stop the Upload or Export](#2-api-to-stop-the-upload-or-export)
3. [API to export filtered data  to CSV](#3-api-to-export-filtered-data-to-csv )

Technologies used:
-----------------------------
  - Python/ Django framework
  - MongoDB
 

  
## Move To

- [Installation Instructions](#installation-instructions)
- [Run in Docker Container](#run-in-a-docker-container)
- [API 1 - API for Upload CSV with Stop feature](#1-api-for-uploading-csv-file)
- [API 2 - API to Stop the Upload or Export](#2-api-to-stop-the-upload-or-export)
- [API 3 - API to export filtered data to CSV with a stop feature](#3-api-to-export-filtered-data-to-csv )
  
## Installation Instructions
-----------------------------
  1. clone the project
  `git clone https://github.com/khatryshikha/SocialCops-Django.git`
  2. cd to project folder `cd SocialCops-Django` and create virtual environment
  `virtualenv venv`
  3. activate virtual environment
  `source venv/bin/activate`
  4. install requirements
  `pip install -r requirements.txt`
  5. run the server
  `python manage.py runserver`


## Run in a Docker Container


If you wish to view a sneak peek of the Systers VMS, you may use Docker to
preview the VMS.


1. Install [Docker](https://docs.docker.com/installation/).
   Follow the installation steps for your specific operating system:
     * Docker runs natively on a Linux-based system.
2. Install [docker-compose](http://docs.docker.com/compose/install/).
   Note: fig has been deprecated. Docker-compose replaces fig.
3. Clone the project `git clone https://github.com/khatryshikha/SocialCops-Django.git` and enter the project folder `cd SocialCops-Django`
4. Run `docker-compose up` to start the webserver for the Django SocialCops Assignment.
1. Systers VMS should be running on port 8000.
     * If you are on Linux, enter `http://0.0.0.0:8000` in your browser.
     

## 1. API for Uploading CSV file

[(Back to top)](#introduction)


This API upload the CSV file to the database(here MongoDB). In this 'tqdm' python module is used to show the uploading progress bar.

API - `http://127.0.0.1:8000/upload`

Methods : POST

![Uploading CSV with progress bar](https://user-images.githubusercontent.com/30694592/52474215-d1c9fe00-2bbd-11e9-81c5-68c7f0d6dd11.jpg)


  ### API Response
   ```
   1. Successful response

    {"code": "1", "Message": "Succesfully added data to database", "status": "success"}
    
```     
![Successful Upload Response](https://user-images.githubusercontent.com/30694592/52428112-59186280-2b27-11e9-9d4e-c14f6a551e21.jpeg)
  
NOTE : This route `http://127.0.0.1:8000/clear` is used to clear the database. 


## 2. API to Stop the Upload or Export

[(Back to top)](#introduction)

This API will Stop the Upload/Export irrespective of the remaining progress without uploading/exporting data to database/CSV File and render back to Upload page to upload/export new file.

API - `http://127.0.0.1:8000/stop`

Methods : GET, POST

![Stop Upload/Export Response](https://user-images.githubusercontent.com/30694592/52427944-02128d80-2b27-11e9-9267-af31352c1969.png)

### API Response
   ```
    {"code": "0", "Message": "Fail to process/Force stopped", "status": "fail"}   
 ```



## 3. API to export filtered data to CSV 

[(Back to top)](#introduction)

This API exports the data to CSV file. It contains the specific filters using them we can filter the data from a database in small segments sothat termination of the export becomes easy.

API : `http://127.0.0.1:8000/export?<filters>=<filtervalues>`

Methods : GET, POST


<b>Filters : </b>

Following filters can be applied:

  | Filter | Meaning | Value Format (refer table below) | Example |
  | ------ | ----- | ------ | ----- |
  | name | filter name (in the given database "name" is "country name"(case sensitive)) | `<filterValue>` | name= US | 
  | Price | Basically filter by value (in the given database "price" is "product price") | `<FilterType>-<filterValue>`| price=gte-100 |
  | startdate | Filter by on or after specific date | `yyyy-mm-dd` | startdate=2019-01-01 |
  | enddate | Filter by on or before a specific date | `yyyy-mm-dd` | enddate=2020-01-01 |

In the format `<FilterType>-<filterValue>`, `<FilterType>` can be

  | numFilterType | Meaning |
  | ------ | ------ |
  | eqt | equal to |
  | gte | greater than or equal to |
  | lte | less than or equal to |

<b>Examples</b>

1. Fitler by name:
```
http://127.0.0.1:8000/export?name=US

```
2. Fitler by price:
```
http://127.0.0.1:8000/export?price=gte-200

```
3. Fitler by Dates:

    1. By Start Date :
    ```
    http://127.0.0.1:8000/export?startdate=2019-01-01

    ```
    2. By End Date : 
    ```
    http://127.0.0.1:8000/export?enddate=2020-01-01

    ```
    3. In range of Start Date and End Date : 
    ```
    http://127.0.0.1:8000/export?startdate=2019-01-01&enddate=2020-01-01

    ```

4. Filter by all parameters:
```
http://127.0.0.1:8000/export?startdate=2019-01-01&name=US&price=gte-200&enddate=2019-03-01

```

5. Export without any Filter:
```
http://127.0.0.1:8000/export

```
![CSV Export with Filters](https://user-images.githubusercontent.com/30694592/52428021-279f9700-2b27-11e9-95e8-276869431255.png)

### API Response
If the request to the API is sent, it downloads a CSV file containing data based on filters.



-----------------------------
-----------------------------

CSV files are available for test : \
<b>** data.csv file contains the date column, contains data of 26 rows.\
** testdata.csv and winedata.csv are large files but doesn't conatin date column.</b>
