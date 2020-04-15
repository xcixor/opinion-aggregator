"""create objects needed at run time
"""
import os
import base64
from django.conf import settings

def create_service_account():
    """create service account
    """
    # print(os.environ.get('DJANGO_SETTINGS_MODULE'), '******settings**********')
    service_account_data = os.environ.get('SERVICE_ACCOUNT')
    account_data = base64.b64decode(service_account_data)
    data = account_data.decode('ascii')
    base_dir = settings.BASE_DIR
    root_dir = base_dir[:-13]
    filename = "{}/account.json".format(root_dir)
    with open(filename, "w") as f:
        f.write(data)