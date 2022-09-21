# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from adal import AuthenticationContext
from azureml.core.authentication import TokenAuthentication, Audience


def retrieve_workspace():
    """Retrieve a workspace.

    Args:
        None

    Returns:
        Workspace: The Azure Machine Learning workspace object

    """

    try:
        ws = Workspace.from_config()
        return ws
    except Exception as e:
        print('Workspace could not be loaded from config file.')
        print(e)

    try:
        print('Trying to load worspace from subscription')
        ws = Workspace.get(
            name=os.environ['AML_MLOPS'],
            resource_group=os.environ['aml_mlops'],
            subscription_id=os.environ['c916f962-17ec-4652-9975-7cc42fabc7b1']
        )
        return ws
    except Exception as e:
        print('Workspace not found.')
        print(e)

    try:
        print('Trying Tokenization')
        def get_token_for_audience(audience):
            
            client_id = "48bf7b8c-8ada-4189-b66a-1a5a6bad6d96"
            client_secret ="iTw8Q~E3hFnj96x4NxnIg8ayw9pNLD4j1cbj8bAi"
            tenant_id = "e4e34038-ea1f-4882-b6e8-ccd776459ca0"
            auth_context = AuthenticationContext("https://login.microsoftonline.com/{}".format(tenant_id))
            resp = auth_context.acquire_token_with_client_credentials(audience,client_id,client_secret)
            token = resp["accessToken"]
            return token

        token_auth = TokenAuthentication(get_token_for_audience=get_token_for_audience)



        ws = Workspace(
            subscription_id="c916f962-17ec-4652-9975-7cc42fabc7b1",
            resource_group="aml_mlops",
            workspace_name="AML_MLOPS",
            auth=token_auth
            )
        return ws
    except Exception as e:
        print('Connection via SP failed:', e)

    print('Error - Workspace not found')
    print('Error - Shuting everything down.')
    sys.exit(-1)
