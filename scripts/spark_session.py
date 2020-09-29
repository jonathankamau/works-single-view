import configparser
from pyspark.sql import SparkSession

class CreateSparkSession:
    """Contains Methods to extract data from the csv file."""

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('configs/data.cfg')
        self.data_path = config['DATA']['DATA_PATH']
        self.output_path = config['DATA']['OUTPUT_PATH']
        self.spark = self.create_spark_session()


    def create_spark_session(self):
        """Method that creates a spark session."""

        spark = SparkSession \
            .builder \
            .config(
                "spark.jars.packages", 
                "org.apache.hadoop:hadoop-aws:2.7.0",
                ) \
            .getOrCreate()
        
        return spark

           


