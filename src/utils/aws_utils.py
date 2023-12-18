import boto3

class AWSUtils:
# Class for managing native AWS services
    def __init__(self) -> None:
        self.ssm = boto3.client('ssm')

    def get_api_password(self, parameter_name) -> str:
        """
        Return item from AWS parameter store
        """
        response = self.ssm.get_parameter(
            Name = parameter_name, 
            WithDecryption = True
        )

        api_password = response['Parameter']['Value']

        return api_password
