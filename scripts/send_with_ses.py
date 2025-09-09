import os, time, boto3


ses = boto3.client("sesv2", region_name=os.environ["AWS_REGION"])


def send_email(to_addr, subject, html):
ses.send_email(
FromEmailAddress=os.environ["SES_SENDER"],
Destination={"ToAddresses":[to_addr]},
Content={"Simple":{"Subject":{"Data":subject},"Body":{"Html":{"Data":html}}}},
EmailTags=[{"Name":"segment","Value":"auto"}]
)
time.sleep(0.2)
