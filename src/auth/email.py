# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# def send_verification_email(email: str, token: str):
#     message = Mail(
#         from_email=os.getenv("SENDGRID_FROM_EMAIL"),
#         to_emails=email,
#         subject="Email Verification",
#         html_content=f"Please click the following link to verify your email: <a href='http://localhost:8000/api/auth/verify-email?token={token}'>Verify Email</a>",
#     )
#     try:
#         sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
#         response = sg.send(message)
#     except Exception as e:
#         print(e.message)

# def send_password_reset_email(email: str, token: str):
#     message = Mail(
#         from_email=os.getenv("SENDGRID_FROM_EMAIL"),
#         to_emails=email,
#         subject="Password Reset",
#         html_content=f"Please click the following link to reset your password: <a href='http://localhost:8000/api/auth/reset-password?token={token}'>Reset Password</a>",
#     )
#     try:
#         sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
#         response = sg.send(message)
#     except Exception as e:
#         print(e.message)
