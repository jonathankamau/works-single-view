# Works Single View

## Requirements

Python 3.7.7
Dependencies are listed in the [requirements.txt](requirements.txt) file.

Clone the repo to your local machine by running either:

            $ git clone https://github.com/jonathankamau/works-single-view.git
Or

            $ git clone git@github.com:jonathankamau/works-single-view.git

Create a virtual environment that you will use to run the python scripts and the API.You can follow the guide [here](https://docs.python-guide.org/dev/virtualenvs/) on how it up using either virtualenv or virtualenvwrapper. Ensure that it's setup to run on Python 3.7 and above.


### Instructions to execute the Works Single View Code
- Activate the virtual environment you created earlier.
- Install all the requirements in the requirements.txt file by running the following command:

            $ pip install requirements.txt
- Install PostgreSQL if you don't have it installed yet on your local machime.
- Create a database using the database name provided in the [data.cfg](configs/data.cfg), or another name that you prefer and update the config file with it.
- After creating the database, run the following command:

        $ python main.py

- Running the above command executes the following steps:
    - It loads some of the Spark dependencies that will be needed in performing aggregating and reconciling actions on the Spark dataframes.

### Instructions to run the Works Single View API (built using Flask Restful)

- After running the Works Single View scripts using the instructions above, you can run the API from the project root folder using the below command:

        $ python api/manage.py runserver
- The API should be running on http://127.0.0.1:5000/

#### Querying the Works Single View by ISWC

- Using a API client such as [Postman](postman.com) you can run the following endpoint using the GET method:

            http://127.0.0.1:5000/api/v1/<iswc>

- Replace `<iswc>` with any of the iswc codes for the musical works in the `works_metadata.csv` file. 
- If successful, you should receive a JSON response with the message in the following format:

```
{
  "message": "The Music Work was retrieved successfully and is being exported as a csv",
  "music_work": {
    "contributors": "Rayo Gibo Antonio|Ripoll Shakira Isabel Mebarak",
    "iswc": "T9214745718",
    "sources": "universal, warner",
    "title": "Me Enamore"
  }
}
```
- The musical work will also be exported in csv format and stored in the `output` folder that is at the root of the project.

#### Import (upload) csv files and reconcile the metadata into the Works Single View

- While the API server is still running, navigate to the following URL on your browser:

        http://127.0.0.1:5000/upload

- Click on `Select CSV files` field and choose the files that you want to upload and that follow the `works_metadata.csv` format.
- After selecting them, you will see them listed on the page.
- Click on the `Upload` button to import them. 
- A reconciled copy of the imported data will be stored in the `data` folder and the scripts to match and reconcile the data with the database will be executed.
