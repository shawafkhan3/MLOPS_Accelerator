from azureml.pipeline.core import PublishedPipeline
import requests
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication()
auth = interactive_auth.get_authentication_header()

p="<Pipeline RestEndpoint>"
response = requests.post(p,
                         headers=auth,
                         json={"ExperimentName": "classification_pipeline"})


response.json()