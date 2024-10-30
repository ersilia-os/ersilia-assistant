# Deploying Llamafile on Lambda - Python Stack

## Introduction

This approach is very much inspired from Ken Collins' [toy project](https://www.unremarkable.ai/serverless-ai-inference-with-gemma-2-using-mozillas-llamafile-on-aws-lambda/).

I am not sure if presently this is the right solution or not, but we have a strong enough use case to not provision a dedicated EC2 instance since this is going to be a toy demo and we do not expect heavy workload demands. Unfortunately neither Lambda nor Fargate support GPU runtimes, so this is as good a choice as any in the serverless realm within AWS.

The stack involves the following components:
1. [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for its ease of use and version controlling the Lambda configuration. As far as I understand, SAM is an [extension](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html) of AWS CloudFormation with a dedicated usecase for Serverless deployments. 
2. [Lambda Web Adapter](https://aws.amazon.com/blogs/compute/using-response-streaming-with-aws-lambda-web-adapter-to-optimize-performance/) which is a relatively new tech supporting response streaming with the advantage of not needing to write code adhering to Lambda's [handler](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html) paradigm.

## Commands

Make sure you are logged into AWS and have sufficient permissions to run these commands. You will probably also need to install the [AWS CLI](https://aws.amazon.com/cli/).

This directory is organised as follows:

```
├── llamafile-infra
│   ├── bin
│   └── src
│       └── tmp
│           └── llamafile
```

- `bin` contains the scripts to build and deploy the Lambda stack.

- `src` contains the code to run Llamafile inside a Docker container, and the Dockerfile to build the said container.

To install a Llamafile and only build the lambda stack:

```bash
cd bin
./build.sh
```

To deploy the Lambda stack, and optionally build if needed:

```bash
cd bin
./deploy.sh
```

The `template.yaml` file declares the Lambda function in terms of which image to use and which resources to provision. 

When the stack is deployed using `sam deploy` (found in `bin/deploy.sh`), it creates a `samconfig.toml` file with the exact state of the presently deployed Lambda stack.

## How everything works

I am mostly writing this down for my future self, but hope it helps anyone landing here.

Lambda Web Adaptor (LWA) listens for a process running at port 8080. In the ideal case this tool was intended to be used in, this would be a Flask app, or a Node.js app, or an Nginx proxy, [etc](https://github.com/awslabs/aws-lambda-web-adapter/tree/main/examples). 

Since Llamafile runs llama.cpp's server written in C++ (for which I don't know if there's a Lambda runtime), the Lambda 'handler' in this stack simply starts the Llamafile server through a subprocess call, and then exits, leaving the Llamafile server running on port 8080, which the LWA is happy passing traffic to. Quite hacky but also very clever!

## Note on Lambda constraints

- At this time, Lambdas can only be provisioned with upto 10G memory, and the vCPUs are allocated proportional to the memory provisioned. With 10G, we get 6 vCPUs.

- A Lambda invokation can only run for upto 15 minutes at a time.

- For using container runtimes in Lambda, the Docker image should not be more than 10G in size.