# Shutdown Amazon SageMaker Canvas on a Schedule

![architecture](./images/scheduled-canvas-shutdown.png)

Run this CloudFormation template to automatically shutdown Amazon SageMaker Canvas apps. You can choose whether to shutdown every day at 8PM or on Fridays at 8PM. Default behaviour: Friday at 8PM.

## Steps to deploy:

1. clone this repository
2. `python3 -m virtualenv .venv`
3. `source .venv/bin/activate`
4. `cdk deploy`
5. Enjoy!

## Steps to cleanup: 

Either execute `cdk destroy` from within this folder, or head over to the [AWS CloudFormation stacks](https://console.aws.amazon.com/cloudformation/home/stacks) page, and delete the `ScheduledCanvasShutdown` stack.