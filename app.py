import streamlit as st
import streamlit.components.v1 as components
import openai
import re

# --- Page Configuration ---
st.set_page_config(page_title="Iterable Demo Copilot", layout="wide")
st.title("Iterable Demo Copilot")

# --- Onboarding Guide ---
with st.expander("📘 How to Use This Demo", expanded=True):
    st.markdown("""
**Welcome to the Iterable Demo Copilot.**  
This tool simulates how a Solutions Consultant at Iterable might demonstrate customer journeys and real-time campaign recommendations using AI.

### How to use this app:
1. **Select a persona** from the sidebar. Each persona represents a fictional customer scenario.
2. **Choose an event** to simulate user behavior (e.g., cart abandonment).
3. Click **'Add Event to Timeline'** to build up a sequence of events.
4. View the **journey diagram**, which highlights key touchpoints and stages.
5. Click **'Ask AI for Campaign Suggestions'** to receive campaign recommendations.
6. Click **'Ask AI for Journey Optimization'** to get strategic journey improvements.
7. The recommended nodes will be **highlighted in yellow**.

You can reset the timeline at any time, or experiment with different personas and user behaviors.
    """)

# --- Persona Selector ---
persona_list = ["GlowSkin", "PulseFit", "JetQuest", "LeadSync"]

# Reset everything when persona changes
if "current_persona" not in st.session_state:
    st.session_state.current_persona = persona_list[0]

persona = st.sidebar.selectbox("Choose a Persona:", persona_list)

# Check if persona changed and reset if so
if persona != st.session_state.current_persona:
    st.session_state.current_persona = persona
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.campaign_suggestion = ""
    st.session_state.journey_optimization = ""
    st.rerun()

# --- Event Selector ---
event_options = {
    "GlowSkin": [
        "Cart Abandoned", "Email Opened", "Email Unopened", "Push Notification Ignored", 
        "SMS Received", "Product Review Left", "Wishlist Item Added", "Discount Code Used",
        "Social Media Shared", "Return Customer", "Subscription Started", "Unsubscribed"
    ],
    "PulseFit": [
        "User Inactive", "Push Notification Sent", "Email Unopened", "Workout Completed",
        "App Opened", "Premium Upgrade", "Goal Achievement", "Friend Invited", 
        "Progress Photo Shared", "Subscription Cancelled", "Support Contact", "Tutorial Skipped"
    ],
    "JetQuest": [
        "Flight Searched", "Booking Abandoned", "Email Opened", "SMS Clicked", 
        "Price Alert Set", "Loyalty Points Earned", "Review Left", "Newsletter Subscribed",
        "Mobile App Downloaded", "Customer Service Contact", "Refund Requested", "Rebooking Attempt"
    ],
    "LeadSync": [
        "Trial Started", "Demo Requested", "Email Unopened", "Feature Explored",
        "Integration Attempted", "Onboarding Completed", "Team Member Invited", "Billing Info Added",
        "Support Ticket Created", "Webinar Attended", "Case Study Downloaded", "Contract Signed"
    ]
}
selected_event = st.selectbox("Simulate User Event:", event_options.get(persona, []))

# --- Timeline Tracking ---
if "event_timeline" not in st.session_state:
    st.session_state.event_timeline = []
if "next_node_id" not in st.session_state:
    st.session_state.next_node_id = ""
if "campaign_suggestion" not in st.session_state:
    st.session_state.campaign_suggestion = ""
if "journey_optimization" not in st.session_state:
    st.session_state.journey_optimization = ""

if st.button("Add Event to Timeline"):
    if selected_event not in st.session_state.event_timeline:
        st.session_state.event_timeline.append(selected_event)

if st.button("Reset Timeline"):
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.campaign_suggestion = ""
    st.session_state.journey_optimization = ""

if st.session_state.event_timeline:
    st.markdown("### Simulated Event Timeline")
    st.write(" → ".join(st.session_state.event_timeline))
else:
    st.markdown("_No events in timeline yet._")

# --- Event Highlight Mapping ---
event_to_node_map = {
    "GlowSkin": {
        "Cart Abandoned": "E", "Email Opened": "H", "Email Unopened": "H", "Push Notification Ignored": "K",
        "SMS Received": "E", "Product Review Left": "D", "Wishlist Item Added": "A", "Discount Code Used": "D",
        "Social Media Shared": "D", "Return Customer": "A", "Subscription Started": "D", "Unsubscribed": "L"
    },
    "PulseFit": {
        "User Inactive": "E", "Push Notification Sent": "E", "Email Unopened": "H", "Workout Completed": "D",
        "App Opened": "A", "Premium Upgrade": "D", "Goal Achievement": "D", "Friend Invited": "D",
        "Progress Photo Shared": "D", "Subscription Cancelled": "L", "Support Contact": "H", "Tutorial Skipped": "E"
    },
    "JetQuest": {
        "Flight Searched": "A", "Booking Abandoned": "E", "Email Opened": "E", "SMS Clicked": "H",
        "Price Alert Set": "A", "Loyalty Points Earned": "D", "Review Left": "D", "Newsletter Subscribed": "H",
        "Mobile App Downloaded": "A", "Customer Service Contact": "H", "Refund Requested": "K", "Rebooking Attempt": "E"
    },
    "LeadSync": {
        "Trial Started": "A", "Demo Requested": "A", "Email Unopened": "E", "Feature Explored": "A",
        "Integration Attempted": "H", "Onboarding Completed": "D", "Team Member Invited": "D", "Billing Info Added": "D",
        "Support Ticket Created": "H", "Webinar Attended": "H", "Case Study Downloaded": "E", "Contract Signed": "D"
    }
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/mermaid@9.4.3/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #ffffff; }}
        .mermaid {{ text-align: center; }}
    </style>
</head>
<body>
    <div class="mermaid">
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

st.markdown("### What You're Seeing")
st.info("""
The diagram above is a dynamic visualization of the current customer journey for your selected persona.  
Highlighted nodes represent:
- Events you've simulated  
- Or AI-recommended next steps based on past behavior

Use the AI suggestions to understand optimal engagement points in the journey.
""")

# --- Event Status Display ---
if highlight_node:
    st.info(f"🎯 **Event Simulation:** {selected_event} - Highlighted in journey diagram")

# --- AI Suggestion Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🤖 Ask AI for Campaign Suggestions", use_container_width=True):
        with st.spinner("Generating campaign suggestions..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                timeline = st.session_state.event_timeline
                event_history = ", ".join(timeline) if timeline else "No events simulated."

                prompt = f"""
You are a senior marketing strategist at Iterable. Based on the customer journey for persona '{persona}', and the following event timeline:
{event_history}

Available journey steps for {persona}:
- Send SMS (early intervention)
- Send Email with discount offer (mid-journey)  
- Send Push notification (final attempt)
- Wait and monitor behavior
- Exit/end journey

Suggest the next best campaign action. Provide:
1. The **recommended action** (e.g. "Send Email with 10% discount")
2. A **brief explanation** (why this is the right step strategically)
3. **Expected outcome** (what you expect to happen)

Format your response clearly with headers.
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

                st.session_state.campaign_suggestion = response.choices[0].message.content
                st.rerun()

            except Exception as e:
                st.error(f"Error generating campaign suggestions: {str(e)}")
                st.info("Please check your OpenAI API key configuration in Streamlit secrets.")

with col2:
    if st.button("🚀 Ask AI for Journey Optimization", use_container_width=True):
        with st.spinner("Analyzing journey optimization..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                timeline = st.session_state.event_timeline
                event_history = ", ".join(timeline) if timeline else "No events simulated."

                prompt = f"""
You are a customer journey optimization expert at Iterable. Analyze the current journey for persona '{persona}' and event timeline:
{event_history}

Provide strategic recommendations for:
1. **Journey Improvements** - How to optimize the current flow
2. **Timing Adjustments** - Better wait times or triggers
3. **Personalization Opportunities** - Ways to make it more relevant
4. **Performance Metrics** - Key KPIs to track

Focus on practical, actionable insights that would improve conversion rates and customer experience.
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a customer journey optimization expert specializing in lifecycle marketing and conversion optimization."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )

                st.session_state.journey_optimization = response.choices[0].message.content
                st.rerun()

            except Exception as e:
                st.error(f"Error generating journey optimization: {str(e)}")
                st.info("Please check your OpenAI API key configuration in Streamlit secrets.")

# --- Display AI Responses ---
if st.session_state.campaign_suggestion:
    st.success("💡 **Campaign Suggestion:**")
    st.markdown(st.session_state.campaign_suggestion)

if st.session_state.journey_optimization:
    st.success("🚀 **Journey Optimization:**")
    st.markdown(st.session_state.journey_optimization)
