import streamlit as st
import streamlit.components.v1 as components
import openai
import re
import math

# --- Page Configuration ---
st.set_page_config(page_title="Iterable Demo Copilot", layout="wide")
st.title("Iterable Demo Copilot")

# --- Onboarding Guide ---
with st.expander("How to Use This Demo", expanded=True):
    st.markdown("""
    **Welcome to the Iterable Demo Copilot.**  
    This tool demonstrates how Iterable transforms disconnected marketing tools into a unified growth engine.

    ### Key Features:
    1. **Select a persona** from the sidebar - each represents a real customer scenario
    2. **Simulate user events** to build behavioral timelines
    3. **Visualize customer journeys** with dynamic flow diagrams
    4. **Get AI-powered recommendations** tailored to specific customer behavior
    5. **Explore A/B testing strategies** with statistical rigor
    6. **See Iterable's ROI impact** on your existing MarTech stack

    ### What makes this demo powerful:
    
    This interactive demo showcases Iterable's core strength: transforming disconnected marketing tools into an intelligent, unified growth engine. Select different customer personas, simulate realistic behavioral events, and watch as the platform coordinates personalized responses across email, SMS, and push notifications in real-time. 
    
    The demo combines visual journey orchestration with AI-powered recommendations, competitive positioning against major platforms like Braze and Klaviyo, and quantified ROI calculations based on your specific MarTech stack. Every feature demonstrates how Iterable eliminates data silos, automates complex workflows, and delivers measurable business impact - turning your collection of marketing tools into a coordinated customer experience that drives conversion and retention.
    """)

# --- Initialize Session State ---
def initialize_session_state():
    """Initialize all session state variables if they don't exist"""
    default_values = {
        'current_persona': 'GlowSkin',
        'event_timeline': [],
        'next_node_id': '',
        'event_suggestion': '',
        'journey_optimization': '',
        'business_impact': ''
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# --- Persona Selector ---
persona_list = ["GlowSkin", "PulseFit", "JetQuest", "LeadSync"]

persona = st.sidebar.selectbox("Choose a Persona:", persona_list, 
                              index=persona_list.index(st.session_state.current_persona) if st.session_state.current_persona in persona_list else 0)

# Check if persona changed and reset if so
if persona != st.session_state.current_persona:
    st.session_state.current_persona = persona
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.event_suggestion = ""
    st.session_state.journey_optimization = ""
    st.session_state.business_impact = ""
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

# --- Timeline Management ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Add Event to Timeline"):
        if selected_event and selected_event not in st.session_state.event_timeline:
            st.session_state.event_timeline.append(selected_event)
            st.rerun()

with col2:
    if st.button("Reset Timeline"):
        st.session_state.event_timeline = []
        st.session_state.next_node_id = ""
        st.session_state.event_suggestion = ""
        st.session_state.journey_optimization = ""
        st.session_state.business_impact = ""
        st.rerun()

# Display current timeline
if st.session_state.event_timeline:
    st.markdown("### Simulated Event Timeline")
    st.write(" → ".join(st.session_state.event_timeline))
else:
    st.markdown("_No events in timeline yet._")

# --- Event Highlight Mapping (Maps events to logical NEXT action based on journey flows) ---
event_to_node_map = {
    "GlowSkin": {
        # Cart abandonment journey: A→E(SMS)→H(Email)→K(Push)→L(Exit)
        "Cart Abandoned": "E",           # Just abandoned → Send SMS (first intervention)
        "Email Opened": "K",             # Email opened but no purchase → Send Push (final attempt)  
        "Email Unopened": "K",           # Email not opened → Send Push (escalate)
        "Push Notification Ignored": "L", # Push ignored → Exit journey (no response after 3 touches)
        "SMS Received": "H",             # SMS received but no purchase → Send Email with discount
        "Product Review Left": "D",      # Review indicates purchase → Exit: Purchase Completed
        "Wishlist Item Added": "E",      # Shows interest but no purchase → Send SMS
        "Discount Code Used": "D",       # Code usage indicates purchase → Exit: Purchase Completed
        "Social Media Shared": "D",      # Sharing indicates satisfaction/purchase → Exit: Purchase Completed
        "Return Customer": "A",          # Return customer starts new journey → User Adds Items to Cart
        "Subscription Started": "D",     # Subscription indicates conversion → Exit: Purchase Completed
        "Unsubscribed": "L"              # Unsubscribed → Exit: No Response After 3 Touches
    },
    "PulseFit": {
        # App engagement journey: A→E(Push)→H(Email)→K(SMS)→L(Exit)
        "User Inactive": "E",            # User inactive after signup → Send Push (re-engagement)
        "Push Notification Sent": "H",   # Push sent but still inactive → Send Email (workout tips)
        "Email Unopened": "K",           # Email not opened → Send SMS with discount
        "Workout Completed": "D",        # Workout done → Exit: User Engaged (success)
        "App Opened": "D",               # App opened shows engagement → Exit: User Engaged
        "Premium Upgrade": "D",          # Upgrade indicates engagement → Exit: User Engaged
        "Goal Achievement": "D",         # Goal achieved shows engagement → Exit: User Engaged
        "Friend Invited": "D",           # Social sharing shows engagement → Exit: User Engaged
        "Progress Photo Shared": "D",    # Photo sharing shows engagement → Exit: User Engaged
        "Subscription Cancelled": "L",   # Cancelled → Exit: User Remains Inactive
        "Support Contact": "H",          # Support needed → Send Email with workout help
        "Tutorial Skipped": "E"          # Tutorial skipped shows disengagement → Send Push
    },
    "JetQuest": {
        # Booking conversion journey: A→E(Email)→H(SMS)→K(Retargeting)→L(Exit)
        "Flight Searched": "E",          # Flight searched but not booked → Send Email (deal expires)
        "Booking Abandoned": "E",        # Booking abandoned → Send Email (deal expires)
        "Email Opened": "H",             # Email opened but no booking → Send SMS (last chance)
        "SMS Clicked": "K",              # SMS clicked but no booking → Send Retargeting Ad
        "Price Alert Set": "E",          # Price alert shows interest → Send Email about deals
        "Loyalty Points Earned": "D",    # Points earned indicates booking → Exit: Booking Completed
        "Review Left": "D",              # Review indicates completed trip → Exit: Booking Completed
        "Newsletter Subscribed": "E",    # Newsletter signup shows interest → Send Email with deals
        "Mobile App Downloaded": "E",    # App download shows interest → Send Email with deals
        "Customer Service Contact": "E", # Service contact → Send Email (helpful follow-up)
        "Refund Requested": "L",         # Refund requested → Exit: Deal Expired
        "Rebooking Attempt": "E"         # Rebooking shows continued interest → Send Email
    },
    "LeadSync": {
        # Trial activation journey: A→E(Email)→H(In-App)→K(CSM Alert)→L(Exit)
        "Trial Started": "E",            # Trial started → Send Email (setup guidance)
        "Demo Requested": "E",           # Demo requested → Send Email (follow up)
        "Email Unopened": "H",           # Email not opened → Send In-App message
        "Feature Explored": "D",         # Feature exploration shows engagement → Exit: Trial Converted
        "Integration Attempted": "H",    # Integration attempted but may need help → Send In-App guide
        "Onboarding Completed": "D",     # Onboarding done shows success → Exit: Trial Converted
        "Team Member Invited": "D",      # Team invitation shows commitment → Exit: Trial Converted
        "Billing Info Added": "D",       # Billing added indicates conversion → Exit: Trial Converted
        "Support Ticket Created": "H",   # Support needed → Send In-App help
        "Webinar Attended": "D",         # Webinar attendance shows engagement → Exit: Trial Converted
        "Case Study Downloaded": "H",    # Case study download shows interest → Send In-App guide
        "Contract Signed": "D"           # Contract signed → Exit: Trial Converted
    }
}

highlight_node = st.session_state.next_node_id or event_to_node_map.get(persona, {}).get(selected_event, "")
highlight_class = "classDef highlight fill:#ffcc00;" if highlight_node else ""
highlight_command = f"class {highlight_node} highlight;" if highlight_node else ""

# --- Node Descriptions for UI Display ---
node_descriptions = {
    "GlowSkin": {
        "A": "User adds items to cart",
        "E": "Send SMS: 'You left something behind'", 
        "H": "Send Email: 'Still want that glow? 10% off'",
        "K": "Send Push: 'Your GlowKit is waiting'",
        "D": "Exit: Purchase completed",
        "L": "Exit: No response after 3 touches"
    },
    "PulseFit": {
        "A": "User signs up for app",
        "E": "Send Push: 'Ready to crush your fitness goals?'", 
        "H": "Send Email: '5 Quick Workouts to Get Started'",
        "K": "Send SMS: 'Get 30% off premium'",
        "D": "Exit: User engaged",
        "L": "Exit: User remains inactive"
    },
    "JetQuest": {
        "A": "User browses flight deals",
        "E": "Send Email: 'Your flight deal expires soon'", 
        "H": "Send SMS: 'Last chance - save $200'",
        "K": "Send Retargeting Ad: Similar destinations",
        "D": "Exit: Booking completed",
        "L": "Exit: Deal expired"
    },
    "LeadSync": {
        "A": "User starts free trial",
        "E": "Send Email: 'Complete your setup in 5 minutes'", 
        "H": "Send In-App: 'Need help? Quick guide'",
        "K": "Alert CSM: High-value prospect needs attention",
        "D": "Exit: Trial converted",
        "L": "Exit: Trial expired"
    }
}

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

st.info("**Key Insight**: Notice how Iterable intelligently orchestrates the timing, channel selection, and messaging across your entire MarTech stack based on real customer behavior.")

# --- Event Status Display ---
if highlight_node:
    action_description = node_descriptions.get(persona, {}).get(highlight_node, "Continue journey")
    st.info(f"**Journey Update:** {selected_event} → Next Action: {action_description}")

# --- AI-Powered Event & Journey Intelligence ---
st.markdown("---")
st.subheader("AI-Powered Marketing Intelligence")

# Check if OpenAI API key is available
def check_openai_config():
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error("OpenAI API key not found in Streamlit secrets. Please configure your API key.")
            return False
        return True
    except Exception as e:
        st.error("Error accessing OpenAI configuration. Please check your Streamlit secrets.")
        return False

def make_openai_request(prompt, system_message, max_tokens=500):
    """Make an OpenAI API request with proper error handling"""
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated to a more reliable model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating AI response: {str(e)}")
        return None

col1, col2 = st.columns(2)

with col1:
    if st.button("Event Suggestions", use_container_width=True):
        if not check_openai_config():
            st.stop()
            
        # Clear other AI responses
        st.session_state.journey_optimization = ""
        
        with st.spinner("Generating event suggestions..."):
            timeline = st.session_state.event_timeline
            event_history = ", ".join(timeline) if timeline else "No events simulated."

            prompt = f"""
You are a senior marketing strategist at Iterable. You must provide recommendations that EXACTLY match the highlighted step in the customer journey diagram.

**Customer Profile:** {persona}
**Recent Event:** {selected_event}
**Event Timeline:** {event_history}

**CRITICAL: The journey diagram is currently highlighting this specific action:**
{node_descriptions.get(persona, {}).get(highlight_node, "Continue journey")}

**Complete Journey Context for {persona}:**
- **GlowSkin:** Cart Abandonment Recovery
  A: User Adds Items to Cart → E: Send SMS "You left something behind" → H: Send Email "Still want that glow? 10% off" → K: Send Push "Your GlowKit is waiting" → D/L: Exit

- **PulseFit:** App Re-engagement  
  A: User Signs Up → E: Send Push "Ready to crush your fitness goals?" → H: Send Email "5 Quick Workouts to Get Started" → K: Send SMS "Get 30% off premium" → D/L: Exit

- **JetQuest:** Booking Conversion
  A: User Browses Flights → E: Send Email "Your flight deal expires soon" → H: Send SMS "Last chance - save $200" → K: Send Retargeting Ad "Similar destinations" → D/L: Exit

- **LeadSync:** Trial Activation
  A: User Starts Trial → E: Send Email "Complete your setup in 5 minutes" → H: Send In-App "Need help? Quick guide" → K: Alert CSM "High-value prospect needs attention" → D/L: Exit

**MANDATORY REQUIREMENT:** Your recommendation must be about the HIGHLIGHTED ACTION ONLY: {node_descriptions.get(persona, {}).get(highlight_node, "Continue journey")}

**Provide your recommendation in this format:**

**Recommended Next Action:** [Must exactly match the highlighted action - if it's "Send SMS", recommend SMS strategy. If it's "Send Email", recommend email strategy, etc.]

**Strategic Reasoning:** [Why this specific highlighted action is the right next step for this event]

**Expected Outcome:** [What you expect from this specific action]

**Tactical Details:** [Specific messaging, timing, or implementation guidance for this highlighted action]

Do NOT recommend any action other than what is currently highlighted in the diagram.
            """

            response = make_openai_request(
                prompt, 
                "You are a senior marketing strategist specializing in customer engagement and MarTech.",
                500
            )
            
            if response:
                st.session_state.event_suggestion = response
                st.rerun()

with col2:
    if st.button("Journey Optimization", use_container_width=True):
        if not check_openai_config():
            st.stop()
            
        # Clear other AI responses
        st.session_state.event_suggestion = ""
        
        with st.spinner("Analyzing journey optimization..."):
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
5. **Expected Business Impact** - Quantified improvements in conversion rates and revenue

Focus on practical, actionable insights that would improve conversion rates and customer experience.
            """

            response = make_openai_request(
                prompt,
                "You are a customer journey optimization expert specializing in lifecycle marketing and conversion optimization.",
                600
            )
            
            if response:
                st.session_state.journey_optimization = response
                st.rerun()

# Display AI Responses for Event & Journey Intelligence
if st.session_state.event_suggestion:
    st.success("**Event-Specific Recommendations:**")
    st.markdown(st.session_state.event_suggestion)

if st.session_state.journey_optimization:
    st.success("**Journey Optimization Strategy:**")
    st.markdown(st.session_state.journey_optimization)

# --- Iterable's Cross-Channel Orchestration Hub ---
st.markdown("---")
st.subheader("Iterable's Cross-Channel Orchestration Hub")

with st.expander("Why Iterable is Your Marketing Command Center", expanded=False):
    st.markdown("""
    **Transform Your Disconnected MarTech Stack into a Unified Growth Engine**  
    
    Most companies have 15+ marketing tools that don't talk to each other, creating data silos and missed opportunities. 
    Iterable serves as your central orchestration layer, making every tool in your stack more effective.
    
    **What makes Iterable different:**
    - **Real-time Cross-Channel Decisions**: Unlike point solutions, Iterable coordinates email, SMS, push, and in-app messages in real-time
    - **Unified Customer Profiles**: Combines data from all sources to create a single view of each customer
    - **Intelligent Channel Selection**: AI automatically chooses the best channel and timing for each individual
    - **Workflow Automation**: Replace manual processes with automated, personalized customer journeys
    """)
    
    # Integration Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current MarTech Stack**")
        data_sources = st.multiselect("Select Your Current Tools:", [
            "Salesforce CRM",
            "Shopify/E-commerce Platform", 
            "Google Analytics",
            "Customer Data Platform (CDP)",
            "Product Analytics (Mixpanel/Amplitude)",
            "Support System (Zendesk)",
            "Billing System (Stripe)",
            "Data Warehouse (Snowflake/BigQuery)"
        ], default=["Salesforce CRM", "Shopify/E-commerce Platform"])
        
        current_challenges = st.multiselect("Current Challenges:", [
            "Data silos between tools",
            "Manual campaign coordination", 
            "Inconsistent customer experience",
            "No unified customer view",
            "Time-consuming campaign setup",
            "Poor cross-channel attribution"
        ], default=["Data silos between tools", "Manual campaign coordination"])
        
    with col2:
        st.markdown("**Channels to Orchestrate**")
        activation_channels = st.multiselect("Target Channels:", [
            "Email",
            "SMS", 
            "Push Notifications",
            "In-App Messages",
            "Direct Mail",
            "Webhooks to External Systems"
        ], default=["Email", "SMS", "Push Notifications"])
        
        team_size = st.selectbox("Marketing Team Size:", [
            "Small (1-5 people)",
            "Medium (6-15 people)", 
            "Large (16+ people)"
        ], index=1)

    # Dynamic Business Impact Calculator
    if data_sources and activation_channels and current_challenges:
        if st.button("Calculate Iterable's Business Impact"):
            if not check_openai_config():
                st.stop()
                
            with st.spinner("Calculating personalized business impact..."):
                prompt = f"""
You are an Iterable ROI analyst. Based on this prospect's current situation, calculate specific, quantified business impact:

**Current State:**
- Tech Stack: {', '.join(data_sources)}
- Challenges: {', '.join(current_challenges)}
- Channels: {', '.join(activation_channels)}
- Team Size: {team_size}
- Persona Focus: {persona}

**Calculate specific business impact metrics:**
1. **Conversion Rate Improvement** - Based on their channels and persona type
2. **Time Savings** - Hours saved per week from automation
3. **Revenue Impact** - Annual revenue increase estimate
4. **Campaign Efficiency** - Reduction in setup time and manual work
5. **Customer Experience Score** - Improvement in unified experience

Provide specific percentages and dollar amounts where possible. Make it realistic but compelling.

IMPORTANT: Format as a brief, scannable list with numbers. Use "dollars" instead of dollar signs to avoid formatting issues. Avoid using asterisks in your response.
                """

                response = make_openai_request(
                    prompt,
                    "You are an ROI analyst specializing in MarTech transformation impact calculations.",
                    400
                )
                
                if response:
                    st.session_state.business_impact = response
                    st.rerun()

    # Display calculated business impact
    if st.session_state.business_impact:
        st.markdown("**Calculated Business Impact:**")
        st.info(st.session_state.business_impact)

    # Enhanced Iterable Value Proposition Visualization
    if data_sources and activation_channels:
        st.markdown("---")
        st.markdown("**Iterable's Orchestration Impact**")
        
        # Create columns for before/after comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**BEFORE: Disconnected Stack**")
            st.error(f"""
**Current State:**
• {len(data_sources)} disconnected tools
• Manual campaign coordination
• Inconsistent customer experience
• Data silos and blind spots

**Problems:**
• {len(current_challenges)} major challenges
• Average 3-5 hour campaign setup
• 40% lower conversion rates
• No real-time optimization
            """)
        
        with col2:
            st.markdown("**AFTER: Iterable Orchestration**")
            st.success(f"""
**Unified Platform:**
• All {len(data_sources)} tools connected
• Automated cross-channel journeys
• Real-time personalization across {len(activation_channels)} channels
• Complete customer view

**Results:**
• 25-40% higher conversion rates
• 50% faster campaign deployment
• Unified customer experience
• AI-powered optimization
            """)
        
        # Overall impact summary
        st.markdown("**Industry Benchmarks - Typical Iterable Impact:**")
        st.caption("*These are average improvements seen across Iterable's customer base, not specific to your configuration above.*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Setup Time Reduction", "50%", "2-3 hours per campaign")
        with col2:
            st.metric("Conversion Rate Lift", "25-40%", "Unified experience")
        with col3:
            st.metric("Customer Satisfaction", "+35%", "Consistent messaging")

# --- Competitive Positioning Module ---
st.markdown("---")
st.subheader("Competitive Landscape Analysis")

with st.expander("Strategic Competitive Positioning", expanded=False):
    st.markdown("""
    **Position Iterable Against Key Competitors**  
    
    Enterprise deals are often competitive. This module helps you understand how to position Iterable's unique advantages 
    against major competitors based on the specific customer situation and journey context.
    
    **Strategic Approach:**
    - Focus on **fit vs. features** - what matters most for their specific use case
    - Emphasize **business outcomes** over technical specifications  
    - Address **real concerns** with professional, value-based responses
    """)
    
    # Competitor Selection and Context
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Competitive Situation**")
        primary_competitor = st.selectbox("Primary Competitor in Evaluation:", [
            "Braze",
            "Klaviyo", 
            "Salesforce Marketing Cloud",
            "Mailchimp",
            "SendGrid/Twilio Engage",
            "HubSpot",
            "Adobe Campaign"
        ])
        
    with col2:
        st.markdown("**Decision Factors**")
        key_priorities = st.multiselect("Customer's Top Priorities:", [
            "Ease of implementation",
            "Advanced personalization",
            "Cross-channel orchestration", 
            "Pricing/ROI",
            "Scalability",
            "Integration capabilities",
            "Mobile-first approach",
            "Enterprise security/compliance"
        ], default=["Cross-channel orchestration", "Ease of implementation"])

    # Competitive Comparison Matrix
    if primary_competitor and key_priorities:
        st.markdown(f"**Iterable vs. {primary_competitor} - Platform Comparison:**")
        
        # Build dynamic comparison based on customer priorities and competitor
        competitor_challenges = {
            "Braze": {
                "Ease of implementation": "Code-heavy implementation requiring months of technical development",
                "Advanced personalization": "Complex segmentation setup with rigid data schema constraints", 
                "Cross-channel orchestration": "Channel silos requiring separate configuration for each touchpoint",
                "Pricing/ROI": "Complex enterprise pricing with hidden implementation and professional service costs",
                "Scalability": "Technical debt accumulation as campaigns become more complex",
                "Integration capabilities": "API-heavy integrations requiring ongoing developer maintenance",
                "Mobile-first approach": "Strong mobile but disconnected from other channel experiences",
                "Enterprise security/compliance": "Enterprise features but complex compliance configuration"
            },
            "Klaviyo": {
                "Ease of implementation": "E-commerce focused setup with limitations beyond retail use cases",
                "Advanced personalization": "Basic behavioral triggers with limited cross-channel context",
                "Cross-channel orchestration": "Email-centric platform with add-on solutions for other channels", 
                "Pricing/ROI": "Rapid price escalation as contact volume and features increase",
                "Scalability": "SMB architecture with performance limitations at enterprise scale",
                "Integration capabilities": "E-commerce integrations but limited enterprise data connectivity",
                "Mobile-first approach": "Limited mobile capabilities beyond basic push notifications",
                "Enterprise security/compliance": "Growing enterprise features but still primarily SMB-focused"
            },
            "Salesforce Marketing Cloud": {
                "Ease of implementation": "Consultant-dependent setup requiring extensive professional services",
                "Advanced personalization": "Advanced capabilities but complex configuration and maintenance",
                "Cross-channel orchestration": "Powerful but requires technical expertise to coordinate channels",
                "Pricing/ROI": "Expensive module-based pricing with hidden costs for basic functionality",
                "Scalability": "Enterprise scale but with complexity overhead and slow deployment",
                "Integration capabilities": "Strong Salesforce ecosystem but complex external integrations",
                "Mobile-first approach": "Mobile capabilities exist but buried in complex interface design",
                "Enterprise security/compliance": "Strong compliance but requires significant configuration effort"
            },
            "Mailchimp": {
                "Ease of implementation": "Simple setup but limited advanced workflow capabilities",
                "Advanced personalization": "Basic automation with template-driven, non-dynamic content",
                "Cross-channel orchestration": "Email-focused with basic additional channel support",
                "Pricing/ROI": "Low initial cost but feature limitations become expensive constraints",
                "Scalability": "SMB platform with significant limitations at enterprise volume",
                "Integration capabilities": "Basic integrations with limited enterprise data flexibility",
                "Mobile-first approach": "Limited mobile strategy beyond basic responsive email",
                "Enterprise security/compliance": "Basic security adequate for SMB but not enterprise-grade"
            },
            "SendGrid/Twilio Engage": {
                "Ease of implementation": "Developer-focused implementation requiring technical resources",
                "Advanced personalization": "API-based personalization requiring custom development work",
                "Cross-channel orchestration": "Transactional focus with limited lifecycle marketing orchestration",
                "Pricing/ROI": "Developer tooling costs that don't align with marketing ROI metrics",
                "Scalability": "Excellent delivery scale but limited marketing campaign sophistication",
                "Integration capabilities": "Strong API connectivity but requires development effort",
                "Mobile-first approach": "SMS/communication focused but limited marketing journey capabilities",
                "Enterprise security/compliance": "Strong infrastructure but limited marketing compliance features"
            },
            "HubSpot": {
                "Ease of implementation": "CRM-first setup with marketing as secondary consideration",
                "Advanced personalization": "Generic automation limited by all-in-one platform constraints",
                "Cross-channel orchestration": "Basic marketing automation within CRM workflow limitations",
                "Pricing/ROI": "Bundle pricing for CRM features you may not need for marketing",
                "Scalability": "Good CRM scale but limited sophisticated marketing campaign capabilities",
                "Integration capabilities": "CRM-centric integrations with marketing data flexibility constraints",
                "Mobile-first approach": "Mobile CRM features but limited advanced mobile marketing",
                "Enterprise security/compliance": "CRM compliance focus with limited marketing-specific features"
            },
            "Adobe Campaign": {
                "Ease of implementation": "Legacy architecture requiring specialist consultants and lengthy setup",
                "Advanced personalization": "Advanced capabilities but complex configuration and user training",
                "Cross-channel orchestration": "Powerful orchestration but requires significant technical expertise",
                "Pricing/ROI": "Complex enterprise licensing with unpredictable cost scaling",
                "Scalability": "Enterprise scale but with outdated architecture and performance issues",
                "Integration capabilities": "Adobe ecosystem strength but complex external system connectivity",
                "Mobile-first approach": "Mobile capabilities exist but buried in legacy interface complexity",
                "Enterprise security/compliance": "Strong enterprise features but requiring extensive configuration"
            }
        }
        
        iterable_advantages = {
            "Ease of implementation": "Visual workflow builder with self-service setup - go live in weeks, not months",
            "Advanced personalization": "Real-time behavioral triggers with flexible data model and dynamic content",
            "Cross-channel orchestration": "Native omnichannel platform with unified customer journey coordination",
            "Pricing/ROI": "Transparent usage-based pricing with predictable scaling and no hidden costs",
            "Scalability": "Cloud-native architecture designed for enterprise scale with consistent performance",
            "Integration capabilities": "Flexible data integration with real-time activation across all channels",
            "Mobile-first approach": "Unified mobile strategy integrated with all touchpoints and customer context",
            "Enterprise security/compliance": "Built-in enterprise security with automated compliance and data governance"
        }
        
        # Create dynamic comparison based on selected priorities
        if key_priorities:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{primary_competitor} Limitations:**")
                competitor_content = ""
                for priority in key_priorities:
                    if priority in competitor_challenges[primary_competitor]:
                        competitor_content += f"**{priority}:**\n• {competitor_challenges[primary_competitor][priority]}\n\n"
                
                # Add additional context based on competitor
                additional_context = {
                    "Braze": "• Complex technical setup requiring developer resources\n• Steep learning curve for marketing teams\n• Hidden implementation costs and ongoing maintenance overhead",
                    "Klaviyo": "• Limited enterprise features and scalability constraints\n• E-commerce focus limits cross-industry applicability\n• Rapid cost escalation as usage grows beyond SMB levels",
                    "Salesforce Marketing Cloud": "• Requires extensive consultant support and training\n• Module-based architecture creates feature silos\n• Legacy architecture impacts performance and user experience",
                    "Mailchimp": "• Basic automation capabilities insufficient for enterprise needs\n• Limited data flexibility and advanced segmentation options\n• Template-driven approach restricts personalization depth",
                    "SendGrid/Twilio Engage": "• Developer-first platform requires technical expertise\n• Limited marketing-specific features and journey capabilities\n• API complexity creates barriers for marketing team adoption",
                    "HubSpot": "• All-in-one approach creates feature limitations\n• CRM-centric design constrains marketing flexibility\n• Generic automation lacks specialized engagement capabilities",
                    "Adobe Campaign": "• Legacy platform with outdated user interface\n• Complex implementation requiring specialized consultants\n• Batch processing limitations impact real-time capabilities"
                }
                
                competitor_content += f"\n**Additional Challenges:**\n{additional_context.get(primary_competitor, '')}"
                
                st.error(competitor_content if competitor_content else f"{primary_competitor} approach has limitations in your priority areas.")
            
            with col2:
                st.markdown("**Iterable's Advantage:**")
                iterable_content = ""
                for priority in key_priorities:
                    if priority in iterable_advantages:
                        iterable_content += f"**{priority}:**\n• {iterable_advantages[priority]}\n\n"
                
                # Add additional Iterable advantages in organized categories
                iterable_content += f"""
**Additional Competitive Strengths:**

**Platform Architecture:**
• Modern cloud-native infrastructure designed for marketing teams
• Self-service setup requiring minimal technical resources

**Data & Orchestration:**  
• Unified customer data model across all touchpoints
• Real-time decisioning and instant campaign updates

**User Experience:**
• Drag-and-drop workflow builder with visual journey mapping
• Comprehensive analytics and attribution across all channels"""
                
                st.success(iterable_content if iterable_content else "Iterable addresses your key priorities with modern platform capabilities.")

# --- Footer ---
st.markdown("---")
st.markdown("*This demo showcases Iterable's platform capabilities and Solutions Consultant expertise in customer journey orchestration.*")
