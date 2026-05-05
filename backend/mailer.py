import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from pathlib import Path

# Chargement des variables d'environnement
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "Protocole_7_Jours_Final.pdf")

def send_delivery_email(customer_email: str):
    """
    Envoie le guide PDF au client après un achat réussi.
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print("Erreur: Paramètres SMTP manquants dans le .env")
        return False

    try:
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = customer_email
        msg['Subject'] = "Félicitations ! Votre Guide Protocole 7 Jours est arrivé 🚀"

        body = f"""
        Bonjour,

        Merci pour votre confiance ! 
        
        Vous trouverez ci-joint votre guide complet "Protocole 7 Jours". 
        C'est le premier pas vers une prospection automatisée et efficace pour votre activité de photographe.

        Si vous avez des questions, n'hésitez pas à répondre à cet email.

        Bonne lecture et beaucoup de succès dans vos prochaines missions !

        L'équipe Protocole 7 Jours
        """
        msg.attach(MIMEText(body, 'plain'))

        # Ajout du PDF en pièce jointe
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= Protocole_7_Jours_Final.pdf")
                msg.attach(part)
        else:
            print(f"Erreur: Le fichier PDF n'a pas été trouvé à l'emplacement {PDF_PATH}")

        # Connexion au serveur et envoi
        server = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"Email envoyé avec succès à {customer_email}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")
        return False
