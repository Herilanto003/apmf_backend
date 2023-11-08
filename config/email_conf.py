from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


async def send_code(email: str, code: str):    
    html = f"Veuillez entrer dans le formulaire d'activation ce code <br/> <strong>{code}</strong>"

    message = MessageSchema(
        subject="CODE D' ACTIVATION",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    await fm.send_message(message)
    # return JSONResponse(content={"message": "email has been sent"})
    print("mmmm")


conf = ConnectionConfig(
    MAIL_USERNAME = "herilantolouis@gmail.com",
    MAIL_PASSWORD = "mnuzehstltequbpb",
    MAIL_FROM = "herilantolouis@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="STATISTIQUE PORTUAIRE",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)


fm = FastMail(conf)


async def send_c():
    return await send_code('herilantolouis@gmail.com', "ddddd")

send_c()