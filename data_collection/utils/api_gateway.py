# helpers to both create and shut down api gateways for proxy requests
from requests_ip_rotator import ApiGateway
import sys, os
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))
from config.config import config_aws

def create_api_gateway() -> ApiGateway:
    params = config_aws()
    gateway = ApiGateway("https://1.1.1.1:8080",
                        access_key_id=params['key'],
                        access_key_secret=params['secret'])
    gateway.start(force=True)
    return gateway
    
# @TODO this isn't working right now
def shutdown_api_gateway(gateway: ApiGateway) -> str:
    gateway.shutdown()
    return('Shut Down Gateway.')

