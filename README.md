# XALDIGITAL - Challenge DE

### This project consisted on designing a database based on a CSV file, ingest the data into a [postgres database](https://www.postgresql.org/) and build a [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api) to allow the user interact with the database.

The architecture was developed using [Docker-compose](https://docs.docker.com/compose/) through three container services. The first one is a container based on a Postgresql image, this enabled us to quickly create a fully operational database instance working at port 5432 of the local host; additionally, we created a container based on a [CentOS](https://www.centos.org/) Linux distribution image, where we validated the format of the data contained in the CSV file and then inserted the records from  a [Pandas](https://pandas.pydata.org/) dataframe into a table within the Postgres database. Unlike the rest of the mentioned containers, this one stops right after uploading the data into Postgres; finally, we mounted another container which was responsible for hosting the REST API which in turn was in charge of communicating with the database. This REST API has the capability of supporting **read** (individual or all records), **write**, **update** and **delete** record operations. It is noteworthy that both the CentOS and the REST API server containers wait until the database is up-and-running before becoming operational.

It is worth mentioning that since this is a development project, I am deliberately commiting the ```.env``` file containing the corresponding environment variables into the repo, for the sake of reproducibility. In a real prod environment this should be part of the ```.gitignore``` file and could take advantage of [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

Finally, an automated unit testing was developed using [Pytest](https://docs.pytest.org/en/7.0.x/) and [GitHub Actions](https://docs.github.com/en/actions) as a CI/CD deployment everytime there is a new Push or Pull Request on the Main branch of the repo. 

---
## Requirements
* [Docker](https://docs.docker.com/get-docker/)
* [Docker-Compose](https://docs.docker.com/compose/install/)

Note: Since we are using Docker, it is not necessary to install the rest of the Python modules, libraries and dependencies individually using [pip](https://pypi.org/project/pip/), [Conda](https://docs.conda.io/en/latest/) or [Brew](https://brew.sh/).

---
## How to execute the project
To start all the services, open a new terminal (CLI) and type the following command:
```
docker-compose up
```
Whereas to bring down the services, type as follows:
```
docker-compose down
```
Additionally, you can use the -d flag (dettached) to keep using the current terminal window and let the processed execute on the background. 

## Developed by: Ivan Legorreta
**Phone number**: +52 55 1320 7574

**Email**: ilegorreta@outlook.com
