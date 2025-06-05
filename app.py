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
    "GlowSkin": '''graph TD
    A[User Adds Items to Cart] --> B[Wait 2 Hours]
    B --> C{Has User Purchased?}
    C -->|Yes| D[Exit: Purchase Completed]
    C -->|No| E[Send SMS: You left something behind]
    E --> F[Wait 4 Hours]
    F --> G{Has User Purchased?}
    G -->|Yes| D
    G -->|No| H[Send Email: Still want that glow? 10% off]
    H --> I[Wait 2 Days]
    I --> J{Has User Purchased?}
    J -->|Yes| D
    J -->|No| K[Send Push: Your GlowKit is waiting]
    K --> L[Exit: No Response After 3 Touches]''',
    
    "PulseFit": '''graph TD
    A[User Signs Up for App] --> B[Wait 24 Hours]
    B --> C{User Active in App?}
    C -->|Yes| D[Exit: User Engaged]
    C -->|No| E[Send Push: Ready to crush your fitness goals?]
    E --> F[Wait 3 Days]
    F --> G{User Active in App?}
    G -->|Yes| D
    G -->|No| H[Send Email: 5 Quick Workouts to Get Started]
    H --> I[Wait 1 Week]
    I --> J{User Active in App?}
    J -->|Yes| D
    J -->|No| K[Send SMS: Get 30% off premium]
    K --> L[Exit: User Remains Inactive]''',
    
    "JetQuest": '''graph TD
    A[User Browses Flight Deals] --> B[Wait 1 Hour]
    B --> C{User Booked Flight?}
    C -->|Yes| D[Exit: Booking Completed]
    C -->|No| E[Send Email: Your flight deal expires soon]
    E --> F[Wait 6 Hours]
    F --> G{User Booked Flight?}
    G -->|Yes| D
    G -->|No| H[Send SMS: Last chance - save $200]
    H --> I[Wait 1 Day]
    I --> J{User Booked Flight?}
    J -->|Yes| D
    J -->|No| K[Send Retargeting Ad: Similar destinations]
    K --> L[Exit: Deal Expired]''',
    
    "LeadSync": '''graph TD
    A[User Starts Free Trial] --> B[Wait 2 Days]
    B --> C{User Setup Complete?}
    C -->|Yes| D[Exit: Trial Converted]
    C -->|No| E[Send Email: Complete your setup in 5 minutes]
    E --> F[Wait 3 Days]
    F --> G{User Active in Trial?}
    G -->|Yes| D
    G -->|No| H[Send In-App: Need help? Quick guide]
    H --> I[Wait 1 Week]
    I --> J{User Engaged?}
    J -->|Yes| D
    J -->|No| K[Alert CSM: High-value prospect needs attention]
    K --> L[Exit: Trial Expired]'''
}

# --- Mermaid Renderer ---
st.subheader(f"Customer Journey: {persona}")

# Create HTML with Mermaid diagram
mermaid_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/mermaid@9.4.3/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
        }}
        .mermaid {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{journey_flows[persona]}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
</body>
</html>
"""

components.html(mermaid_html, height=700, scrolling=True)

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
        try:
            # Updated OpenAI client initialization
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            prompt = f"""
You are a senior marketing strategist. Based on the customer journey below for the persona '{persona}', suggest improvements for engagement, timing, or conversion. Include subject lines, SMS copy, push notification ideas, and any relevant A/B testing strategies.

Journey Summary:
{summaries.get(persona, '')}

Be concise and strategic. Break your response into clearly labeled sections.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior marketing strategist specializing in customer engagement and MarTech."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            suggestions = response.choices[0].message.content
            st.markdown("### AI Campaign Suggestions")
            st.markdown(suggestions)
            
        except Exception as e:
            st.error(f"Error generating AI suggestions: {str(e)}")
            st.info("Please check your OpenAI API key configuration in Streamlit secrets.")
