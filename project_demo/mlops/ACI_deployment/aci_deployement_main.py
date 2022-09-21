import urllib.request
from azureml.core.model import Model
from azureml.core import Workspace, Environment
from azureml.core import Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import Model

# Download model
urllib.request.urlretrieve("<URL for the model present in the artifact>", "<Model_name in pkl formal>")

# Register model
model = Model.register(ws, model_name="", model_path="./<Model_name as pkl format>")

ws = Workspace.from_config()
env = Environment.get(workspace=ws, name="<Enviroment_name which is already registered>")


inference_config = InferenceConfig(
    environment=env,
    source_directory="./",
    entry_script="./score.py",
)

## Port can be changed accordingly
deployment_config = LocalWebservice.deploy_configuration(port=6789)

## Final Deployment
deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)
service = Model.deploy(ws, "aciservice", [model], inference_config, deployment_config)
service.wait_for_deployment(show_output = True)
print(service.state)


### To deploy as a local service
"""service = Model.deploy(
    ws,
    "myservice",
    [model],
    dummy_inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)"""