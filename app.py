import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="Iterable Demo Copilot", layout="wide")
st.title("Iterable Demo Copilot")

# --- Persona Selector ---
persona_list = ["GlowSkin", "PulseFit", "JetQuest", "LeadSync"]
persona = st.sidebar.selectbox("Choose a Persona:", persona_list)

# --- Mermaid.js Journey Maps ---
journey_flows = {
    "GlowSkin": """
        flowchart TD
            Start([User Adds Items to Cart])
            Wait1[Wait 2 Hours]
            Decision1{Has User Purchased?}
            SMS[Send SMS: \\\"You left something behind\\\"]
            Wait2[Wait 4 Hours]
            Decision2{Has User Purchased?}
            Email[Send Email: \\\"Still want that glow? Here's 10% off\\\"]
            Wait3[Wait 2 Days]
            Decision3{Has User Purchased?}
            Push[Send Push: \\\"Your GlowKit is still waiting\\\"]
            ExitSuccess([Exit: Purchase Completed])
            ExitFail([Exit: No Response After 3 Touches])

            Start --> Wait1 --> Decision1
            Decision1 -- \"Yes\" --> ExitSuccess
            Decision1 -- \"No\" --> SMS --> Wait2 --> Decision2
            Decision2 -- \"Yes\" --> ExitSuccess
            Decision2 -- \"No\" --> Email --> Wait3 --> Decision3
            Decision3 -- \"Yes\" --> ExitSuccess
            Decision3 -- \"No\" --> Push --> ExitFail
    """,
    "PulseFit": """
        flowchart TD
            Start([User Signs Up for App])
            Wait1[Wait 72 Hours]
            Decision1{Has User Opened the App?}
            Push[Send Push: \\\"Start Day 1 Workout\\\"]
            Wait2[Wait 24 Hours]
            Decision2{Has User Opened the App?}
            Email[Send Email: \\\"How to Get Started + Welcome Video\\\"]
            Wait3[Wait 3 Days]
            Decision3{Still Inactive?}
            SMS[Send SMS: \\\"25% off your first month\\\"]
            ExitActive([Exit: User Engaged with App])
            ExitInactive([Exit: No Activity After Journey])

            Start --> Wait1 --> Decision1
            Decision1 -- \"Yes\" --> ExitActive
            Decision1 -- \"No\" --> Push --> Wait2 --> Decision2
            Decision2 -- \"Yes\" --> ExitActive
            Decision2 -- \"No\" --> Email --> Wait3 --> Decision3
            Decision3 -- \"No\" --> SMS --> ExitInactive
            Decision3 -- \"Yes\" --> ExitActive
    """,
    "JetQuest": """
        flowchart TD
            Start([User Browses Flight but Doesn't Book])
            Wait1[Wait 24 Hours]
            Decision1{Has User Booked Trip?}
            Email[Send Email: \\\"Still dreaming of Hawaii? Here's 10% Off\\\"]
            Wait2[Wait 2 Days]
            Decision2{Has User Booked?}
            SMS[Send SMS: \\\"Your dream trip is still available\\\"]
            Retarget[Launch Retargeting Ads]
            Wait3[Wait 3 Days]
            Decision3{Still No Booking?}
            ExitBook([Exit: Trip Booked])
            ExitNoBook([Exit: No Response After Ads])

            Start --> Wait1 --> Decision1
            Decision1 -- \"Yes\" --> ExitBook
            Decision1 -- \"No\" --> Email --> Wait2 --> Decision2
            Decision2 -- \"Yes\" --> ExitBook
            Decision2 -- \"No\" --> SMS --> Retarget --> Wait3 --> Decision3
            Decision3 -- \"Yes\" --> ExitBook
            Decision3 -- \"No\" --> ExitNoBook
    """,
    "LeadSync": """
        flowchart TD
            Start([User Starts Free Trial])
            Wait1[Wait 3 Days]
            Decision1{Has User Used Core Feature?}
            Email[Send Email: \\\"Try Auto-Enrich Today\\\"]
            Wait2[Wait 2 Days]
            Decision2{Feature Used?}
            InApp[Trigger In-App: \\\"Walkthrough\\\"]
            Wait3[Wait 2 Days]
            Decision3{Still Not Used?}
            CSM[Alert Sales Team to Follow Up]
            ExitUsed([Exit: Feature Engaged])
            ExitUnconverted([Exit: Trial Ends Inactive])

            Start --> Wait1 --> Decision1
            Decision1 -- \"Yes\" --> ExitUsed
            Decision1 -- \"No\" --> Email --> Wait2 --> Decision2
            Decision2 -- \"Yes\" --> ExitUsed
            Decision2 -- \"No\" --> InApp --> Wait3 --> Decision3
            Decision3 -- \"Yes\" --> ExitUsed
            Decision3 -- \"No\" --> CSM --> ExitUnconverted
    """
}

# --- Render Diagram ---
st.subheader(f"Customer Journey: {persona}")
components.html(
    f"""
    <div class="mermaid">
    {journey_flows[persona]}
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
    """,
    height=600,
    scrolling=True
)

# --- Summary Card ---
summaries = {
    "GlowSkin": "Recover abandoned carts using SMS, Email, and Push with incentives to drive conversion.",
    "PulseFit": "Re-engage inactive app signups using push, educational email, and promo SMS.",
    "JetQuest": "Follow up with browsing users using email, SMS, and retargeting to drive bookings.",
    "LeadSync": "Activate trial users with email nudges, in-app guidance, and CSM alerts."
}

st.markdown(f"**Use Case Summary:** {summaries[persona]}")
