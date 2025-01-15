For traefik deployment,
```
first add the helm chart
show values
add the trusted ips of vpc and add annotation for nlb
then helm install with values
get the loadbalancer ips and put them in values then do helm upgrade
k create deploy web-server...
k expose --port 80
k create ingressroute
check it in browser
```
`
For jenkins

```
sh "aws sts assume-role --role-arn arn:aws:iam::account-id:role/role-name --role-session-name session-name --duration-seconds 3600 --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' --output text | tr '\t' '\n' > env_vars"

sh "cp env_vars temp_vars"

sh "echo 'export AWS_ACCESS_KEY_ID='$(awk 'NR==1' temp_vars) > env_vars"
sh "echo 'export AWS_SECRET_ACCESS_KEY='$(awk 'NR==2' temp_vars) >> env_vars"
sh "echo 'export AWS_SESSION_TOKEN='$(awk 'NR==3' temp_vars) >> env_vars"

sh "rm temp_vars"


sh "source env_vars"


sh "aws eks --region region update-kubeconfig --name cluster-name --role-arn arn:aws:iam::account-id:role/role-name"


sh "echo $KUBECONFIG"


sh "kubectl apply -f path/to/application.yaml"

```

Another way for jenkins deployment.
```
aws sts assume-role --role-arn arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME --role-session-name SESSION_NAME --duration-seconds 3600 --output json > role_credentials.json


aws configure set aws_access_key_id $(cat role_credentials.json | jq .Credentials.AccessKeyId | tr -d '"') --profile dev
aws configure set aws_secret_access_key $(cat role_credentials.json | jq .Credentials.SecretAccessKey | tr -d '"') --profile dev
aws configure set aws_session_token $(cat role_credentials.json | jq .Credentials.SessionToken | tr -d '"') --profile dev


aws eks update-kubeconfig --name my-cluster --region us-west-2 --role-arn arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME --profile dev

try:
    # code that uses the session token
    # deploy your application to EKS cluster
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ExpiredToken':
        # Get the new temporary credentials
        sts_client = boto3.client('sts')
        response = sts_client.assume_role(
            RoleArn='arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME',
            RoleSessionName='session_name'
        )
        # Create a new session and update the dev profile
        session = boto3.Session(
            aws_access_key_id=response['Credentials']['AccessKeyId'],
            aws_secret_access_key=response['Credentials']['SecretAccessKey'],
            aws_session_token=response['Credentials']['SessionToken']
        )
        # Deploy your application to EKS cluster



try:
    # code that uses the session token
    # deploy your application to EKS cluster
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ExpiredToken':
        # Get the new temporary credentials
        !aws sts get-session-token --duration-seconds 3600 --output json > role_credentials.json
        export AWS_ACCESS_KEY_ID=$(cat role_credentials.json | jq .Credentials.AccessKeyId | tr -d '"')
        export AWS_SECRET_ACCESS_KEY=$(cat role_credentials.json | jq .Credentials.SecretAccessKey | tr -d '"')
        export AWS_SESSION_TOKEN=$(cat role_credentials.json | jq .Credentials.SessionToken | tr -d '"')
        
        # Add the new credentials to the dev profile
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile dev
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile dev
        aws configure set aws_session_token $AWS_SESSION_TOKEN --profile dev
        
        # Deploy your application to EKS cluster
        
 ```

if virtualbox is not able to ping or connect to the internet we need to use below command and create an active connection and select the network and then activate
nmcli -d
nmtui





