import argparse
from azureml.core import Dataset, Datastore
import utils
import os
from azureml.core import Run
from azureml.core import Dataset, Datastore
from azureml.datadrift import DataDriftDetector



@utils.exec_time
def main(model_name):
    print("Connecting to Workspace and Data Store")
    ## Step 1- Connect to Workspace and Dataset
    ws = utils.retrieve_workspace()
    run = Run.get_context()
    config = utils.get_model_config_ws(ws,model_name)


    ## Data Drift monitor
    datastore_name = config['datastore_name']
    datastore = Datastore.get(ws, datastore_name)  
    
    #Baseline dataset
    diabetes_module = Dataset.get_by_name(ws, name=config["data_prep_datasets"]["dataset"])

    cluster_name = config['train_compute_name']

    ## Target Dataset
    target_data_set=Dataset.get_by_name(ws, name="diabetes target")


    ### Data Drift Monitor
    features = ['Pregnancies', 'Age', 'BMI']

    # set up data drift detector
    try:
        monitor = DataDriftDetector.create_from_datasets(ws, 'data-drift', diabetes_module, target_data_set,
                compute_target=cluster_name, 
                frequency='Week', 
                feature_list=features, 
                drift_threshold=.3, 
                latency=24)

    except:
        monitor = DataDriftDetector.get_by_name(ws, 'data-drift')

    run.complete()



def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str)
    args_parsed = parser.parse_args(args_list)
    return args_parsed

if __name__ == '__main__':
    args = parse_args()
    main(
        model_name=args.model_name,
    )



