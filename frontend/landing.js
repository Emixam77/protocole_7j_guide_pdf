document.addEventListener('DOMContentLoaded', () => {
    // 1. Scroll Reveal Logic (Intersection Observer)
    const sections = document.querySelectorAll('section');
    const observerOptions = {
        threshold: 0.1
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

    // 2. Floating CTA Logic
    const floatingCta = document.getElementById('floating-cta');
    const heroSection = document.querySelector('.hero');

    window.addEventListener('scroll', () => {
        const heroBottom = heroSection.getBoundingClientRect().bottom;
        if (heroBottom < 0) {
            floatingCta.classList.add('visible');
        } else {
            floatingCta.classList.remove('visible');
        }
    });

    // 3. Interactive Plan (Graphcet) - Updated Teasers
    const teaserBox = document.getElementById('teaser-content');
    const dayCards = document.querySelectorAll('.day-card');
    const teasers = {
        1: "JOUR 1 : INFILTRATION. Scanner votre zone et identifier les 10 cibles avec le plus gros 'Gap' de valeur.",
        2: "JOUR 2 : SOURCING IA. Utiliser l'intelligence Nexus pour extraire les failles techniques des concurrents.",
        3: "JOUR 3 : L'AUDIT INVISIBLE. Créer une preuve de concept en 5 minutes qui rend votre offre irrésistible.",
        4: "JOUR 4 : LA PROPOSITION COMMANDO. Structurer votre prix pour que le 'Non' ne soit pas une option.",
        5: "JOUR 5 : CLOSING PSYCHOLOGIQUE. La technique de la 'Double Contrainte' pour valider le contrat en un appel.",
        6: "JOUR 6 : MAÎTRISE DE LA LUMIÈRE. Optimiser votre setup pour garantir un résultat premium en un minimum de temps.",
        7: "JOUR 7 : SIGNATURE & RÉPÉTITION. Célébrer et relancer la machine pour la semaine suivante."
    };

    dayCards.forEach(card => {
        card.addEventListener('click', () => {
            dayCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            const day = card.getAttribute('data-day');
            teaserBox.innerText = teasers[day];
        });
    });

    // 4. Glitch Randomization (Optional: adds variety to the CSS animation)
    const glitches = document.querySelectorAll('.glitch');
    setInterval(() => {
        const randomGlitch = glitches[Math.floor(Math.random() * glitches.length)];
        randomGlitch.style.setProperty('--glitch-translate', `${(Math.random() - 0.5) * 10}px`);
    }, 200);

    // 5. Form Submission Simulation
    const contactForm = document.getElementById('contact-form');
    const payBtn = document.getElementById('pay-btn');
    const licensesCount = document.querySelector('.licenses-count');

    // Simulation de décompte d'urgence
    if (licensesCount) {
        setTimeout(() => {
            licensesCount.innerText = "13";
            licensesCount.style.transform = "scale(1.2)";
            setTimeout(() => licensesCount.style.transform = "scale(1)", 200);
        }, 5000);
    }

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('contact-email').value;
        
        payBtn.innerText = "INITIALISATION PAIEMENT...";
        payBtn.disabled = true;

        // On redirige vers Stripe avec l'email pré-rempli (LIEN DE TEST)
        const stripeUrl = `https://buy.stripe.com/test_8x214m3Ku0Gq5Li7sM18c01?prefilled_email=${encodeURIComponent(email)}`;
        
        setTimeout(() => {
            window.location.href = stripeUrl;
        }, 800);
    });
});
