import streamlit as st
import streamlit.components.v1 as components
import openai

# --- Page Configuration ---
st.set_page_config(page_title="Iterable Demo Copilot", layout="wide")
st.title("Iterable Demo Copilot")

# --- Persona Selector ---
persona_list = ["GlowSkin", "PulseFit", "JetQuest", "LeadSync"]
persona = st.sidebar.selectbox("Choose a Persona:", persona_list)

# --- Mermaid.js Journey Maps ---
journey_flows = {
    "GlowSkin": '''
        flowchart TD
            Start([User Adds Items to Cart])
            Wait1[Wait 2 Hours]
            Decision1{Has User Purchased?}
            SMS[Send SMS: "You left something behind"]
            Wait2[Wait 4 Hours]
            Decision2{Has User Purchased?}
            Email[Send Email: "Still want that glow? Here's 10% off"]
            Wait3[Wait 2 Days]
            Decision3{Has User Purchased?}
            Push[Send Push: "Your GlowKit is still waiting"]
            ExitSuccess([Exit: Purchase Completed])
            ExitFail([Exit: No Response After 3 Touches])
            Start --> Wait1 --> Decision1
            Decision1 -- Yes --> ExitSuccess
            Decision1 -- No --> SMS --> Wait2 --> Decision2
            Decision2 -- Yes --> ExitSuccess
            Decision2 -- No --> Email --> Wait3 --> Decision3
            Decision3 -- Yes --> ExitSuccess
            Decision3 -- No --> Push --> ExitFail
    '''
}

# --- Mermaid Renderer (Using v10.4.0 for compatibility) ---
st.subheader(f"Customer Journey: {persona}")
components.html(
    f"""
    <div class="mermaid">
    {journey_flows[persona]}
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.esm.min.mjs';
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

st.markdown(f"**Use Case Summary:** {summaries.get(persona, 'N/A')}")

# --- GPT Integration: AI Suggestions ---
if st.button("Ask AI for Campaign Suggestions"):
    with st.spinner("Generating AI suggestions..."):
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        prompt = f"""
You are a senior marketing strategist. Based on the customer journey below for the persona '{persona}', suggest improvements for engagement, timing, or conversion. Include subject lines, SMS copy, push notification ideas, and any relevant A/B testing strategies.

Journey Summary:
{summaries.get(persona, '')}

Be concise and strategic. Break your response into clearly labeled sections.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior marketing strategist specializing in customer engagement and MarTech."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        suggestions = response["choices"][0]["message"]["content"]
        st.markdown("### AI Campaign Suggestions")
        st.markdown(suggestions)
