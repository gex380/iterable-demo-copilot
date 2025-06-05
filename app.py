import streamlit as st
import streamlit.components.v1 as components
import openai
import re

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
- **Campaign Suggestions**: Immediate tactical recommendations based on customer behavior
- **Journey Optimization**: Strategic improvements to increase conversion rates  
- **A/B Testing Center**: Scientific approach to validating marketing decisions
- **ROI Assessment**: Quantified business impact of switching to Iterable's orchestration platform

This showcases Iterable's unique value: turning your collection of marketing tools into an intelligent, coordinated growth engine.
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
    st.session_state.ab_test_strategy = ""
    st.session_state.integration_analysis = ""
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
if "ab_test_strategy" not in st.session_state:
    st.session_state.ab_test_strategy = ""
if "integration_analysis" not in st.session_state:
    st.session_state.integration_analysis = ""

if st.button("Add Event to Timeline"):
    if selected_event not in st.session_state.event_timeline:
        st.session_state.event_timeline.append(selected_event)

if st.button("Reset Timeline"):
    st.session_state.event_timeline = []
    st.session_state.next_node_id = ""
    st.session_state.campaign_suggestion = ""
    st.session_state.journey_optimization = ""
    st.session_state.ab_test_strategy = ""
    st.session_state.integration_analysis = ""

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
    st.info(f"**Event Simulation:** {selected_event} - Highlighted in journey diagram")

# --- A/B Testing Module ---
st.markdown("---")
st.subheader("A/B Testing Center")

with st.expander("A/B Test Setup & Analysis", expanded=False):
    st.markdown("""
    **Smart A/B Testing with AI-Powered Insights**  
    Generate test hypotheses, calculate sample sizes, and get AI recommendations based on your current timeline and persona behavior.
    
    **How Timeline Events Affect Testing:**
    - **Cart Abandoned + Email Unopened**: Tests focus on subject line optimization and send time
    - **Push Ignored + SMS Received**: Tests emphasize message content and channel preference  
    - **Multiple Touchpoints**: Tests prioritize cross-channel coordination and frequency capping
    - **High Engagement Events**: Tests explore upsell opportunities and personalization depth
    """)
    
    # A/B Test Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Test Configuration**")
        test_type = st.selectbox("Test Type:", [
            "Subject Line Variation", 
            "Send Time Optimization", 
            "Content Personalization",
            "CTA Button Text",
            "Email Template Design",
            "Discount Amount"
        ])
        
        current_metric = st.number_input("Current Conversion Rate (%)", min_value=0.1, max_value=50.0, value=2.5, step=0.1)
        expected_lift = st.number_input("Expected Lift (%)", min_value=1.0, max_value=100.0, value=15.0, step=1.0)
        confidence_level = st.selectbox("Confidence Level:", ["90%", "95%", "99%"], index=1)
        
    with col2:
        st.markdown("**Sample Size Calculator**")
        # Simple sample size calculation
        base_rate = current_metric / 100
        lift_rate = (current_metric + expected_lift) / 100
        
        # Simplified statistical calculation
        import math
        z_score = {"90%": 1.645, "95%": 1.96, "99%": 2.576}[confidence_level]
        pooled_rate = (base_rate + lift_rate) / 2
        sample_size = int((2 * pooled_rate * (1 - pooled_rate) * (z_score / (lift_rate - base_rate))**2))
        
        st.metric("Required Sample Size (per variant):", f"{sample_size:,}")
        st.metric("Total Test Duration:", f"{math.ceil(sample_size / 1000)} days*")
        st.caption("*Assuming 1,000 sends per day")

    # Timeline Context for Testing
    if st.session_state.event_timeline:
        st.markdown("**Current Timeline Context:**")
        timeline_str = " → ".join(st.session_state.event_timeline)
        st.write(f"**{timeline_str}**")
        st.caption("AI will use this context to generate relevant test strategies")

    if st.button("Generate A/B Test Strategy"):
        # Clear other AI responses
        st.session_state.campaign_suggestion = ""
        st.session_state.journey_optimization = ""
        st.session_state.integration_analysis = ""
        
        with st.spinner("Generating AI-powered test strategy..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                prompt = f"""
You are a senior CRO (Conversion Rate Optimization) expert at Iterable. Generate a comprehensive A/B testing strategy for:

**Test Details:**
- Persona: {persona}
- Test Type: {test_type}
- Current Conversion Rate: {current_metric}%
- Expected Lift: {expected_lift}%
- Required Sample Size: {sample_size:,} per variant

**Critical Context - User Timeline:** {', '.join(st.session_state.event_timeline) if st.session_state.event_timeline else 'No specific events'}

**Timeline Impact on Testing:**
Based on the user's event timeline, explain how their specific behavior pattern should influence the test design. For example:
- If they abandoned cart but opened emails: focus on email content tests
- If they ignored push notifications: test alternative messaging channels
- If they engaged with discounts: test pricing and offer strategies

Provide:
1. **Test Hypothesis** - Clear, testable prediction based on timeline behavior
2. **Variant Recommendations** - Specific A vs B suggestions tailored to their journey stage  
3. **Success Metrics** - Primary and secondary KPIs to track
4. **Timeline-Specific Insights** - How their behavior pattern affects test design
5. **Risk Assessment** - Potential downsides to watch for
6. **Next Test Ideas** - Follow-up experiments based on results

Make recommendations specific to {persona} persona, {test_type} testing, and their timeline behavior pattern.
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior CRO expert specializing in email marketing optimization and statistical testing methodology."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )

                st.session_state.ab_test_strategy = response.choices[0].message.content
                st.rerun()

            except Exception as e:
                st.error(f"Error generating A/B test strategy: {str(e)}")

# --- MarTech Integration Visualizer ---
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
        st.markdown("**Iterable's Impact**")
        activation_channels = st.multiselect("Channels to Orchestrate:", [
            "Email",
            "SMS", 
            "Push Notifications",
            "In-App Messages",
            "Direct Mail",
            "Webhooks to External Systems"
        ], default=["Email", "SMS", "Push Notifications"])
        
        business_outcomes = st.multiselect("Expected Business Impact:", [
            "25-40% increase in conversion rates",
            "50% reduction in campaign setup time",
            "Unified customer experience",
            "Real-time personalization",
            "Automated lifecycle campaigns",
            "Complete attribution visibility"
        ], default=["25-40% increase in conversion rates", "50% reduction in campaign setup time"])

    if st.button("Generate Iterable ROI Assessment"):
        # Clear other AI responses
        st.session_state.campaign_suggestion = ""
        st.session_state.journey_optimization = ""
        st.session_state.ab_test_strategy = ""
        
        with st.spinner("Calculating Iterable's business impact..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                prompt = f"""
You are an Iterable solutions architect presenting to a prospective enterprise client. Create a compelling ROI assessment that shows Iterable's unique value:

**Client's Current State:**
- Persona: {persona}
- Current Tools: {', '.join(data_sources)}
- Current Challenges: {', '.join(current_challenges)}
- Target Channels: {', '.join(activation_channels)}
- Expected Outcomes: {', '.join(business_outcomes)}
- Customer Journey Context: {', '.join(st.session_state.event_timeline) if st.session_state.event_timeline else 'Standard journey'}

**Focus on Iterable's Competitive Advantages:**
1. **Cross-Channel Orchestration** - How Iterable coordinates all channels in real-time (unlike point solutions)
2. **Unified Customer Profiles** - Single view across all touchpoints 
3. **AI-Powered Optimization** - Automatic channel, timing, and content optimization
4. **Workflow Automation** - Replace manual processes with intelligent automation
5. **Real-Time Decisioning** - Instant responses to customer behavior
6. **ROI Impact** - Specific business outcomes and timeframes

**Provide:**
1. **Current State Problems** - What's broken with their disconnected stack
2. **Iterable's Solution** - How we solve these specific problems uniquely  
3. **Business Impact** - Quantified improvements (conversion rates, efficiency, revenue)
4. **Implementation Roadmap** - Clear path to value realization
5. **Competitive Differentiation** - Why Iterable vs. other solutions

Make this sound like a compelling business case that would convince a CMO to invest.
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an Iterable solutions architect specializing in enterprise ROI assessments and competitive positioning."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )

                st.session_state.integration_analysis = response.choices[0].message.content
                st.rerun()

            except Exception as e:
                st.error(f"Error generating ROI assessment: {str(e)}")

    # Iterable Value Proposition Visualization
    if data_sources and activation_channels:
        st.markdown("**Iterable's Orchestration Impact**")
        
        # Show before/after comparison
        before_after = f"""
BEFORE ITERABLE (Disconnected):
{' + '.join(data_sources)} → Manual Processes → {' + '.join(activation_channels)}
❌ Data silos
❌ Manual coordination  
❌ Inconsistent experience
❌ No real-time optimization

AFTER ITERABLE (Orchestrated):
{' + '.join(data_sources)} → ITERABLE ORCHESTRATION HUB → {' + '.join(activation_channels)}
✅ Unified customer profiles
✅ Automated cross-channel journeys
✅ Real-time personalization  
✅ AI-powered optimization
✅ Complete attribution

BUSINESS IMPACT: {', '.join(business_outcomes)}
        """
        
        st.code(before_after, language=None)

# --- AI Suggestion Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Campaign Suggestions", use_container_width=True):
        # Clear other AI responses
        st.session_state.journey_optimization = ""
        st.session_state.ab_test_strategy = ""
        st.session_state.integration_analysis = ""
        
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
    if st.button("Journey Optimization", use_container_width=True):
        # Clear other AI responses
        st.session_state.campaign_suggestion = ""
        st.session_state.ab_test_strategy = ""
        st.session_state.integration_analysis = ""
        
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

# --- Display AI Responses ---
if st.session_state.campaign_suggestion:
    st.success("**Campaign Suggestion:**")
    st.markdown(st.session_state.campaign_suggestion)

if st.session_state.journey_optimization:
    st.success("**Journey Optimization:**")
    st.markdown(st.session_state.journey_optimization)

if st.session_state.ab_test_strategy:
    st.success("**A/B Test Strategy:**")
    st.markdown(st.session_state.ab_test_strategy)

if st.session_state.integration_analysis:
    st.success("**Iterable ROI Assessment:**")
    st.markdown(st.session_state.integration_analysis)
