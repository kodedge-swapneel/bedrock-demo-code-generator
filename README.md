# bedrock-demo-code-generator

## AWS Lambda Inline policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": "*"
        }
    ]
}
```

## S3 Bucket Policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

## Lambda Console Test Event:
```
{
  "body": {
    "content": "Write a Python function to reverse a string."
  }
}
```

## API Gateway Console Test Request Body
```
{
  "content": "Write a Python function to reverse a string."
}
```
