import smtplib
from email.message import EmailMessage
from emailo_config import *
from string import Template
from sqlalchemy.orm import sessionmaker
from model import engine, User, Subscription, Invoice
import uuid
from datetime import datetime

Session = sessionmaker(bind=engine)


class Invoices:
    def __init__(self, username):
        self.session = Session()
        self.username = username
        self.user = self.session.query(User).filter_by(username=username).first()
        self.email = self.session.query(User.email).filter_by(id=self.user.id).first()
        self.name = self.session.query(User.name).filter_by(id=self.user.id).first()
        self.date = self.session.query(Subscription.date).filter_by(user_id=self.user.id)

    def invoice(self):
        while True:
            new_uuid = str(uuid.uuid4())
            existing_user = self.session.query(Invoice).filter_by(id=new_uuid).first()
            if not existing_user:
                break

        email = EmailMessage()
        email["from"] = f"Stock & Crypto App <{EMAIL}>"
        email["to"] = self.email
        email["subject"] = "Invoice"

        with open("templates/invoice.html", mode="r", encoding="utf-8") as f:
            html_text = f.read()

        changes = {
            "today": datetime.utcnow(),
            "uuid": new_uuid,
        }
        template = Template(html_text)
        html_text = template.substitute(changes)

        email.set_content(html_text, "html")

        with smtplib.SMTP(host=SMTP_HOST, port=PORT) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.login(EMAIL, PASSWORD)
            smtp_server.send_message(email)

        new_invoice = Invoice(
            id=new_uuid,
            username=self.username
        )

        self.session.add(new_invoice)
        self.session.commit()
        self.session.close()

        return
