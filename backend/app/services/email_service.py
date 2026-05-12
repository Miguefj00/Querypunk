import os
import smtplib
from email.message import EmailMessage


class EmailService:

    @staticmethod
    def build_html_email(content: str):
        """ Builds the base HTML template for system emails. """
        return f"""
        <html>
        <body style="font-family: Arial, Helvetica, sans-serif; background:#f4f6f8; padding:40px;">
            
            <table width="100%" style="max-width:600px;margin:auto;background:white;border-radius:8px;padding:30px;border:1px solid #e5e7eb;">
                
                <tr>
                    <td style="text-align:center;padding-bottom:20px;">
                        <h2 style="margin:0;color:#1f2937;">Querypunk</h2>
                    </td>
                </tr>

                <tr>
                    <td style="color:#374151;font-size:15px;line-height:1.6;">
                        {content}
                    </td>
                </tr>

                <tr>
                    <td style="padding-top:30px;font-size:12px;color:#9ca3af;text-align:center;">
                        Este es un correo automático del sistema Querypunk.
                    </td>
                </tr>

            </table>

        </body>
        </html>
        """

    @staticmethod
    def send_email(to_email: str, subject: str, body: str, html_body: str | None = None):
        """ Sends an email via SMTP (plain text + optional HTML). """
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_name = os.getenv("SMTP_SENDER_NAME", "Querypunk")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{sender_name} <{smtp_user}>"
        msg["To"] = to_email

        msg.set_content(body)

        if html_body:
            msg.add_alternative(html_body, subtype="html")

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

    @staticmethod
    def send_existing_user_added(email: str, group_name: str):
        """ Notifies an existing user that they were added to a group. """
        subject = "Has sido asignado a un grupo"

        body = f"""
            Bienvenido/a de nuevo,
            
            Has sido añadido a un nuevo grupo: {group_name}
            
            Puedes acceder al sistema con tu cuenta habitual.
            
            Saludos.
            """

        html_content = f"""
        <p>Bienvenido/a de nuevo,</p>

        <p>
        Has sido añadido a un nuevo grupo:<br>
        <strong>{group_name}</strong>
        </p>

        <p>Puedes acceder al sistema con tu cuenta habitual.</p>

        <p>Saludos.</p>
        """

        html_body = EmailService.build_html_email(html_content)

        EmailService.send_email(email, subject, body, html_body)

    @staticmethod
    def send_new_user_credentials(email: str, username: str, password: str, group_name: str):
        """ Sends initial credentials to a newly created user. """
        subject = "Tu cuenta ha sido creada"

        body = f"""
            Bienvenido/a a Querypunk,
            
            Le informamos de que su cuenta ha sido dada de alta en el sistema correctamente.
            
            Usuario: {username}
            Contraseña: {password}
            
            Grupo asignado: {group_name}
            
            Puedes cambiar tu contraseña al iniciar sesión.
            
            Saludos.
            """

        html_content = f"""
        <p>Bienvenido/a a <strong>Querypunk</strong>,</p>

        <p>
        Le informamos de que su cuenta ha sido dada de alta en el sistema correctamente.
        </p>

        <table style="border-collapse:collapse;margin:20px 0;">
            <tr>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;"><strong>Usuario</strong></td>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;">{username}</td>
            </tr>
            <tr>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;"><strong>Contraseña</strong></td>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;">{password}</td>
            </tr>
            <tr>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;"><strong>Grupo</strong></td>
                <td style="padding:8px 12px;border:1px solid #e5e7eb;">{group_name}</td>
            </tr>
        </table>

        <p>Puedes cambiar tu contraseña al iniciar sesión.</p>

        <p>Saludos.</p>
        """

        html_body = EmailService.build_html_email(html_content)

        EmailService.send_email(email, subject, body, html_body)
