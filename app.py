#!/usr/bin/env python3

from aws_cdk import core

from workshop.stack.production_stack import ProductionStack
from workshop.stack.cicdpipeline_stack import CICDPipelineStack
from workshop.stack.webapplication_stack import WebApplicationStack
import os

UserName = os.getenv("UserName")
EmailAddress = os.getenv("EmailAddress")
Region = os.getenv("Region")

app = core.App()
Production = ProductionStack(app, 
    "Production-" + UserName.lower(),
    UserName = UserName.lower(),
    EmailAddress = EmailAddress,
    env={'region': Region}
)

WebApplication = WebApplicationStack(app, 
    "WebApplication-" + UserName.lower(),
    UserName = UserName.lower(),
    EmailAddress = EmailAddress,
    Vpc=Production.getVpc(),
    StateMachine = Production.getStateMachine(),
    env={'region': Region}
)

CICDPipeline = CICDPipelineStack(app, 
    "CICDPipeline-" + UserName.lower(),
    UserName = UserName.lower(),
    EmailAddress = EmailAddress,
    BatchRepo = Production.getEcrRepo(),
    WebRepo = WebApplication.getEcrRepo(),
    WebService = WebApplication.getService(),
    env={'region': Region}
)


app.synth()
