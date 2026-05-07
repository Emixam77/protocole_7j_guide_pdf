from datetime import datetime, timedelta, timezone
from ..database import get_supabase
from ..mailer import send_j7_upsell_email

def process_j7_emails():
    """
    Vérifie les achats effectués il y a plus de 7 jours et envoie l'email de relance
    si ce n'est pas déjà fait.
    """
    print("🤖 Agent Mail Tracker : Démarrage du scan J+7...")
    
    try:
        supabase = get_supabase()
        
        # Calcul de la date limite : il y a exactement 7 jours
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        # Requête : récupérer les emails non envoyés dont la date d'achat est <= il y a 7 jours
        response = supabase.table('mail_tracker').select('*').eq('j7_email_sent', False).lte('purchased_at', seven_days_ago.isoformat()).execute()
        
        records = response.data
        if not records:
            print("🤖 Agent Mail Tracker : Aucune relance J+7 à envoyer.")
            return

        print(f"🤖 Agent Mail Tracker : {len(records)} relance(s) à effectuer.")

        for record in records:
            email = record['email']
            record_id = record['id']
            
            print(f"Envoi de la relance J+7 à {email}...")
            success = send_j7_upsell_email(email)
            
            if success:
                # Marquer comme envoyé
                supabase.table('mail_tracker').update({'j7_email_sent': True}).eq('id', record_id).execute()
                print(f"✅ Statut mis à jour pour {email}.")
            else:
                print(f"❌ Échec de l'envoi pour {email}.")
                
    except Exception as e:
        print(f"🤖 Agent Mail Tracker : Erreur lors du scan - {str(e)}")

if __name__ == "__main__":
    process_j7_emails()
