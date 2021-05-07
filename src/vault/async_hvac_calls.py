import async_hvac, os.path, json
import load_configs

url=load_configs.file_configs["VAULT_URL"]
token=load_configs.file_configs["VAULT_TOKEN"]
mount_point=load_configs.file_configs["VAULT_MOUNT_POINT"]

def open_connection(url, token):
    client = async_hvac.AsyncClient(url=url,token=token,verify=False)
    return client

async def close_connection(client):
    await client.close()

#Get Secrets
async def get_secrets(pbn): 
    #print("url: {}".format(url))
    #print("token: {}".format(token))
    #print("pbn: {}".format(pbn))
    client = open_connection(url, token)
    get_response = await client.read('apps/'+pbn+'/credentials')
    await close_connection(client)
    if get_response is None:
        #print("Problem occured getting credentials")
        return False
    else:
        return True
    
#Put Secrets
async def put_secrets(pbn):  
    client = open_connection(url, token)
    put_response = await client.write('apps/'+pbn+'/credentials', key='value')
    await close_connection(client)
    if put_response is None:
        #print("Success setting credentials")
        return True
    else:
        return False

#Get Policies
async def get_policy(pbn): 
    client = open_connection(url, token)
    policy = await client.get_policy(pbn+"-policy")
    await close_connection(client)
    if policy is None:
        return False
    else:
        return True

#Put Policies, aways overrides
async def put_policy(pbn): 
    policy_content = """path "apps/"""+pbn+"""/*" {   
    capabilities = ["read"]
    }
    """
    
    client = open_connection(url, token)
    set_policy_response = await client.set_policy(pbn+"-policy", policy_content)
    await close_connection(client)
    
#Get Role
async def get_role(pbn): 
    try:
        client = open_connection(url, token)
        await client.get_role(pbn, mount_point)
        await close_connection(client)
        return True
    except:
        print("Error getting Role")  
        await close_connection(client)
        return False


