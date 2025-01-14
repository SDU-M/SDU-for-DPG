# **DPG SDU**

## **Before You Begin**

### Prerequisites

1. **Install Docker**  
   [Docker Installation Guide](https://docs.docker.com/get-started/)

2. **Install Docker Compose (v2.14.0 or newer)**  
   [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

---

## **1. Deploy ClickHouse Database**

ClickHouse is a fast SQL engine optimized for analytical queries. Here's how to set it up:

1. **Navigate to the ClickHouse directory**:
   ```bash
   cd clickhouse
   ```

2. **Set environment variables for specific versions (optional)**:  
   By default, the latest versions of ClickHouse and ClickHouse Keeper will be used. To specify a version:
   ```bash
   export CHVER=23.4
   export CHKVER=23.4-alpine
   ```

3. **Start the ClickHouse service**:
   ```bash
   docker compose up
   ```

4. **Verify ClickHouse availability**:  
   Open [http://localhost:8123/play](http://localhost:8123/play) in your browser.

---

## **2. Deploy Apache Airflow**

Apache Airflow is used for task orchestration. Ensure your Docker Engine has at least 4GB memory (preferably 8GB).

1. **Navigate to the Airflow directory**:
   - If you are in the ClickHouse directory:
     ```bash
     cd ../airflow
     ```
   - If you are in the root directory:
     ```bash
     cd airflow
     ```

2. **Fetch the docker-compose.yaml file**:
   ```bash
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
   ```

3. **Set up the Airflow user (Linux-specific)**:
   ```bash
   mkdir -p ./dags ./logs ./plugins ./config
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

4. **Initialize the Airflow database**:
   ```bash
   docker compose up airflow-init
   ```

5. **Start Airflow**:
   ```bash
   docker compose up
   ```

6. **Access Airflow**:
   - Webserver: [http://localhost:8080](http://localhost:8080)
   - Flower (monitoring): [http://localhost:5555](http://localhost:5555)

---

## **3. Deploy Apache Superset**

Apache Superset is a business intelligence (BI) tool.

1. **Navigate to the Superset directory**:
   - From the Airflow directory:
     ```bash
     cd ..
     ```
   - If already in the root directory, stay there.

2. **Clone the Superset repository**:
   ```bash
   git clone --depth=1 https://github.com/apache/superset.git
   ```

3. **Navigate to the Superset directory**:
   ```bash
   cd superset
   ```

4. **Replace the `docker-compose-non-dev.yml` file**:  
   Replace the existing file in `/superset` with the one located in the root directory of this repository.

5. **Set production mode**:  
   Edit `/superset/docker/.env`:
   ```
   SUPERSET_ENV=production
   ```

6. **Start Superset**:
   ```bash
   docker compose -f docker-compose-non-dev.yml up
   ```

---

## **4. Connect the Tools**

1. **Create a Shared Docker Network**:
   ```bash
   docker network create shared_network
   ```

2. **Connect Services to the Shared Network**:
   - List all running containers:
     ```bash
     docker ps
     ```
   - Connect each container (ClickHouse, Airflow, Superset) to the shared network:
     ```bash
     docker network connect shared_network <container_name>
     ```

3. **Connect ClickHouse to Superset**:
   - Access the Superset container:
     ```bash
     docker exec -it superset_app bash
     ```
   - Inside the container, install the ClickHouse connector:
     ```bash
     pip install clickhouse-connect
     ```
   - Now, you can create a database connection in Superset. Use:
     - Host: `clickhouse`
     - Port: `8123`
     - Password 

4. **Connect Airflow to ClickHouse**:
   - Extend the current Airflow image using the provided `requirements.txt` and `Dockerfile` in the `/airflow` directory:
     ```bash
     docker build -t extended_airflow:latest .
     ```
   - Update the Airflow image in `/airflow/docker-compose.yaml`:
     ```yaml
     image: ${AIRFLOW_IMAGE_NAME:-extended_airflow:latest}
     ```
   - Start Airflow again:
     ```bash
     docker compose up
     ```
   - Test the connection using the preconfigured DAG (`click-test.py`) in the `/airflow/dags` folder. Run this DAG in Airflow and verify the logs.

---

## **Access Information**

- ClickHouse: [http://localhost:8123/play](http://localhost:8123/play)
- Airflow Webserver: [http://localhost:8080](http://localhost:8080)
- Airflow Flower: [http://localhost:5555](http://localhost:5555)
- Superset: [http://localhost:8088](http://localhost:8088)

---

## **Notes**

- Ensure all Docker services are running smoothly.
- Monitor logs for errors during setup.
- Allocate sufficient system resources for Docker containers.
