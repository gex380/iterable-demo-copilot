import streamlit as st
import streamlit.components.v1 as components
import openai
import re

# --- Page Configuration ---
st.set_page_config(page_title="Iterable Demo Copilot", layout="wide")
st.title("Iterable Demo Copilot")

# --- Persona Selector ---
persona_list = ["GlowSkin", "PulseFit", "JetQuest", "LeadSync"]
persona = st.sidebar.selectbox("Choose a Persona:", persona_list)

# --- Event Selector ---
event_options = {
    "GlowSkin": ["Cart Abandoned", "Email Opened", "Push Ignored"],
    "PulseFit": ["User Inactive", "Push Sent", "Email Unopened"],
    "JetQuest": ["Browsed Flight", "No Booking", "Retargeting Ad"],
    "LeadSync": ["Trial Started", "No Setup", "No Engagement"]
}
selected_event = st.selectbox("Simulate User Event:", event_options.get(persona, []))

# --- Timeline Tracking ---
if "event_timeline" not in st.session_state:
    st.session_state.event_timeline = []
if "next_node_id" not in st.session_state:
    st.session_state.next_node_id = ""
if "next_node_reason" not in st.session_state:
    st.session_state.next_node_reason = ""

if st.button("Add Event to Timeline"):
    if selected_event not in st.session_state.event_timeline:
        st.session_state.event_timeline.append(selected_event)

if st.button("Reset Timeline"):
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.next_node_reason = ""

if st.session_state.event_timeline:
    st.markdown("### Simulated Event Timeline")
    st.write(" → ".join(st.session_state.event_timeline))
else:
    st.markdown("_No events in timeline yet._")

# --- Event Highlight Mapping ---
event_to_node_map = {
    "GlowSkin": {"Cart Abandoned": "E", "Email Opened": "H", "Push Ignored": "K"},
    "PulseFit": {"User Inactive": "E", "Push Sent": "E", "Email Unopened": "H"},
    "JetQuest": {"Browsed Flight": "A", "No Booking": "F", "Retargeting Ad": "K"},
    "LeadSync": {"Trial Started": "A", "No Setup": "E", "No Engagement": "H"}
}

highlight_node = st.session_state.next_node_id or event_to_node_map.get(persona, {}).get(selected_event, "")
highlight_class = "classDef highlight fill:#ffcc00;"
highlight_command = f"class {highlight_node} highlight;" if highlight_node else ""

# --- Journey Definitions with Highlight Support ---
def get_journey_flow(persona_name, highlight_class_def, highlight_command_def):
    flows = {
        "GlowSkin": f'''graph TD
    A[User Adds Items to Cart] --> B[Wait 2 Hours]
    B --> C{{Has User Purchased?}}
    C -->|Yes| D[Exit: Purchase Completed]
    C -->|No| E[Send SMS: You left something behind]
    E --> F[Wait 4 Hours]
    F --> G{{Has User Purchased?}}
    G -->|Yes| D
    G -->|No| H[Send Email: Still want that glow? 10% off]
    H --> I[Wait 2 Days]
    I --> J{{Has User Purchased?}}
    J -->|Yes| D
    J -->|No| K[Send Push: Your GlowKit is waiting]
    K --> L[Exit: No Response After 3 Touches]
    {highlight_class_def}
    {highlight_command_def}
    ''',
        "PulseFit": f'''graph TD
    A[User Signs Up for App] --> B[Wait 24 Hours]
    B --> C{{User Active in App?}}
    C -->|Yes| D[Exit: User Engaged]
    C -->|No| E[Send Push: Ready to crush your fitness goals?]
    E --> F[Wait 3 Days]
    F --> G{{User Active in App?}}
    G -->|Yes| D
    G -->|No| H[Send Email: 5 Quick Workouts to Get Started]
    H --> I[Wait 1 Week]
    I --> J{{User Active in App?}}
    J -->|Yes| D
    J -->|No| K[Send SMS: Get 30% off premium]
    K --> L[Exit: User Remains Inactive]
    {highlight_class_def}
    {highlight_command_def}
    ''',
        "JetQuest": f'''graph TD
    A[User Browses Flight Deals] --> B[Wait 1 Hour]
    B --> C{{User Booked Flight?}}
    C -->|Yes| D[Exit: Booking Completed]
    C -->|No| E[Send Email: Your flight deal expires soon]
    E --> F[Wait 6 Hours]
    F --> G{{User Booked Flight?}}
    G -->|Yes| D
    G -->|No| H[Send SMS: Last chance - save $200]
    H --> I[Wait 1 Day]
    I --> J{{User Booked Flight?}}
    J -->|Yes| D
    J -->|No| K[Send Retargeting Ad: Similar destinations]
    K --> L[Exit: Deal Expired]
    {highlight_class_def}
    {highlight_command_def}
    ''',
        "LeadSync": f'''graph TD
    A[User Starts Free Trial] --> B[Wait 2 Days]
    B --> C{{User Setup Complete?}}
    C -->|Yes| D[Exit: Trial Converted]
    C -->|No| E[Send Email: Complete your setup in 5 minutes]
    E --> F[Wait 3 Days]
    F --> G{{User Active in Trial?}}
    G -->|Yes| D
    G -->|No| H[Send In-App: Need help? Quick guide]
    H --> I[Wait 1 Week]
    I --> J{{User Engaged?}}
    J -->|Yes| D
    J -->|No| K[Alert CSM: High-value prospect needs attention]
    K --> L[Exit: Trial Expired]
    {highlight_class_def}
    {highlight_command_def}
    '''
    }
    return flows.get(persona_name, "")

# --- Mermaid Renderer ---
st.subheader(f"Customer Journey: {persona}")
current_flow = get_journey_flow(persona, highlight_class, highlight_command)

mermaid_html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <script src=\"https://unpkg.com/mermaid@9.4.3/dist/mermaid.min.js\"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #ffffff; }}
        .mermaid {{ text-align: center; }}
    </style>
</head>
<body>
    <div class=\"mermaid\">
{current_flow}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }}
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

# --- Event Status Display ---
if highlight_node:
    st.info(f"🎯 **Event Simulation:** {selected_event} - Highlighting node {highlight_node} in the journey")
if st.session_state.next_node_id:
    st.success(f"💡 **AI Recommendation:** Highlighting node {st.session_state.next_node_id} as the next step")
    st.markdown(f"**Reasoning:** {st.session_state.next_node_reason}")

# --- GPT Integration: AI Suggestions ---
if st.button("Ask AI for Campaign Suggestions"):
    with st.spinner("Generating AI suggestions..."):
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            timeline = st.session_state.event_timeline
            event_history = ", ".join(timeline) if timeline else "No events simulated."

            prompt = f"""
You are a senior marketing strategist. Based on the customer journey for persona '{persona}', and the following event timeline:
{event_history}

Suggest the next best step in the journey. Provide:
1. The **node ID** (e.g. H)
2. The **action/label** (e.g. Send Email: Offer 10% off)
3. A **brief explanation** (why this is the right step)

Format:
Node: <ID>
Action: <Label>
Reason: <Short explanation>
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

            # Extract recommended node from GPT response
            match_node = re.search(r"Node:\s*(\\w+)", suggestions)
            match_reason = re.search(r"Reason:\s*(.*)", suggestions)

            if match_node:
                st.session_state.next_node_id = match_node.group(1)
            if match_reason:
                st.session_state.next_node_reason = match_reason.group(1)

            st.markdown("### AI Campaign Suggestion Response")
            st.markdown(suggestions)

        except Exception as e:
            st.error(f"Error generating AI suggestions: {str(e)}")
            st.info("Please check your OpenAI API key configuration in Streamlit secrets.")
