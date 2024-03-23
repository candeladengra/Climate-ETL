# Climate-ETL

Climate-ETL is a robust Extract, Transform, Load (ETL) pipeline built using Python, Redshift, and Apache Airflow. This powerful tool is designed to efficiently retrieve climate data from an API on a daily basis, perform necessary transformations, and store the processed data securely in Redshift for further analysis.

# Features

Automated Data Retrieval: Climate-ETL automates the process of fetching climate data from an external API, ensuring timely and consistent updates.

Scalable Storage: Leveraging Redshift's scalable and high-performance data warehousing capabilities, Climate-ETL ensures reliable storage of large volumes of climate data.

Scheduled Execution: Integrated with Apache Airflow, Climate-ETL facilitates scheduled execution, enabling seamless orchestration of data extraction, transformation, and loading tasks.

Email Alerts for Temperature Limits: Climate-ETL sends email alerts when temperature values exceed certain thresholds. This functionality enhances the system's monitoring capabilities by proactively notifying administrators when certain thresholds are surpassed.

# Usage

1. Build Docker Containers:

```
docker-compose build
```

2. Start Climate-ETL:

```
docker-compose up
```

3. Access Airflow Dashboard:

Once Climate-ETL is up and running, you can access the Airflow dashboard by navigating to localhost:8080 in your web browser. Here, you can monitor the execution of ETL tasks, manage workflows, and view logs.
