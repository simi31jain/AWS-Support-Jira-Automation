import json
import requests
import boto3
import base64
import os

def lambda_handler(event, context):
    # Extract relevant data from CloudWatch event
    cloudtrail_data = event['detail']

    # Process the CloudTrail data
    print(cloudtrail_data)
    
    support_client = boto3.client('support')
    event_name = cloudtrail_data["eventName"]
    
    if event_name == "CreateCase":
        
        case_id = cloudtrail_data['responseElements']['caseId']
        severity = cloudtrail_data['requestParameters']['severityCode']
        #issue_type = cloudtrail_data['requestParameters']['issueType']
        description = cloudtrail_data['requestParameters'].get('description', 'Check CaseId')
    
        # call Create Jira issue function
        jira_url = "https://simijain123.atlassian.net/rest/api/3/issue"
        jira_username = os.environ['JIRA_USERNAME']
        jira_api_token = os.environ['API_TOKEN']
        
        project_key = os.environ['PROJECT_KEY']
        # Create Jira issue payload
        payload = {
            "fields": {
                "project": {
                    "key": project_key  # Replace with your Jira project key
                },
                "summary": f"AWS Support Case:{case_id}",
                "description": {
                    "content": [
                        {
                            "content": [
                                {
                                    "text": f"{description} {severity}",
                                    "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                "type": "doc",
                "version": 1
                },
                "issuetype": {
                    "name": "Task"
                }
            }
        }
        
        # Jira API request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{jira_username}:{jira_api_token}".encode()).decode()
        }

        # Send request to create Jira issue
        response = requests.post(jira_url, headers=headers, json=payload)

        # Check if request was successful
        if response.status_code == 201:
            print("Jira ticket created successfully")
        else:
            print("Failed to create Jira ticket")
            print(response.text)
            
     
    elif event_name == "AddCommunicationToCase":
        cloudtrail_data = event['detail']
        caseId = cloudtrail_data['requestParameters']['caseId']
        print("caseId", caseId)
        # Retrieve communications/messages associated with the case
        
        response = support_client.describe_cases(
            caseIdList=[caseId]
        )
        
        print(response)
    
        
        # Extract messages from the response
        communications = response['cases'][0]['recentCommunications']['communications']
        #messages = [communication["body"] for communication in communications]
        messages = [communications[0]["body"]]
        print("messages---->", messages)
        
        #messages = ["Reply to the case", "Cases Resolved", "Get Back To You in 24 hrs"]
        print(f"Case ID: {caseId}")
        
        for communication in communications:
            sender = communication['submittedBy']   # Extract details from each communication
            message = communication['body']
            created_at = communication['timeCreated']
            
            # Print or process the details as needed
            print("Sender:", sender)
            print("Message:", message)
            print("Created At:", created_at)
         
        issue_key = get_issue_key_by_summary(caseId)
        # Add comments to the Jira issue
        if issue_key :
            add_comment_to_jira(issue_key, messages,sender,created_at)
        else:
            print("issue key is None")
    else:
        print("Event is not relevant for this Lambda function.")

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed')
    }
 

def add_comment_to_jira(issue_key,messages,sender,created_at):
    # Jira API endpoint
    jira_url = f"https://simijain123.atlassian.net/rest/api/2/issue/{issue_key}/comment"
    print("jira_url for comment",jira_url,messages,created_at)

    # Jira authentication credentials
    jira_username = os.environ['JIRA_USERNAME']
    jira_api_token = os.environ['API_TOKEN']
    
    comment_body = f"Sender: {sender} , Created At: {created_at}\n"
    comment_body += "\n".join(messages)
    
    # Create payload to add comments to the Jira issue
    add_comment_payload = {
        
        #"body": "AWS Support Messages and sender:\n" + "\n".join(messages)
        "body": f"AWS Support Messages and sender: \n {comment_body}"
        
    }
    print(add_comment_payload)
    #get_issue_key_by_summary(summary)
    
    # Jira API request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f"{jira_username}:{jira_api_token}".encode()).decode()
    }

    # Send request to add comments to the Jira issue
    response = requests.post(f"{jira_url}", headers=headers,json=add_comment_payload )
    print("Status of Post method: ",response.status_code)
    print("response",response)
    # Check if request was successful
    
    if response.status_code == 200 or response.status_code == 201:
        print("Comments added to Jira ticket successfully")
    else:
        print("Failed to add comments to Jira ticket")
        print("response text",response.text)
   
def get_issue_key_by_summary(caseId):
   # Jira API endpoint for searching issues
    
    jira_url = f"https://simijain650.atlassian.net/rest/api/2/search?jql=project='TEST' AND summary~'AWS Support Case:{caseId}'"
    print(jira_url)
    
    jira_username = os.environ['JIRA_USERNAME']
    jira_api_token = os.environ['API_TOKEN']

    # Jira API request headers
    headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{jira_username}:{jira_api_token}".encode()).decode()
        }
    auth = (jira_username, jira_api_token)
    
    jql_query = f'project = "TEST" AND summary ~ "AWS Support Case:{caseId}"'
    
    # Payload for the search request
    params = {
        'jql': jql_query
    }
    print("params -->",params)
    # Send request to search for the issue
    response = requests.get(jira_url, headers=headers)
    #response = requests.get(jira_url, headers=headers, params=params, auth=auth)
    print("response----------------->",response.json(), response.status_code)
    
    # Check response status
    if response.status_code == 200:
        # Parse response JSON
        response_json = response.json()
        issues = response_json['issues']
        if issues:
            issuer_key = issues[0]['key']                      # Return the key of the first issue found
            print(issuer_key)
            return issuer_key
        else:
            return None
    else:
        return None