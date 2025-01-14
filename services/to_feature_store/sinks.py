import hopsworks
import pandas as pd
from quixstreams.sinks.base import BatchingSink, SinkBackpressureError, SinkBatch

# https://www.realworldml.net/products/building-a-better-real-time-ml-system-together-cohort-3/categories/2156666851/posts/2183413377
# Code example

# https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/branch-4.1/integrations/great_expectations/fraud_batch_data_validation.ipynb
# open from hopsworks


class HopsWorksFeatureStoreSink(BatchingSink):
    """
    Some sink writing data to a database
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],  # list of str
        feature_group_event_time: str,
    ):
        """
        Establish connection to the Hopsworks Feature Store
        """

        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version

        # Establish connection to the Hopsworks Feature Store
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()

        # Get the feature group
        self._feature_group = self._fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,  # For live streaming
        )

        # Call constructor of the base class to make sure batches are initialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Simulate some DB connection here
        data = [item.value for item in batch]

        data = pd.DataFrame(data)

        try:
            # Try to write data to the db
            self._feature_group.insert(data)
        except Exception as err:
            # In case of timeout, tell the app to wait for 30s
            # and retry the writing later
            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err
