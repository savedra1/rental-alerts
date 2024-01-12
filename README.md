# Automated alerting for the UK rental market
Finding a place to rent in any major UK city is becoming more and more difficult due to the constantly rising prices and demand. To (very slightly) help the situation I've built this Terraform/AWS project that will send live alerts for any new listings posted on the popular property websites. As opposed to signing up for any official property alerts, this approach centralises alerting from multiple listing sources, is completely free of cost, allows for SMS alerting and allows continuous integration on the fly whenever updates are needed. I thought I'd make this repo public in case anyone out there can also benefit. Was also a great learning project to consolidate some terraform and AWS knowledge. 

## How it works
When the source code is executed, Terraform will create an AWS Lambda function with a scheduled EventBridge cron trigger. The code added to the Lambda function will crawl through the specified listing sites looking for property data that matches the requirements specified in the project's `config.json` file. When new properties (posted on the day of execution) are found and have not already been processed for that day, their hrefs will be sent via email and SMS (optionally) to the contact information that was specified for the recipient. The CI workflow (GitHub Actions) allows for easy updates to the config parameters and provides a template for new scraper objects to be added.

## Limitations
Certain rental sites that use Cloudflare are difficult to access from a serverless environment. For example the page source can be retreived locally for `https://zoopla.co.uk` using a browser client like `selenium` or `playwrite`, however, when the same approach is attempted from an AWS ECR image/raw lambda function it gets blocked due to the traffic being associated with an AWS environemnt. Client libraries such as `cloudscraper` all now seem to be outdated for this also. I would recommend using a custom proxy/server or applying for an official API key to use these services instead. 

## Getting started 
**Dependencies**:
- Git CLI local install
- Admin access to an AWS instance
- Terraform to be installed locally (if running the project locally)
- Access to at least one Gmail account

**Important considerations**:
- The notifications are sent via email using Python's `smtplib` library using the Gmail server. This means you should ensure the recipient email [has enabled less secure app access](https://support.google.com/accounts/answer/6010255) and the sender account has [configured a Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)
- Twilio details (optional) can be generated for free [here](https://www.twilio.com/en-us/messaging/channels/sms?utm_source=google&utm_medium=cpc&utm_term=mass%20messaging%20system&utm_campaign=G_S_EMEA_NB_SMS_T1_EN_NV&cq_plac=&cq_net=g&cq_pos=&cq_med=&cq_plt=gp&gad_source=1&gclid=CjwKCAiA44OtBhAOEiwAj4gpOdUQUIqd9zgYif9rIvFVnoGPH_sx3xBoQAw3BSbtaBB1KdbKeoTavhoCkRQQAvD_BwE) but may need updating periodically to avoid having to spend money.
- Code for any additional sites you'd like to scrape can be added to the `rental-alerts/scrapers` directory on an ad-hoc basis.
- The cron schedule in use can be found in `aws-infra/cloudwatchevent_rule.tf` and can be updated there as and when. 
- If the developers of the sites being scraped make any changes this may break the project and you will be notified of thi by email only. This will require pulling the page source manually (making use of the `.local-dev` resources where necessary) and updating the `rental-alerts/utils/constants.py` file with new page separators in order to extract the property information. 

**Required environment variable definitions**:
- *AWS_ACCESS_KEY*: _The AWS access key for your AWS service account user._
- *AWS_SECRET_KEY*: _The AWS secret key for your service account user._
- *S3_STATE_BUCKET_NAME*: _The name of the AWS S3 bucket used to hold your Terraform state file._
- *SMTP_RECIPIENT_EMAIL*: _The email used to receive the alerts._
- *SMTP_SENDER_EMAIL*: _The Gmail email used to send the alerts._
- *SMTP_SENDER_KEY*: _The Gmail App password used to authenticate with Python's SMTP Gmail server_
- *TWILIO_AUTH_TOKEN*: _The authentication key for your Twilio account (optional)_
- *TWILIO_RECIPIENT*: _The mobile number to receive the alerts (optional)_
- *TWILIO_SENDER*: _Your twilio sender mobile number(optional)_
- *TWILIO_SID*: _Your twilio account's SID (optional)_ 


### Staging
1. Clone this repo from the root folder with `git clone https://github.com/savedra1/rental-alerts.git`.

2. Create an AWS user with the following permissions:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
             {
                "Effect": "Allow",
                "Action": [
                    "lambda:CreateFunction",
                    "lambda:UpdateFunctionCode",
                    "lambda:UpdateFunctionConfiguration",
                    "lambda:DeleteFunction",
                    "lambda:AddPermission",
                    "lambda:RemovePermission"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ] 
                "Resource": "*"
            }
            {
                "Effect": "Allow",
                "Action": [
                    "events:*",
                    "cloudwatch:*"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateRole",
                    "iam:AttachRolePolicy",
                    "iam:PutRolePolicy",
                    "iam:PassRole",
                    "iam:GetRole",
                    "iam:ListRolePolicies",
                    "iam:ListAttachedRolePolicies",
                    "iam:ListInstanceProfilesForRole",
                    "iam:DeleteRole",
                    "iam:DetachRolePolicy",
                    "iam:UpdateAssumeRolePolicy"
                ],
                "Resource": "*"
            }
        ]
    }
    ```
    _Note: Be aware this AWS user will be fairly priviledges so be careful when saving their AWS access key and secret key. It's also recommended to add these permissions to an IAM group which the user can then be added to rather than to the user directly._

3. Create an AWS s3 bucket manually with a folder called inside the bucket called `dev`. Also ensure the region set in the project's `/aws-infra/main.tf` is correct. E.g: 
    ```
    provider "aws" {
        region = "eu-west-1"
    }

    terraform {
        backend "s3" {
        bucket = var.S3_STATE_BUCKET_NAME
        key    = "dev/terraform.tfstate"
        region = "eu-west-1"
        }
    }

    ```

4. Add your rental preferences to the `rental-alerts/resourcesconfig.json` file.

### Deploying with Github Actions
If you'd like to set this up with the same CI pipeline as myself, where the Terraform actions are all taken in Github Actions, follow this section. Otherwise you can skip this section for instructions on local deployemt. 

1. Create your own private repo in GitHub and set that as the new remote origin for your local clone with `git remote set-url origin https://github.com/you/your-repo.git`.

2. Add the following environemnt secrets to your Github repo:
    - AWS_ACCESS_KEY *
    - AWS_SECRET_KEY *
    - S3_STATE_BUCKET_NAME *
    - SMTP_RECIPIENT_EMAIL *
    - SMTP_SENDER_EMAIL *
    - SMTP_SENDER_KEY *
    - TWILIO_AUTH_TOKEN _(optional)_
    - TWILIO_RECIPIENT _(optional)_
    - TWILIO_SENDER _(optional)_
    - TWILIO_SID _(optional)_

3. Make sure the default branch in your Github repo is named `main`.

4. Push your changes to the main branch, triggering the Github actions workflow. Once this has completed the build, you can log back into the AWS console to spot-check and test the newly created Lambda function. 

### Local deployment
If you don't intend to set up a CI pipeline and just want to spin up the resources from your local machine, you will need to take the following steps: 

1. Install Terraform on your local machine if it is not already.

2. In your terminal, move into the `aws-infra` folder from the root directory with `cd aws-infra`.

3. Export your AWS credentials to your terminal session as enironment variables with the following commands:
    ```
    export AWS_ACCESS_KEY_ID=your_aws_users_access_key_id
    export AWS_SECRET_ACCESS_KEY=your_aws_users_secret_access_key_id
    ```
    _This will tell terraform to use these credentials when accessing your S3 state bucket and building your resources._ 

4. Run the command `terraform init` and you will be prompted for each required environment variable in your terminal. Any parameters from the following list that are tagged as _(optional)_ can be skipped by typing _Enter_ if you don't wish to make use of them:
    - S3_STATE_BUCKET_NAME *
    - SMTP_RECIPIENT_EMAIL *
    - SMTP_SENDER_EMAIL *
    - SMTP_SENDER_KEY *
    - TWILIO_AUTH_TOKEN _(optional)_
    - TWILIO_RECIPIENT _(optional)_
    - TWILIO_SENDER _(optional)_
    - TWILIO_SID _(optional)_

8. Run the command `terraform plan` to view what will be created in AWS.

9. Run the command `terraform apply` to deploy your resources.

10. Future updates to your project's `config.json` file can then be added at any time by simply saving your changes locally and running back throgh steps 6-9. 


## Maintainers
[me](https://github.com/savedra1)



