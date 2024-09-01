from storages.backends.azure_storage import AzureStorage
import os
from dotenv import load_dotenv
load_dotenv()


class AzureMediaStorage(AzureStorage):
    account_name = 'storagedjango'  # Replace with your Azure account name
    account_key = 'PJII8m578uyDNPm4mKZTtf+xRAOEgaYPMVksizZIvK/hcavi3cI6KRIX0hyZtpjCwqNhYKc3klCB+AStn4mFmw=='  # Replace with your Azure account key
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'storagedjango'  # Replace with your Azure account name
    account_key = 'PJII8m578uyDNPm4mKZTtf+xRAOEgaYPMVksizZIvK/hcavi3cI6KRIX0hyZtpjCwqNhYKc3klCB+AStn4mFmw=='  # Replace with your Azure account key
    azure_container = 'static'
    expiration_secs = None
