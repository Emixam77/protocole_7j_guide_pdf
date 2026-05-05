from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from .agents import AgentSourcing, AgentCommunity, AgentAdsIntel
from .database import get_supabase
from .mailer import send_delivery_email
import os
import stripe

app = FastAPI(title="Protocole 7 Jours API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class SourcingRequest(BaseModel):
    user_id: str
    niche: str
    city: str

@app.get("/")
async def root():
    return {"message": "Protocole 7 Jours Backend Active"}

@app.post("/scan/leads")
async def scan_leads(req: SourcingRequest):
    agent = AgentSourcing(niche=req.niche, city=req.city)
    leads = agent.scan_google_maps()
    agent.inject_leads(leads, req.user_id)
    return {"status": "success", "leads": leads, "leads_count": len(leads)}

class PitchRequest(BaseModel):
    company_name: str
    gap: str

@app.post("/commando/pitch")
async def get_pitch(req: PitchRequest):
    agent = AgentAdsIntel()
    pitch = agent.generate_pitch(req.company_name, req.gap)
    return {"pitch": pitch}

@app.get("/intelligence/ads")
async def get_ads_intel():
    agent = AgentAdsIntel()
    return agent.analyze_competitors()

@app.get("/radar/signals")
async def get_radar_signals():
    agent = AgentCommunity()
    return agent.detect_distress()

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Extraction ultra-sécurisée de l'email (méthode getattr en cascade)
        customer_details = getattr(session, 'customer_details', None)
        customer_email = getattr(customer_details, 'email', None) if customer_details else None
        
        if customer_email:
            print(f"Paiement réussi pour {customer_email}. Envoi du guide...")
            send_delivery_email(customer_email)

    return {"status": "success"}

# Servir le frontend en dernier recours (pour éviter de bloquer les routes API)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

