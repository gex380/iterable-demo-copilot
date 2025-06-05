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
            with st.spinner("Calculating personalized business impact..."):
                try:
                    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    
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

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an ROI analyst specializing in MarTech transformation impact calculations."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=400
                    )

                    st.session_state.business_impact = response.choices[0].message.content
                    st.rerun()

                except Exception as e:
                    st.error(f"Error calculating business impact: {str(e)}")

    # Display calculated business impact
    if hasattr(st.session_state, 'business_impact') and st.session_state.business_impact:
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
            "No unified customer viewimport streamlit as st
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
    
    **Customer Journey Simulation**
    - **Persona Selection**: Choose from e-commerce, SaaS, or fintech customer profiles
    - **Dynamic Event Timeline**: Build realistic customer journeys with purchase, browse, abandon, and support events
    - **Context-Aware AI**: All recommendations adapt based on the specific journey you create
    
    **Visual Journey Orchestration**  
    - **Before/After Transformation**: See the dramatic difference between disconnected tools vs. Iterable's orchestration
    - **Real-Time Visualization**: Watch your customer journey come to life with dynamic, color-coded progression
    - **Professional Presentation**: Client-ready visualization that clearly demonstrates value
    
    **Business Impact Calculator**
    - **MarTech Stack Configuration**: Input your current tools, team size, and monthly volume
    - **Personalized ROI Analysis**: Get AI-generated business impact calculations specific to your situation
    - **Industry Benchmarks**: Compare your potential results with typical Iterable customer improvements
    
    **AI-Powered Marketing Intelligence**
    - **Event Suggestions**: Immediate tactical recommendations based on specific customer events and journey context
    - **Journey Optimization**: Strategic improvements to increase conversion rates and customer lifetime value
    - **A/B Testing Center**: Scientific approach to validating marketing decisions with specific test designs
    
    **Competitive Positioning Module**
    - **Dynamic Competitor Analysis**: Professional comparisons vs. Braze, Klaviyo, Salesforce Marketing Cloud, and other major players
    - **Priority-Based Messaging**: Positioning automatically adapts based on what matters most to your specific situation
    - **Client-Ready Presentation**: Visual before/after competitive comparisons suitable for prospect meetings
    
    **Solutions Consultant Excellence**
    - **Consultative Discovery**: Demonstrates needs assessment and solution tailoring capabilities
    - **Technical Competence**: Shows understanding of MarTech integration and data orchestration
    - **Business Acumen**: Quantifies value and ROI in business terms that matter to executives
    - **Competitive Intelligence**: Professional positioning against market leaders without disparaging competitors
    - **Presentation Skills**: Clean, engaging demo flow suitable for C-level presentations
    
    This showcases Iterable's unique value: turning your collection of marketing tools into an intelligent, coordinated growth engine while demonstrating the strategic thinking and technical competence expected from elite Solutions Consultants.
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
    st.session_state.event_suggestion = ""
    st.session_state.journey_optimization = ""
    st.session_state.ab_test_strategy = ""
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

# --- Timeline Tracking ---
if "event_timeline" not in st.session_state:
    st.session_state.event_timeline = []
if "next_node_id" not in st.session_state:
    st.session_state.next_node_id = ""
if "event_suggestion" not in st.session_state:
    st.session_state.event_suggestion = ""
if "journey_optimization" not in st.session_state:
    st.session_state.journey_optimization = ""
if "ab_test_strategy" not in st.session_state:
    st.session_state.ab_test_strategy = ""
if "business_impact" not in st.session_state:
    st.session_state.business_impact = ""

if st.button("Add Event to Timeline"):
    if selected_event not in st.session_state.event_timeline:
        st.session_state.event_timeline.append(selected_event)

if st.button("Reset Timeline"):
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.event_suggestion = ""
    st.session_state.journey_optimization = ""
    st.session_state.ab_test_strategy = ""
    st.session_state.business_impact = ""

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

st.info("**Key Insight**: Notice how Iterable creates a unified customer experience by coordinating all your existing tools, rather than replacing them.")

# --- Event Status Display ---
if highlight_node:
    st.info(f"**Event Simulation:** {selected_event} - Highlighted in journey diagram")

# --- AI-Powered Event & Journey Intelligence ---
st.markdown("---")
st.subheader("AI-Powered Marketing Intelligence")

col1, col2 = st.columns(2)

with col1:
    if st.button("Event Suggestions", use_container_width=True):
        # Clear other AI responses
        st.session_state.journey_optimization = ""
        st.session_state.ab_test_strategy = ""
        
        with st.spinner("Generating event suggestions..."):
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

                st.session_state.event_suggestion = response.choices[0].message.content
                st.rerun()

            except Exception as e:
                st.error(f"Error generating event suggestions: {str(e)}")
                st.info("Please check your OpenAI API key configuration in Streamlit secrets.")

with col2:
    if st.button("Journey Optimization", use_container_width=True):
        # Clear other AI responses
        st.session_state.event_suggestion = ""
        st.session_state.ab_test_strategy = ""
        
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
5. **Expected Business Impact** - Quantified improvements in conversion rates and revenue

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

# Display AI Responses for Event & Journey Intelligence
if st.session_state.event_suggestion:
    st.success("**Event-Specific Recommendations:**")
    st.markdown(st.session_state.event_suggestion)

if st.session_state.journey_optimization:
    st.success("**Journey Optimization Strategy:**")
    st.markdown(st.session_state.journey_optimization)

# --- A/B Testing Strategy Center ---
st.markdown("---")
st.subheader("A/B Testing Strategy Center")

with st.expander("Scientific Testing Framework", expanded=False):
    st.markdown("""
    **Validate Your Marketing Decisions with Data**
    
    Iterable's A/B testing capabilities help you make data-driven decisions about your customer engagement strategy.
    This module generates specific test recommendations based on your customer journey and current events.
    """)
    
    if st.session_state.event_timeline:
        if st.button("Generate A/B Test Strategy"):
            # Clear other AI responses
            st.session_state.event_suggestion = ""
            st.session_state.journey_optimization = ""
            
            with st.spinner("Designing A/B test strategy..."):
                try:
                    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    timeline = st.session_state.event_timeline
                    event_history = ", ".join(timeline) if timeline else "No events simulated."

                    prompt = f"""
You are a conversion optimization expert designing A/B tests for Iterable's platform. Based on the customer persona '{persona}' and their journey: {event_history}

Design a comprehensive A/B testing strategy including:

1. **Primary Test Hypothesis** - What you want to prove/disprove
2. **Test Variables** - Specific elements to test (subject lines, timing, channels, content)
3. **Success Metrics** - How to measure test performance 
4. **Sample Size & Duration** - Statistical requirements for valid results
5. **Expected Impact** - Predicted improvement ranges

Focus on tests that would have the highest impact on conversion rates and customer experience for this specific journey and persona.

Make recommendations practical and implementable within Iterable's testing framework.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a conversion optimization expert specializing in A/B testing and statistical analysis for marketing campaigns."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=600
                    )

                    st.session_state.ab_test_strategy = response.choices[0].message.content
                    st.rerun()

                except Exception as e:
                    st.error(f"Error generating A/B test strategy: {str(e)}")
                    st.info("Please check your OpenAI API key configuration in Streamlit secrets.")
    else:
        st.info("**Build a customer journey above to get personalized A/B testing recommendations**")

# --- Business Impact Calculator ---
st.markdown("---")
st.subheader("Business Impact Calculator")

with st.expander("Calculate Iterable's ROI for Your Organization", expanded=False):
    st.markdown("**See the quantified business impact of implementing Iterable's orchestration platform**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Current MarTech Stack**")
        email_platform = st.selectbox("Email Platform:", ["Mailchimp", "Constant Contact", "Campaign Monitor", "Other"])
        sms_platform = st.selectbox("SMS Platform:", ["Twilio", "Attentive", "Postscript", "Other"])
        push_platform = st.selectbox("Push Platform:", ["OneSignal", "Airship", "Firebase", "Other"])
        
    with col2:
        st.markdown("**Team & Volume**")
        team_size = st.number_input("Marketing Team Size:", min_value=1, max_value=50, value=5)
        monthly_emails = st.number_input("Monthly Email Volume:", min_value=1000, max_value=10000000, value=100000, step=10000)
        monthly_revenue = st.number_input("Monthly Revenue ($):", min_value=10000, max_value=100000000, value=500000, step=50000)
        
    with col3:
        st.markdown("**Current Challenges**")
        challenges = st.multiselect("Primary Pain Points:", [
            "Manual campaign coordination",
            "Inconsistent customer experience", 
            "Poor campaign timing",
            "Limited personalization",
            "Fragmented customer data",
            "High tool management overhead"
        ])
    
    if email_platform and sms_platform and challenges:
        if st.button("Calculate Iterable's Business Impact"):
            # Clear other AI responses  
            st.session_state.event_suggestion = ""
            st.session_state.journey_optimization = ""
            st.session_state.ab_test_strategy = ""
            
            with st.spinner("Calculating personalized business impact..."):
                try:
                    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    
                    prompt = f"""
You are a business impact analyst calculating ROI for Iterable's customer engagement platform. Based on this organization's profile:

**Current Setup:**
- Email Platform: {email_platform}
- SMS Platform: {sms_platform}  
- Push Platform: {push_platform}
- Team Size: {team_size} people
- Monthly Email Volume: {monthly_emails:,}
- Monthly Revenue: ${monthly_revenue:,}
- Primary Challenges: {', '.join(challenges)}

**Calculate specific business impact including:**

1. **Cost Savings** - Tool consolidation, reduced manual work, team efficiency gains
2. **Revenue Impact** - Improved conversion rates, better timing, increased personalization
3. **Time Savings** - Automation benefits, reduced campaign setup time
4. **Implementation Timeline** - Expected timeline and resource requirements
5. **ROI Summary** - Quantified return on investment with specific metrics

Use realistic industry benchmarks for marketing automation ROI. Provide specific dollar amounts and percentages where possible.

Make calculations realistic and conservative, focusing on measurable business outcomes that would resonate with finance teams and executives.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a business impact analyst specializing in MarTech ROI analysis and platform consolidation benefits."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=800
                    )

                    st.session_state.business_impact = response.choices[0].message.content
                    st.rerun()

                except Exception as e:
                    st.error(f"Error calculating business impact: {str(e)}")
    
    # Display business impact analysis
    if st.session_state.business_impact:
        st.success("**Personalized Business Impact Analysis:**")
        st.markdown(st.session_state.business_impact)

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
                
                # Add additional Iterable advantages
                iterable_context = {
                    "general": "• Modern cloud-native architecture built for marketing teams\n• Self-service platform requiring minimal technical resources\n• Unified customer data model across all touchpoints\n• Real-time decisioning and instant campaign updates\n• Drag-and-drop workflow builder with visual journey mapping\n• Comprehensive analytics and attribution across all channels"
                }
                
                iterable_content += f"\n**Platform Advantages:**\n{iterable_context['general']}"
                
                st.success(iterable_content if iterable_content else "Iterable addresses your key priorities with modern platform capabilities.")

# Display A/B Test Strategy
if st.session_state.ab_test_strategy:
    st.success("**A/B Test Strategy:**")
    st.markdown(st.session_state.ab_test_strategy)

# --- Footer ---
st.markdown("---")
st.markdown("*This demo showcases Iterable's platform capabilities and Solutions Consultant expertise in customer journey orchestration.*")
