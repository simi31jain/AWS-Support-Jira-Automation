# AWS-Support-Jira-Automation

# AWS Support Case Integration with Partner Ticketing System

# Overview of the Project
AWS Support Case Integration with Partner Ticketing System is a serverless solution designed to automate the integration between AWS Support Cases and a Partner's ticketing system. The primary goal of this integration is to ensure that updates from AWS on support cases are seamlessly ingested into the Partner's ticketing system. This enables AWS Partner operations staff to stay informed about support case developments and ensures that information obtained from AWS Support contributes to enhancing the Partner’s internal knowledge base.

# Functionality
1. AWS Support Case Event Handling
CreateCase Event: When a new AWS Support Case is created, this Lambda function automatically generates a corresponding Jira issue. It extracts relevant information such as the Case ID, severity, and description to populate the Jira issue.
AddCommunicationToCase Event: This event is triggered when there's communication (e.g., updates, replies) on an existing AWS Support Case. The Lambda function retrieves these communications and adds them as comments to the corresponding Jira issue.

2. Jira Integration
Creating Jira Issues: The Lambda function utilizes the Jira REST API to create Jira issues. It constructs the necessary payload with the extracted AWS Support Case details and sends a POST request to the Jira API endpoint.
Adding Comments to Jira Issues: Communications/messages associated with AWS Support Cases are fetched and appended as comments to the respective Jira issues. This helps in maintaining a consolidated view of the case's history within Jira.
Setup
To deploy and configure this Lambda function, follow these steps:

AWS Lambda Setup: Create a Lambda function in the AWS Management Console and paste the code provided in the lambda_function.py file.
Environment Variables: Set up the necessary environment variables for your Jira instance, including JIRA_USERNAME, API_TOKEN, and PROJECT_KEY.

Permissions: Ensure that the Lambda function has the required IAM permissions to interact with AWS Support and Jira APIs.
CloudWatch Event Rule: Create CloudWatch Event Rules to trigger the Lambda function based on AWS Support Case events (CreateCase and AddCommunicationToCase).
Configuration
Adjust the configuration parameters within the Lambda function code to match your environment and requirements. These include Jira API endpoint URLs, issue types, and project keys.

Dependencies
Boto3: AWS SDK for Python to interact with AWS Support service.
Requests: HTTP library for making requests to Jira REST API.
Base64: Encoding library to handle authentication for Jira API requests.


# Acknowledgments
AWS Support and Jira API documentation.

https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/#about
https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-add-comment-8946422/#:~:text=The%20Rest%20API%20allows%20you,part%20of%20editing%20an%20issue.



Feel free to customize this template according to your specific use case and audience!

