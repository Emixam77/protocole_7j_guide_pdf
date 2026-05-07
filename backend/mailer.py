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

def send_delivery_email(customer_email: str, password: str = None):
    """
    Envoie le guide PDF au client après un achat réussi et lui fournit ses accès.
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

        # Message incluant les accès et la mention de l'application interactive
        body = f"""
Bonjour,

Merci pour votre confiance ! 

Vous trouverez ci-joint votre guide complet "Protocole 7 Jours" (en PDF). 

L'application interactive qui l'accompagne va grandement vous faciliter la tâche dans la recherche et l'analyse de vos prospects.

Voici vos accès pour vous connecter à votre interface :
Lien d'accès : https://protocole-7.onrender.com/
Email : {customer_email}
Mot de passe : {password if password else "Non généré (veuillez contacter le support)"}

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

def send_j7_upsell_email(customer_email: str):
    """
    Envoie l'email de relance à J+7 pour demander un témoignage et proposer un upsell.
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print("Erreur: Paramètres SMTP manquants dans le .env")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = customer_email
        msg['Subject'] = "Bilan Protocole 7 Jours 🎯 + La suite logique"

        body = f"""Bonjour,

Cela fait exactement 7 jours que vous avez débloqué le "Protocole 7 Jours". 

Si vous avez suivi le plan d'action, vous devriez déjà avoir identifié vos cibles, envoyé vos premiers pitchs, et potentiellement sécurisé vos premiers rendez-vous.
J'adorerais avoir votre retour : comment s'est passée cette semaine commando ? Répondez simplement à cet email pour me partager vos victoires (je suis toujours preneur de témoignages !).

Vous avez rencontré des difficultés ?
C'est normal. Parfois, le plus dur n'est pas la théorie, mais l'adaptation à la réalité du terrain (bloquer sur l'appel de closing, ne pas savoir quoi répondre à une objection, etc.).

Si vous sentez que vous avez besoin d'un regard expert sur votre situation spécifique, je propose des sessions d'accompagnement privé (en visio ou en présentiel). L'objectif : analyser ce qui bloque dans votre processus et le débloquer ensemble.

Vous pouvez me contacter directement ici :
https://chat.whatsapp.com/KJl2515p6hQC6NNMeskucF

À très vite,
Maxime
"""
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"Email J+7 envoyé avec succès à {customer_email}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email J+7 : {str(e)}")
        return False
