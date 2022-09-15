import boto3
import json
import logging

# Add any user you want to skip here below
users_exceptions = ['USER-PROFILE-TO-SKIP']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def clean_sagemaker_studio():
    client = boto3.client("sagemaker")
    domains = client.list_domains()['Domains']
    for dom in domains:
        domain_id = dom["DomainId"]
        users = client.list_user_profiles(DomainIdEquals=domain_id)['UserProfiles']
        for u in users:
            user = u['UserProfileName']
            if user in users_exceptions:
                logger.info(f'Skipping user {user} from domain {domain_id}')
                continue
            apps = client.list_apps(DomainIdEquals=domain_id, UserProfileNameEquals=user)['Apps']
            for a in apps:
                app_type, app_name, app_status = a['AppType'], a['AppName'], a['Status']
                # Only clean Canvas apps - remove if you want to clean up everything
                if app_type != 'Canvas':
                    logger.info(f'Ignoring app {app_name} of type {app_type}')
                    continue
                if app_status != 'InService':
                    logger.info(f'Cannot delete app {app_name} ({app_type}) of user {user} in domain {domain_id} because its status is {app_status.upper()}')
                    continue
                # Delete the app
                logger.info(f'Deleting app {app_name} ({app_type}) of user {user} in domain {domain_id}')
                client.delete_app(
                    DomainId=domain_id, UserProfileName=user,
                    AppType=app_type, AppName=app_name
                )
        

def lambda_handler(event, context):
    try:
        clean_sagemaker_studio()
        return {
            'statusCode': 200,
            'body': json.dumps('SageMaker Studio has been cleaned.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('There has been a problem with cleaning SageMaker Studio.'),
            'errorMessage': json.dumps(e)
        }

