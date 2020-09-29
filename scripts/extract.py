import unicodedata
from scripts.spark_session import CreateSparkSession
from pyspark.sql.functions import collect_set, concat_ws, udf, col
import os


class ExtractWorks(CreateSparkSession):
    """Contains Methods to extract data from the csv file."""

    def extract_data(self):
        """Method to extract data from the csv file."""

        works_data = self.data_path + '*'
        

        works_data_df = self.spark.read.load(
            works_data,
            format="csv",
            header="true"
        )
        unicode_conversion = udf(
            lambda value: unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode())

        works_data_df = works_data_df.withColumn(
            'converted_title', unicode_conversion(col('title')))
        
        works_data_df = works_data_df.withColumn(
            'converted_contributors', unicode_conversion(col('contributors'))) 

        reconciled_data = works_data_df.select('*') \
                                            .groupBy('iswc') \
                                            .agg(concat_ws(', ', collect_set('converted_title')) \
                                            .alias('title'),
                                            concat_ws('|', collect_set('converted_contributors')) \
                                            .alias('contributors'),
                                            concat_ws(', ', collect_set('source')) \
                                            .alias('sources')) \
                                            .dropDuplicates() \
                                            .na.drop()
                                            
        return reconciled_data
