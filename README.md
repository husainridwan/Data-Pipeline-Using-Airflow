# 🏡 Zillow Data Pipeline

An automated ETL pipeline that extracts real estate data from Zillow API, transforms it using AWS cloud services, and loads it into Redshift for analysis.

---

## 🛠️ Key Components
- **Extract**: Zillow API → Raw JSON (S3)
- **Transform**: AWS Lambda (JSON → CSV)
- **Orchestrate**: Apache Airflow (EC2)
- **Store**: Amazon S3 Buckets
- **Analyze**: Redshift Data Warehouse

---

## 🔄 Workflow
1. Airflow DAG triggers daily Zillow API extraction
2. Raw JSON stored in S3 bucket
3. Lambda function transforms data to CSV
4. Transformed CSV loaded to clean S3 bucket
5. Data copied to Redshift for analytics

---

## 🔧 Requirements
- Python 3.10+
- AWS Account
- RapidAPI Zillow Key
- Apache Airflow
- Redshift Cluster

---

### Medium: [Data Pipeline with Airflow](https://medium.com/@husainridwan/from-zillow-api-to-redshift-automating-a-data-pipeline-with-airflow-aws-5412355b2467)
