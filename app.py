from aws_cdk import (
    App, Stack, Duration,
    aws_events, aws_events_targets, 
    aws_lambda, aws_iam
)
from constructs import Construct


SHUTDOWN_DAILY_8PM = "cron(0 20 ? * * *)"
SHUTDOWN_FRIDAY_8PM = "cron(0 20 ? * FRI *)"


class ScheduledCanvasShutdown(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda function
        lambda_function = aws_lambda.Function(
            self, "CanvasShutdown",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset("lambda"),
            handler="lambda.lambda_handler",
            timeout=Duration.seconds(300)
        )
        lambda_function.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
        )

        # Schedule every weekend
        schedule = aws_events.Rule(
            self, "CanvasShutdownSchedule",
            schedule=aws_events.Schedule.expression(SHUTDOWN_FRIDAY_8PM),
            targets=[aws_events_targets.LambdaFunction(lambda_function)],
        )


app = App()
ScheduledCanvasShutdown(app, "ScheduledCanvasShutdown")
app.synth()