# Stocks Manager

- jorge.fiestas@utec.edu.pe
- ferndando.delosheros@utec.edu.pe

## Introduction

Time series analyisis is an extremely powerfull tool that allows the prediction of future values of the series and possible trends just based on these trends alone. One of the most commmon and profitable applications of such analysis is to run predictions of the stock market in order to know beforhand when the good moments to buy and sell should happen. In the past, these analysis were done through the study of theory and finances, however, with the arrival of new technologies and the democratizaton of information, a new paradigm for time series analyisis has emerges: Artifial Intelligence trained on Big Data.

However one huge disadvantage of time series analysis is the computational complexity these computations have. Even for simple models, the computational power and time that it would take to compute and accurrate prediction is not small at all, specially if are thinking about a PC scale. What is even worse is that many times keeping track of a single stock is not enought to have sufficient information, many time models have to be trained on multiple distinct series and metrics.

## Solution Proposal

Considering the problems described above, we propose a *Stock Managment* platform that will allow users to keep track of their stocks of interest and compute time series analysis and predictions on these. The three main capabilities of our platform should be:

1. **Scrapping:** Recent stocks data can be obtained in order to have up-to-date information. User can manage which stocks he would like to track.
2. **Analysis:** Using the data fetched by the scrapper, the user should be able to run analysis of these time series.
3. **Visualization:** Users can have access to UI services that make the data obtained digestible.

In a way this will be similar to *FaaS* platforms, with the main difference being that the functions users can call are limited by the API. This way, even users with begginer level understanding of topics of programming and stocks can have a friendly platform to query from. Aswell, in-memory processing will be used in order to realize the complex calculations.

## Architecture Proposal

![Architecture Diagram](docs/architecture.png)

**Alpha Vantage:**
Alpha Vantage is an API that allows services to access stocks data through HTTP requests. Alpha Vantage usually has a very elaborate API that allows to realize all kinds of queries, however, for the scope of this proyect we chose two query 1 year of data for each stock in intervals of 5 minutes. Stocks can be accesed through their stock market code **eg** AAPL (Apple), TSLA (Tesla), etc. This will be the only component of the solution that is not hosted on the kubernetes cluster.

**InfluxDB:** 
InfluxDB is a database manager specialized in the indexation and storage of time series data. The two main ways two communicate with InfluxDB are through its `Python` client `influxdb_client`, or through requests with its own query language: *Flux*. We build InfluxDB in a container with a persistant volume in order to mantain the stored data. This will be one of our Kubernetes services.

**Grafana:**
Grafana is a web platform that allows to easily visualize data through a simple UI that has many custom graph options. This application has support to easily connect to InfluxDB buckets through HTTP. We also built grafana in a container and ran it as a Kubernetes service.

**WebApp:**
Our web application is a simple API server that allows for simple HTTP request. We used Pythons `Flask` in order to implement it. This service also has acces to InfluxDB and AlphaVantage through the Python client and HTTP respectively. As no data is stored in this service, we decided to lunch multiple replicas of the application in different pods in order to prevent down time and better distribute the number of requests.

## Monitoring


## Scalability

The request heavy parts of our application will be the web application and our InfluxDB service, as they will constantly recieve I/O requests. We believe both of this services need some form of scaling in order to deal with higher or lower requests per second. However, as they are different in nature, we believe that each of this should have a different type of scaling.

As the web application works *in memory* and loads the information from *Alpha Vantage* and *InfluxDB*, we believe that the best option for this pods will be horizontal scaling. This is also compatible with the nature of *Flask*, that tends to have sequential procesing. To achieve this we can use a Kubernetes horizontal pod auto-scaling sevice (HPA). 

For InfluxDB scaling horizontally can be a challenge as it has persistent data that would need to be replicated or a more complex query system would need to be built. In order to avoid this we opted for vertical scaling, as InfluxDB already has a parallel procesing nature. For this reason we believe that is better to opt for vertical scalability. In order to achieve this we can use a Kubernetes vertical pod auto-scaling service (VPA).

## Conclusions


