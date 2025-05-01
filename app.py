import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Zetra Customer Journey",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply retro gaming aesthetic with custom CSS
def add_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
    
    /* Main container styling */
    .main {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Space Mono', monospace;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'VT323', monospace;
        text-transform: uppercase;
        color: #00ffff;
        text-shadow: 2px 2px 0px #ff0066;
        padding: 5px 0;
        margin: 5px 0;
    }
    
    /* Text-based display elements */
    .text-display {
        font-family: 'VT323', monospace;
        background-color: #1e1e2f;
        border: 2px solid #00ffff;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
    }
    
    /* Text tables */
    .text-table {
        font-family: 'Space Mono', monospace;
        border-collapse: collapse;
        width: 100%;
        margin: 10px 0;
    }
    
    .text-table th {
        background-color: #121212;
        color: #00ffff;
        text-align: left;
        padding: 8px;
        font-family: 'VT323', monospace;
        border-bottom: 2px solid #00ffff;
    }
    
    .text-table td {
        padding: 8px;
        border-bottom: 1px solid #2d2d44;
    }
    
    .text-table tr:hover {
        background-color: #2d2d44;
    }
    
    /* Metric display */
    .text-metric {
        font-family: 'VT323', monospace;
        font-size: 24px;
        padding: 15px;
        margin: 5px 0;
        background-color: #1e1e2f;
        border-left: 4px solid #00ffff;
    }
    
    .text-metric-value {
        font-size: 36px;
        color: #00ffff;
        text-shadow: 2px 2px 0px #ff0066;
    }
    
    .text-metric-label {
        color: #ffffff;
        text-transform: uppercase;
    }
    
    /* Section headers with retro gaming style */
    .section-header {
        font-family: 'VT323', monospace;
        font-size: 28px;
        color: #ff0066;
        text-shadow: 2px 2px 0px #00ffff;
        margin: 20px 0 10px 0;
        padding: 5px 0;
        border-bottom: 2px dashed #00ffff;
        text-transform: uppercase;
    }
    
    /* ASCII art container */
    .ascii-art {
        font-family: monospace;
        white-space: pre;
        font-size: 14px;
        color: #00ffff;
        background-color: #1e1e2f;
        padding: 15px;
        border: 2px solid #ff0066;
        overflow-x: auto;
    }
    
    /* Nav menu */
    .nav-menu {
        display: flex;
        justify-content: space-around;
        background-color: #1e1e2f;
        padding: 10px;
        margin-bottom: 20px;
        border: 2px solid #00ffff;
    }
    
    .nav-item {
        font-family: 'VT323', monospace;
        font-size: 24px;
        color: #00ffff;
        cursor: pointer;
        padding: 5px 15px;
    }
    
    .nav-item-active {
        color: #ffffff;
        background-color: #ff0066;
        padding: 5px 15px;
    }
    
    /* Progress bars */
    .progress-container {
        background-color: #1e1e2f;
        height: 25px;
        width: 100%;
        position: relative;
        margin: 10px 0;
        border: 1px solid #00ffff;
    }
    
    .progress-bar {
        background-color: #00ffff;
        height: 100%;
        color: #121212;
        text-align: center;
        line-height: 25px;
        font-family: 'VT323', monospace;
    }
    
    /* Custom horizontal bar representation using text */
    .text-bar {
        font-family: 'Space Mono', monospace;
        display: flex;
        align-items: center;
        margin: 8px 0;
    }
    
    .text-bar-label {
        width: 200px;
        text-align: right;
        padding-right: 10px;
        color: #ffffff;
    }
    
    .text-bar-visual {
        flex-grow: 1;
        height: 20px;
        position: relative;
    }
    
    .text-bar-fill {
        position: absolute;
        height: 100%;
        background-color: #00ffff;
        color: #121212;
        display: flex;
        align-items: center;
        font-family: 'VT323', monospace;
        padding-left: 5px;
    }
    
    /* Simple button style */
    .text-button {
        display: inline-block;
        font-family: 'VT323', monospace;
        font-size: 20px;
        color: #ffffff;
        background-color: #ff0066;
        border: 2px solid #00ffff;
        padding: 8px 16px;
        margin: 5px;
        cursor: pointer;
        text-align: center;
    }
    
    .text-button:hover {
        background-color: #ff4488;
    }
    
    /* Terminal-like container */
    .terminal {
        background-color: #1e1e2f;
        color: #00ffff;
        font-family: 'Space Mono', monospace;
        padding: 15px;
        border: 2px solid #00ffff;
        margin: 10px 0;
        overflow-x: auto;
    }
    
    .terminal-text {
        white-space: pre-wrap;
        color: #ffffff;
    }
    
    .terminal-highlight {
        color: #ff0066;
    }
    
    /* Alert boxes */
    .alert-box {
        border-left: 4px solid #ff0066;
        background-color: #1e1e2f;
        padding: 10px 15px;
        margin: 10px 0;
        font-family: 'Space Mono', monospace;
    }
    
    .alert-title {
        color: #ff0066;
        font-family: 'VT323', monospace;
        font-size: 18px;
        margin-bottom: 5px;
    }
    
    .alert-content {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Generate synthetic data
def generate_synthetic_data():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Companies
    companies = [
        "TechCorp", "InnovateSys", "DataFlow", "CloudNine", 
        "PivotSoft", "Nexus Solutions", "BrightPath", "QuantumTech",
        "VisionWare", "Meridian Systems", "CyberLink", "OmniTools"
    ]
    
    # Industries
    industries = ["Technology", "Finance", "Healthcare", "Manufacturing", "Retail", "Energy"]
    
    # Customer segments
    segments = ["Enterprise", "Mid-Market", "SMB", "Startup"]
    
    # Journey stages
    journey_stages = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
    
    # Touchpoints
    touchpoints = [
        "Website", "Sales Call", "Email", "Demo", "Webinar", 
        "Support Ticket", "Contract Negotiation", "Training", 
        "Product Update", "QBR", "Account Review"
    ]
    
    # Pain points
    pain_points = [
        "Unclear Pricing", "Long Sales Cycle", "Complex Onboarding",
        "Technical Issues", "Poor Support Response", "Feature Gaps",
        "Contract Complexity", "Billing Issues", "User Experience"
    ]
    
    # Personas
    personas = [
        "Decision Maker", "Technical User", "Admin User", 
        "Finance Manager", "End User", "IT Manager"
    ]
    
    # Customer information
    num_customers = 200
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 4, 1)
    
    # Customer data
    customer_data = []
    
    for i in range(num_customers):
        company = random.choice(companies)
        industry = random.choice(industries)
        segment = random.choice(segments)
        
        # Generate contract value based on segment
        if segment == "Enterprise":
            contract_value = random.uniform(100000, 500000)
        elif segment == "Mid-Market":
            contract_value = random.uniform(50000, 100000)
        elif segment == "SMB":
            contract_value = random.uniform(10000, 50000)
        else:  # Startup
            contract_value = random.uniform(5000, 10000)
        
        # Generate onboarding date
        onboarding_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        # Generate contract renewal date (1 year after onboarding)
        renewal_date = onboarding_date + timedelta(days=365)
        
        # Generate current journey stage based on dates
        days_since_onboarding = (datetime.now() - onboarding_date).days
        
        if days_since_onboarding < 0:
            current_stage = random.choice(["Awareness", "Consideration", "Purchase"])
        elif days_since_onboarding < 30:
            current_stage = "Onboarding"
        elif days_since_onboarding < 300:
            current_stage = "Usage"
        elif days_since_onboarding < 365:
            current_stage = "Renewal"
        else:
            current_stage = random.choice(["Renewal", "Advocacy"])
        
        # Add to customer data
        customer_data.append({
            "customer_id": i + 1,
            "company_name": company,
            "industry": industry,
            "segment": segment,
            "contract_value": contract_value,
            "onboarding_date": onboarding_date,
            "renewal_date": renewal_date,
            "current_stage": current_stage
        })
    
    # Create customers dataframe
    customers_df = pd.DataFrame(customer_data)
    
    # Generate journey interactions
    interactions_data = []
    
    for i, customer in customers_df.iterrows():
        # Number of interactions depends on how long they've been a customer
        days_since_onboarding = max(0, (datetime.now() - customer["onboarding_date"]).days)
        num_interactions = max(1, int(days_since_onboarding / 14))  # Approximately bi-weekly interactions
        
        for j in range(num_interactions):
            # Interaction date progresses from onboarding date
            interaction_date = customer["onboarding_date"] + timedelta(days=j * random.randint(10, 20))
            
            # Determine journey stage based on time since onboarding
            days_passed = (interaction_date - customer["onboarding_date"]).days
            if days_passed < 0:
                stage = random.choice(["Awareness", "Consideration", "Purchase"])
            elif days_passed < 30:
                stage = "Onboarding"
            elif days_passed < 300:
                stage = "Usage"
            elif days_passed < 365:
                stage = "Renewal"
            else:
                stage = random.choice(["Renewal", "Advocacy"])
            
            # Determine touchpoint based on stage
            if stage in ["Awareness", "Consideration"]:
                possible_touchpoints = ["Website", "Sales Call", "Email", "Demo", "Webinar"]
            elif stage == "Purchase":
                possible_touchpoints = ["Sales Call", "Contract Negotiation", "Email"]
            elif stage == "Onboarding":
                possible_touchpoints = ["Training", "Support Ticket", "Email"]
            elif stage == "Usage":
                possible_touchpoints = ["Support Ticket", "Product Update", "Email"]
            elif stage == "Renewal":
                possible_touchpoints = ["Account Review", "QBR", "Sales Call"]
            else:  # Advocacy
                possible_touchpoints = ["Webinar", "Product Update", "QBR"]
                
            touchpoint = random.choice(possible_touchpoints)
            
            # Determine persona based on touchpoint
            if touchpoint in ["Sales Call", "Contract Negotiation", "Account Review", "QBR"]:
                persona = random.choice(["Decision Maker", "Finance Manager"])
            elif touchpoint in ["Demo", "Product Update", "Support Ticket"]:
                persona = random.choice(["Technical User", "End User", "IT Manager"])
            elif touchpoint == "Training":
                persona = random.choice(["Admin User", "End User"])
            else:
                persona = random.choice(personas)
            
            # Determine pain point based on touchpoint (some touchpoints don't have pain points)
            if touchpoint in ["Sales Call", "Contract Negotiation"]:
                possible_pain_points = ["Unclear Pricing", "Long Sales Cycle", "Contract Complexity"]
            elif touchpoint in ["Training", "Support Ticket"]:
                possible_pain_points = ["Complex Onboarding", "Technical Issues", "Poor Support Response", "User Experience"]
            elif touchpoint in ["Product Update", "Demo"]:
                possible_pain_points = ["Feature Gaps", "User Experience"]
            elif touchpoint == "QBR":
                possible_pain_points = ["Billing Issues", "Feature Gaps"]
            else:
                possible_pain_points = [None]
            
            pain_point = random.choice(possible_pain_points)
            
            # Generate emotion based on touchpoint and pain point
            if pain_point:
                emotion = random.choice(["Frustrated", "Confused", "Dissatisfied", "Neutral"])
            else:
                emotion = random.choice(["Satisfied", "Neutral", "Delighted", "Impressed"])
            
            # Generate NPS, CSAT, and CES based on emotion
            if emotion == "Delighted":
                nps = random.randint(9, 10)
                csat = random.uniform(4.5, 5.0)
                ces = random.uniform(1.0, 2.0)
            elif emotion == "Impressed":
                nps = random.randint(7, 9)
                csat = random.uniform(4.0, 4.5)
                ces = random.uniform(1.5, 2.5)
            elif emotion == "Satisfied":
                nps = random.randint(7, 8)
                csat = random.uniform(3.5, 4.0)
                ces = random.uniform(2.0, 3.0)
            elif emotion == "Neutral":
                nps = random.randint(5, 7)
                csat = random.uniform(3.0, 3.5)
                ces = random.uniform(2.5, 3.5)
            elif emotion == "Dissatisfied":
                nps = random.randint(3, 5)
                csat = random.uniform(2.0, 3.0)
                ces = random.uniform(3.5, 4.5)
            elif emotion == "Confused":
                nps = random.randint(3, 6)
                csat = random.uniform(2.5, 3.5)
                ces = random.uniform(3.0, 4.0)
            else:  # Frustrated
                nps = random.randint(0, 3)
                csat = random.uniform(1.0, 2.0)
                ces = random.uniform(4.0, 5.0)
            
            # Add to interactions data
            interactions_data.append({
                "interaction_id": len(interactions_data) + 1,
                "customer_id": customer["customer_id"],
                "company_name": customer["company_name"],
                "industry": customer["industry"],
                "segment": customer["segment"],
                "interaction_date": interaction_date,
                "journey_stage": stage,
                "touchpoint": touchpoint,
                "persona": persona,
                "pain_point": pain_point,
                "emotion": emotion,
                "nps": nps,
                "csat": csat,
                "ces": ces
            })
    
    # Create interactions dataframe
    interactions_df = pd.DataFrame(interactions_data)
    
    # Generate improvement suggestions
    improvements_data = []
    
    # Group pain points by frequency
    pain_point_counts = interactions_df[interactions_df["pain_point"].notna()].groupby("pain_point").size().reset_index(name="count")
    pain_point_counts = pain_point_counts.sort_values("count", ascending=False)
    
    for i, row in pain_point_counts.iterrows():
        pain_point = row["pain_point"]
        count = row["count"]
        
        # Only generate improvements for pain points that occur frequently
        if count >= 5:
            # Generate 1-3 improvement suggestions per pain point
            for j in range(random.randint(1, 3)):
                if pain_point == "Unclear Pricing":
                    suggestion = random.choice([
                        "Create interactive pricing calculator",
                        "Develop clearer pricing documentation",
                        "Train sales team on pricing discussion"
                    ])
                    impact = "Reduced sales cycle by 15%"
                elif pain_point == "Long Sales Cycle":
                    suggestion = random.choice([
                        "Implement guided demo process",
                        "Develop ROI calculator",
                        "Create simplified purchase path"
                    ])
                    impact = "Increased conversion rate by 12%"
                elif pain_point == "Complex Onboarding":
                    suggestion = random.choice([
                        "Develop step-by-step onboarding checklist",
                        "Create video tutorials for key features",
                        "Assign dedicated onboarding specialist"
                    ])
                    impact = "Reduced time-to-value by 30%"
                elif pain_point == "Technical Issues":
                    suggestion = random.choice([
                        "Improve error messaging",
                        "Create self-service troubleshooting guide",
                        "Develop proactive monitoring system"
                    ])
                    impact = "Reduced support tickets by 25%"
                elif pain_point == "Poor Support Response":
                    suggestion = random.choice([
                        "Implement SLA tracking system",
                        "Expand support team for key regions",
                        "Create tier-based support system"
                    ])
                    impact = "Improved response time by 40%"
                elif pain_point == "Feature Gaps":
                    suggestion = random.choice([
                        "Develop roadmap communication process",
                        "Create workaround documentation",
                        "Implement feature request voting system"
                    ])
                    impact = "Increased feature satisfaction by 20%"
                elif pain_point == "Contract Complexity":
                    suggestion = random.choice([
                        "Develop simplified contract templates",
                        "Create contract explainer videos",
                        "Implement digital signing process"
                    ])
                    impact = "Reduced contract signing time by 35%"
                elif pain_point == "Billing Issues":
                    suggestion = random.choice([
                        "Improve invoice clarity",
                        "Develop self-service billing portal",
                        "Create billing FAQ documentation"
                    ])
                    impact = "Reduced billing inquiries by 30%"
                else:  # User Experience
                    suggestion = random.choice([
                        "Conduct UX testing with key personas",
                        "Simplify navigation structure",
                        "Improve UI for common tasks"
                    ])
                    impact = "Increased user satisfaction by 25%"
                
                # Determine implementation status
                status = random.choice(["Planned", "In Progress", "Completed", "Not Started"])
                
                # Add to improvements data
                improvements_data.append({
                    "improvement_id": len(improvements_data) + 1,
                    "pain_point": pain_point,
                    "frequency": count,
                    "suggestion": suggestion,
                    "status": status,
                    "impact": impact
                })
    
    # Create improvements dataframe
    improvements_df = pd.DataFrame(improvements_data)
    
    return customers_df, interactions_df, improvements_df

# Load or generate data
@st.cache_data
def load_data():
    return generate_synthetic_data()

customers_df, interactions_df, improvements_df = load_data()

# Helper function to provide recommendations based on pain point
def get_recommendation_for_pain_point(pain_point):
    recommendations = {
        "Unclear Pricing": "Implement transparent pricing structures and provide detailed breakdowns of costs.",
        "Long Sales Cycle": "Streamline the sales process and provide clear milestones for progression.",
        "Complex Onboarding": "Develop simplified onboarding workflows and provide better documentation.",
        "Technical Issues": "Increase technical support resources and implement proactive monitoring.",
        "Poor Support Response": "Improve response times and develop a tiered support system.",
        "Feature Gaps": "Create a roadmap for feature development based on customer needs.",
        "Contract Complexity": "Simplify contract language and provide guided walkthroughs.",
        "Billing Issues": "Improve invoice clarity and develop self-service billing tools.",
        "User Experience": "Conduct UX testing and simplify interface design."
    }
    
    return recommendations.get(pain_point, "Investigate this pain point further to develop targeted solutions.")

# Create a text-based loading screen
def loading_screen():
    st.markdown("""
    <div style="text-align: center; margin-top: 20vh;">
        <div style="font-family: 'VT323', monospace; font-size: 48px; color: #00ffff; text-shadow: 2px 2px 0px #ff0066; margin-bottom: 30px;">
            LOADING ZETRA CUSTOMER JOURNEY
        </div>
        <div style="font-family: 'Space Mono', monospace; font-size: 18px; color: #ffffff; margin-bottom: 20px;" id="loading-text">
            Initializing retro gaming experience...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple text-based loading animation
    loading_text = [
        "Initializing retro gaming experience...",
        "Loading customer data...",
        "Processing journey maps...",
        "Calculating metrics...",
        "Generating text reports...",
        "Preparing dashboard..."
    ]
    
    for i, text in enumerate(loading_text):
        time.sleep(0.5)  # Reduced time for faster loading
        progress = (i + 1) / len(loading_text)
        
        # Create a text-based progress bar
        bar_length = 50
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        st.markdown(f"""
        <div style="text-align: center; font-family: 'Space Mono', monospace; color: #ffffff;">
            {text}<br><br>
            <div style="color: #00ffff;">[{bar}] {int(progress * 100)}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    time.sleep(0.5)  # Reduced time for faster loading
    
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <div style="display: inline-block; background-color: #ff0066; color: #ffffff; font-family: 'VT323', monospace; font-size: 24px; padding: 10px 30px; border: 2px solid #00ffff;">
            GAME LOADED! PRESS START
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(0.5)  # Reduced time for faster loading
    st.session_state.loading_complete = True
    st.rerun()

# Overview section with text-based displays
def show_overview():
    # Main overview section with text-based presentation
    st.markdown('<div class="section-header">DASHBOARD OVERVIEW</div>', unsafe_allow_html=True)
    
    # Key metrics in text-based display
    col1, col2 = st.columns(2)
    
    with col1:
        total_customers = len(customers_df)
        avg_nps = round(interactions_df["nps"].mean(), 1)
        
        st.markdown(f'''
        <div class="text-metric">
            <div class="text-metric-label">TOTAL CUSTOMERS</div>
            <div class="text-metric-value">{total_customers}</div>
        </div>
        
        <div class="text-metric">
            <div class="text-metric-label">AVERAGE NPS</div>
            <div class="text-metric-value">{avg_nps}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        avg_csat = round(interactions_df["csat"].mean(), 1)
        total_value = round(customers_df["contract_value"].sum() / 1000000, 1)
        
        st.markdown(f'''
        <div class="text-metric">
            <div class="text-metric-label">AVERAGE CSAT</div>
            <div class="text-metric-value">{avg_csat}/5</div>
        </div>
        
        <div class="text-metric">
            <div class="text-metric-label">TOTAL VALUE</div>
            <div class="text-metric-value">${total_value}M</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Customer segments as text-based table
    st.markdown('<div class="section-header">CUSTOMER SEGMENTS</div>', unsafe_allow_html=True)
    
    # Get segment data
    segment_counts = customers_df["segment"].value_counts().reset_index()
    segment_counts.columns = ["segment", "count"]
    
    # Calculate percentages
    total = segment_counts["count"].sum()
    segment_counts["percentage"] = segment_counts["count"] / total * 100
    
    # Sort by count
    segment_counts = segment_counts.sort_values("count", ascending=False)
    
    # Create text-based table
    segment_table = '<div class="terminal"><table class="text-table">'
    segment_table += '<tr><th>SEGMENT</th><th>COUNT</th><th>PERCENTAGE</th><th>REPRESENTATION</th></tr>'
    
    for _, row in segment_counts.iterrows():
        # Create simple text-based bar
        bar_length = int(row["percentage"] / 5)  # 5% = 1 character
        text_bar = '█' * bar_length
        
        segment_table += f'''
        <tr>
            <td>{row["segment"]}</td>
            <td>{row["count"]}</td>
            <td>{row["percentage"]:.1f}%</td>
            <td>{text_bar}</td>
        </tr>
        '''
    
    segment_table += '</table></div>'
    st.markdown(segment_table, unsafe_allow_html=True)
    
    # Contract value by segment as text-based display
    segment_values = customers_df.groupby("segment")["contract_value"].sum().reset_index()
    segment_values["contract_value_m"] = segment_values["contract_value"] / 1000000
    segment_values = segment_values.sort_values("contract_value", ascending=False)
    
    st.markdown('<div class="text-display">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 20px; color: #ff0066; margin-bottom: 10px;">CONTRACT VALUE BY SEGMENT</div>', unsafe_allow_html=True)
    
    # Calculate max value for scaling
    max_value = segment_values["contract_value_m"].max()
    
    for _, row in segment_values.iterrows():
        # Calculate percentage of max for bar width
        percentage = (row["contract_value_m"] / max_value) * 100
        
        st.markdown(f'''
        <div class="text-bar">
            <div class="text-bar-label">{row["segment"]}</div>
            <div class="text-bar-visual">
                <div class="text-bar-fill" style="width: {percentage}%;">
                    ${row["contract_value_m"]:.1f}M
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Journey stage distribution as text-based display
    st.markdown('<div class="section-header">JOURNEY STAGE DISTRIBUTION</div>', unsafe_allow_html=True)
    
    # Get journey stage data
    journey_order = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
    stage_counts = customers_df["current_stage"].value_counts().reset_index()
    stage_counts.columns = ["stage", "count"]
    
    # Sort by journey progression
    stage_counts['order'] = stage_counts['stage'].apply(lambda x: journey_order.index(x) if x in journey_order else 999)
    stage_counts = stage_counts.sort_values('order')
    
    # Create ASCII journey map
    journey_map = '<div class="ascii-art">'
    journey_map += '  CUSTOMER JOURNEY FLOW\n'
    journey_map += '  -------------------\n\n'
    
    total = stage_counts["count"].sum()
    
    for _, row in stage_counts.iterrows():
        percentage = (row["count"] / total) * 100
        bar_length = int(percentage / 2)  # Scale to fit
        
        journey_map += f'  {row["stage"].ljust(15)} | {("█" * bar_length)} {row["count"]} ({percentage:.1f}%)\n'
    
    journey_map += '\n  -------------------\n'
    journey_map += '  TOTAL CUSTOMERS: ' + str(total)
    journey_map += '</div>'
    
    st.markdown(journey_map, unsafe_allow_html=True)
    
    # Top pain points as text-based display
    st.markdown('<div class="section-header">TOP PAIN POINTS</div>', unsafe_allow_html=True)
    
    # Get pain point data
    pain_point_counts = interactions_df[interactions_df["pain_point"].notna()].groupby("pain_point").size().reset_index(name="count")
    pain_point_counts = pain_point_counts.sort_values("count", ascending=False).head(5)  # Top 5 pain points
    
    # Create alert boxes for top pain points
    for i, row in pain_point_counts.iterrows():
        impact_level = "HIGH" if i < 2 else ("MEDIUM" if i < 4 else "LOW")
        
        st.markdown(f'''
        <div class="alert-box">
            <div class="alert-title">{i+1}. {row["pain_point"].upper()} - FREQUENCY: {row["count"]} - IMPACT: {impact_level}</div>
            <div class="alert-content">
                This pain point affects customer satisfaction and retention. 
                {get_recommendation_for_pain_point(row["pain_point"])}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Simple CX health indicator
    avg_nps = round(interactions_df["nps"].mean(), 1)
    avg_csat = round(interactions_df["csat"].mean(), 1)
    cx_health_score = (avg_nps / 10 * 0.5) + (avg_csat / 5 * 0.5)  # Scale to 0-1
    cx_health_percentage = cx_health_score * 100
    
    st.markdown('<div class="section-header">CX HEALTH INDICATOR</div>', unsafe_allow_html=True)
    
    # Create text-based health meter
    health_level = "EXCELLENT" if cx_health_percentage >= 80 else ("GOOD" if cx_health_percentage >= 60 else ("AVERAGE" if cx_health_percentage >= 40 else ("POOR" if cx_health_percentage >= 20 else "CRITICAL")))
    
    st.markdown(f'''
    <div class="terminal">
        <div style="margin-bottom: 10px; font-size: 18px;">OVERALL CUSTOMER EXPERIENCE HEALTH: {health_level}</div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {cx_health_percentage}%;">{cx_health_percentage:.1f}%</div>
        </div>
        <div style="margin-top: 15px;">
            <span class="terminal-highlight">►</span> NPS Score: {avg_nps}/10<br>
            <span class="terminal-highlight">►</span> CSAT Score: {avg_csat}/5<br>
            <span class="terminal-highlight">►</span> Top Pain Point: {pain_point_counts.iloc[0]["pain_point"] if not pain_point_counts.empty else "None identified"}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Journey Map section with text-based displays
def show_journey_map():
    st.markdown('<div class="section-header">CUSTOMER JOURNEY MAP</div>', unsafe_allow_html=True)
    
    # Filter controls in text-based format
    st.markdown('''
    <div class="terminal" style="margin-bottom: 20px;">
        <div style="color: #ff0066; font-family: 'VT323', monospace; font-size: 20px; margin-bottom: 10px;">FILTER SELECTION</div>
        <div class="terminal-text">
            <span class="terminal-highlight">SELECT SEGMENT:</span> All
            <span class="terminal-highlight">SELECT INDUSTRY:</span> All
            <span class="terminal-highlight">SELECT PERSONA:</span> All
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Get journey stage data
    journey_order = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
    filtered_interactions = interactions_df.copy()
    
    # Create ASCII art journey map
    st.markdown('<div class="section-header">JOURNEY FLOW VISUALIZATION</div>', unsafe_allow_html=True)
    
    # Count transitions between stages
    customer_journeys = filtered_interactions.sort_values(["customer_id", "interaction_date"])
    journey_flows = []
    
    for customer_id in customer_journeys["customer_id"].unique():
        customer_stages = customer_journeys[customer_journeys["customer_id"] == customer_id]["journey_stage"].tolist()
        
        for i in range(len(customer_stages) - 1):
            source = customer_stages[i]
            target = customer_stages[i + 1]
            
            if source != target:  # Only count transitions between different stages
                journey_flows.append((source, target))
    
    # Count frequencies of each transition
    flow_counts = {}
    for source, target in journey_flows:
        if (source, target) in flow_counts:
            flow_counts[(source, target)] += 1
        else:
            flow_counts[(source, target)] = 1
    
    # Sort by frequency
    sorted_flows = sorted(flow_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Create ASCII art for journey flow
    journey_flow_art = '<div class="ascii-art">'
    journey_flow_art += '  TOP JOURNEY TRANSITIONS\n'
    journey_flow_art += '  ---------------------\n\n'
    
    for (source, target), count in sorted_flows[:10]:  # Show top 10 transitions
        arrow_length = min(40, count)
        journey_flow_art += f'  {source.ljust(15)} → {target.ljust(15)} {"=" * arrow_length}> {count}\n'
    
    journey_flow_art += '</div>'
    
    st.markdown(journey_flow_art, unsafe_allow_html=True)
    
    # Journey metrics as text table
    st.markdown('<div class="section-header">JOURNEY STAGE METRICS</div>', unsafe_allow_html=True)
    
    # Calculate metrics by journey stage
    stage_metrics = filtered_interactions.groupby("journey_stage").agg({
        "nps": "mean",
        "csat": "mean",
        "ces": "mean",
        "customer_id": "count"
    }).reset_index()
    
    # Round metrics
    stage_metrics["nps"] = stage_metrics["nps"].round(1)
    stage_metrics["csat"] = stage_metrics["csat"].round(1)
    stage_metrics["ces"] = stage_metrics["ces"].round(1)
    stage_metrics.rename(columns={"customer_id": "count"}, inplace=True)
    
    # Sort by journey order
    stage_metrics['order'] = stage_metrics['journey_stage'].apply(lambda x: journey_order.index(x) if x in journey_order else 999)
    stage_metrics = stage_metrics.sort_values('order')
    stage_metrics = stage_metrics.drop('order', axis=1)
    
    # Create text-based table
    metrics_table = '<div class="terminal"><table class="text-table">'
    metrics_table += '<tr><th>JOURNEY STAGE</th><th>NPS</th><th>CSAT</th><th>CES</th><th>COUNT</th></tr>'
    
    for _, row in stage_metrics.iterrows():
        # Color coding based on NPS
        nps_color = "#00ff66" if row["nps"] >= 7 else ("#ffcc00" if row["nps"] >= 5 else "#ff0066")
        csat_color = "#00ff66" if row["csat"] >= 4 else ("#ffcc00" if row["csat"] >= 3 else "#ff0066")
        ces_color = "#00ff66" if row["ces"] <= 2 else ("#ffcc00" if row["ces"] <= 3 else "#ff0066")
        
        metrics_table += f'''
        <tr>
            <td>{row["journey_stage"]}</td>
            <td style="color: {nps_color};">{row["nps"]}</td>
            <td style="color: {csat_color};">{row["csat"]}</td>
            <td style="color: {ces_color};">{row["ces"]}</td>
            <td>{row["count"]}</td>
        </tr>
        '''
    
    metrics_table += '</table></div>'
    st.markdown(metrics_table, unsafe_allow_html=True)
    
    # Touchpoint analysis
    st.markdown('<div class="section-header">TOUCHPOINT ANALYSIS</div>', unsafe_allow_html=True)
    
    # Count touchpoints by journey stage
    touchpoint_counts = filtered_interactions.groupby(['touchpoint', 'journey_stage']).size().reset_index(name='count')
    
    # Create a pivot table
    pivot_data = {}
    for _, row in touchpoint_counts.iterrows():
        touchpoint = row['touchpoint']
        stage = row['journey_stage']
        count = row['count']
        
        if touchpoint not in pivot_data:
            pivot_data[touchpoint] = {'total': 0}
        
        pivot_data[touchpoint][stage] = count
        pivot_data[touchpoint]['total'] += count
    
    # Sort touchpoints by total count
    sorted_touchpoints = sorted(pivot_data.keys(), key=lambda x: pivot_data[x]['total'], reverse=True)
    
    # Create text-based representation
    touchpoint_table = '<div class="terminal"><table class="text-table">'
    touchpoint_table += '<tr><th>TOUCHPOINT</th>'
    
    # Add columns for each stage
    for stage in journey_order:
        touchpoint_table += f'<th>{stage}</th>'
    
    touchpoint_table += '<th>TOTAL</th></tr>'
    
    # Add rows for each touchpoint
    for touchpoint in sorted_touchpoints:
        touchpoint_table += f'<tr><td>{touchpoint}</td>'
        
        total = pivot_data[touchpoint]['total']
        
        for stage in journey_order:
            value = pivot_data[touchpoint].get(stage, 0)
            
            # Use symbols to represent frequency
            if value == 0:
                symbol = '-'
            elif value < 5:
                symbol = '•'
            elif value < 10:
                symbol = '••'
            elif value < 20:
                symbol = '•••'
            else:
                symbol = '••••'
            
            touchpoint_table += f'<td title="{value}">{symbol} {value}</td>'
        
        touchpoint_table += f'<td>{total}</td></tr>'
    
    touchpoint_table += '</table></div>'
    st.markdown(touchpoint_table, unsafe_allow_html=True)
    
    # Persona journey analysis
    st.markdown('<div class="section-header">PERSONA JOURNEY ANALYSIS</div>', unsafe_allow_html=True)
    
    # Create text representation of persona involvement
    persona_counts = filtered_interactions.groupby('persona')['customer_id'].count().reset_index()
    persona_counts.columns = ['persona', 'count']
    persona_counts = persona_counts.sort_values('count', ascending=False)
    
    # ASCII visualization
    persona_vis = '<div class="ascii-art">'
    persona_vis += '  PERSONA INVOLVEMENT\n'
    persona_vis += '  ------------------\n\n'
    
    max_count = persona_counts['count'].max()
    
    for _, row in persona_counts.iterrows():
        bar_length = int(30 * (row['count'] / max_count))
        persona_vis += f'  {row["persona"].ljust(15)} | {("█" * bar_length)} {row["count"]}\n'
    
    persona_vis += '\n  KEY INSIGHTS:\n'
    persona_vis += '  • ' + persona_counts.iloc[0]['persona'] + ' has the highest involvement\n'
    persona_vis += '  • Technical users primarily engage during Onboarding and Usage stages\n'
    persona_vis += '  • Decision Makers are most active in Consideration and Renewal phases\n'
    persona_vis += '</div>'
    
    st.markdown(persona_vis, unsafe_allow_html=True)

# CX Metrics section with text-based displays
def show_cx_metrics():
    st.markdown('<div class="section-header">CUSTOMER EXPERIENCE METRICS</div>', unsafe_allow_html=True)
    
    # Filter controls in text-based format
    st.markdown('''
    <div class="terminal" style="margin-bottom: 20px;">
        <div style="color: #ff0066; font-family: 'VT323', monospace; font-size: 20px; margin-bottom: 10px;">METRIC FILTERS</div>
        <div class="terminal-text">
            <span class="terminal-highlight">SELECT SEGMENT:</span> All
            <span class="terminal-highlight">SELECT INDUSTRY:</span> All
            <span class="terminal-highlight">DATE RANGE:</span> All Time
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Display NPS, CSAT, and CES over time as text-based
    st.markdown('<div class="section-header">CX METRICS OVER TIME</div>', unsafe_allow_html=True)
    
    # Group metrics by month for trending
    filtered_interactions = interactions_df.copy()
    filtered_interactions["month"] = filtered_interactions["interaction_date"].dt.to_period("M")
    
    metrics_over_time = filtered_interactions.groupby("month").agg({
        "nps": "mean",
        "csat": "mean",
        "ces": "mean"
    }).reset_index()
    
    # Convert period to datetime for display
    metrics_over_time["month"] = metrics_over_time["month"].dt.to_timestamp().dt.strftime('%b %Y')
    
    # Round values
    metrics_over_time["nps"] = metrics_over_time["nps"].round(1)
    metrics_over_time["csat"] = metrics_over_time["csat"].round(1)
    metrics_over_time["ces"] = metrics_over_time["ces"].round(1)
    
    # Create ASCII chart for metrics over time
    time_series = '<div class="ascii-art">'
    time_series += '  METRIC TRENDS OVER TIME\n'
    time_series += '  ----------------------\n\n'
    time_series += '  Month       | NPS   | CSAT  | CES   |\n'
    time_series += '  ------------|-------|-------|-------|\n'
    
    for _, row in metrics_over_time.iterrows():
        # Format month
        month = row["month"]
        
        # Format metrics with indicators
        nps_trend = "↑" if row["nps"] > metrics_over_time["nps"].mean() else ("↓" if row["nps"] < metrics_over_time["nps"].mean() else "→")
        csat_trend = "↑" if row["csat"] > metrics_over_time["csat"].mean() else ("↓" if row["csat"] < metrics_over_time["csat"].mean() else "→")
        ces_trend = "↓" if row["ces"] < metrics_over_time["ces"].mean() else ("↑" if row["ces"] > metrics_over_time["ces"].mean() else "→")  # Lower CES is better
        
        time_series += f'  {month.ljust(12)}| {row["nps"]} {nps_trend} | {row["csat"]} {csat_trend} | {row["ces"]} {ces_trend} |\n'
    
    time_series += '</div>'
    
    st.markdown(time_series, unsafe_allow_html=True)
    
    # NPS distribution as text-based display
    st.markdown('<div class="section-header">NPS DISTRIBUTION</div>', unsafe_allow_html=True)
    
    # Calculate NPS categories
    filtered_interactions["nps_category"] = pd.cut(
        filtered_interactions["nps"],
        bins=[-1, 6, 8, 10],
        labels=["Detractor", "Passive", "Promoter"]
    )
    
    # Count NPS categories
    nps_counts = filtered_interactions["nps_category"].value_counts().reset_index()
    nps_counts.columns = ["category", "count"]
    
    # Calculate NPS score
    total = nps_counts["count"].sum()
    promoters = nps_counts[nps_counts["category"] == "Promoter"]["count"].iloc[0] if "Promoter" in nps_counts["category"].values else 0
    detractors = nps_counts[nps_counts["category"] == "Detractor"]["count"].iloc[0] if "Detractor" in nps_counts["category"].values else 0
    
    nps_score = int(((promoters - detractors) / total) * 100)
    
    # Create text-based NPS visualization
    nps_vis = '<div class="terminal">'
    nps_vis += f'<div style="font-size: 24px; margin-bottom: 15px;">NPS SCORE: <span style="color: {"#00ff66" if nps_score >= 40 else "#ffcc00" if nps_score >= 0 else "#ff0066"}">{nps_score}</span></div>'
    
    # Create distribution bars
    for category in ["Detractor", "Passive", "Promoter"]:
        if category in nps_counts["category"].values:
            count = nps_counts[nps_counts["category"] == category]["count"].iloc[0]
            percentage = (count / total) * 100
            bar_length = int(percentage / 2)  # Scale to fit
            
            # Color coding
            color = "#ff0066" if category == "Detractor" else ("#ffcc00" if category == "Passive" else "#00ff66")
            
            nps_vis += f'<div style="margin: 10px 0;">'
            nps_vis += f'<div style="margin-bottom: 5px;"><span style="color: {color};">{category}</span>: {count} ({percentage:.1f}%)</div>'
            nps_vis += f'<div style="background-color: #1e1e2f; width: 100%; height: 20px; border: 1px solid #00ffff;">'
            nps_vis += f'<div style="background-color: {color}; height: 100%; width: {percentage}%"></div>'
            nps_vis += '</div></div>'
    
    nps_vis += '<div style="margin-top: 15px; font-style: italic; color: #ffffff;">'
    nps_vis += 'NPS = % Promoters - % Detractors<br>'
    nps_vis += f'NPS = {(promoters/total*100):.1f}% - {(detractors/total*100):.1f}% = {nps_score}'
    nps_vis += '</div>'
    
    nps_vis += '</div>'
    
    st.markdown(nps_vis, unsafe_allow_html=True)
    
    # Display CX metrics by segment and journey stage as text tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">CX METRICS BY SEGMENT</div>', unsafe_allow_html=True)
        
        # Calculate metrics by segment
        segment_metrics = filtered_interactions.groupby("segment").agg({
            "nps": "mean",
            "csat": "mean",
            "ces": "mean"
        }).reset_index()
        
        # Round values
        segment_metrics["nps"] = segment_metrics["nps"].round(1)
        segment_metrics["csat"] = segment_metrics["csat"].round(1)
        segment_metrics["ces"] = segment_metrics["ces"].round(1)
        
        # Sort by NPS
        segment_metrics = segment_metrics.sort_values("nps", ascending=False)
        
        # Create text-based table
        segment_table = '<div class="terminal"><table class="text-table">'
        segment_table += '<tr><th>SEGMENT</th><th>NPS</th><th>CSAT</th><th>CES</th></tr>'
        
        for _, row in segment_metrics.iterrows():
            # Color coding based on metrics
            nps_color = "#00ff66" if row["nps"] >= 7 else ("#ffcc00" if row["nps"] >= 5 else "#ff0066")
            csat_color = "#00ff66" if row["csat"] >= 4 else ("#ffcc00" if row["csat"] >= 3 else "#ff0066")
            ces_color = "#00ff66" if row["ces"] <= 2 else ("#ffcc00" if row["ces"] <= 3 else "#ff0066")
            
            segment_table += f'''
            <tr>
                <td>{row["segment"]}</td>
                <td style="color: {nps_color};">{row["nps"]}</td>
                <td style="color: {csat_color};">{row["csat"]}</td>
                <td style="color: {ces_color};">{row["ces"]}</td>
            </tr>
            '''
        
        segment_table += '</table></div>'
        st.markdown(segment_table, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">CX METRICS BY JOURNEY STAGE</div>', unsafe_allow_html=True)
        
        # Calculate metrics by journey stage
        journey_order = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
        stage_metrics = filtered_interactions.groupby("journey_stage").agg({
            "nps": "mean",
            "csat": "mean",
            "ces": "mean"
        }).reset_index()
        
        # Round values
        stage_metrics["nps"] = stage_metrics["nps"].round(1)
        stage_metrics["csat"] = stage_metrics["csat"].round(1)
        stage_metrics["ces"] = stage_metrics["ces"].round(1)
        
        # Sort by journey progression
        stage_metrics['order'] = stage_metrics['journey_stage'].apply(lambda x: journey_order.index(x) if x in journey_order else 999)
        stage_metrics = stage_metrics.sort_values('order')
        stage_metrics = stage_metrics.drop('order', axis=1)
        
        # Create text-based table
        stage_table = '<div class="terminal"><table class="text-table">'
        stage_table += '<tr><th>JOURNEY STAGE</th><th>NPS</th><th>CSAT</th><th>CES</th></tr>'
        
        for _, row in stage_metrics.iterrows():
            # Color coding based on metrics
            nps_color = "#00ff66" if row["nps"] >= 7 else ("#ffcc00" if row["nps"] >= 5 else "#ff0066")
            csat_color = "#00ff66" if row["csat"] >= 4 else ("#ffcc00" if row["csat"] >= 3 else "#ff0066")
            ces_color = "#00ff66" if row["ces"] <= 2 else ("#ffcc00" if row["ces"] <= 3 else "#ff0066")
            
            stage_table += f'''
            <tr>
                <td>{row["journey_stage"]}</td>
                <td style="color: {nps_color};">{row["nps"]}</td>
                <td style="color: {csat_color};">{row["csat"]}</td>
                <td style="color: {ces_color};">{row["ces"]}</td>
            </tr>
            '''
        
        stage_table += '</table></div>'
        st.markdown(stage_table, unsafe_allow_html=True)
    
    # Customer emotions analysis
    st.markdown('<div class="section-header">CUSTOMER EMOTIONS</div>', unsafe_allow_html=True)
    
    # Count emotions
    emotion_counts = filtered_interactions["emotion"].value_counts().reset_index()
    emotion_counts.columns = ["emotion", "count"]
    
    # Calculate percentages
    total = emotion_counts["count"].sum()
    emotion_counts["percentage"] = emotion_counts["count"] / total * 100
    
    # Sort by count
    emotion_counts = emotion_counts.sort_values("count", ascending=False)
    
    # Create text-based emotion visualization
    emotion_vis = '<div class="terminal">'
    emotion_vis += '<div style="margin-bottom: 15px;">CUSTOMER EMOTION DISTRIBUTION</div>'
    
    # Define emotion symbols and colors
    emotion_symbols = {
        "Delighted": "😄 #00ff66",
        "Impressed": "🙂 #00ffff",
        "Satisfied": "😐 #ffcc00",
        "Neutral": "😶 #ffffff",
        "Dissatisfied": "🙁 #ff9900",
        "Confused": "😕 #cc66ff",
        "Frustrated": "😠 #ff0066"
    }
    
    for _, row in emotion_counts.iterrows():
        emotion = row["emotion"]
        count = row["count"]
        percentage = row["percentage"]
        
        # Get symbol and color
        symbol, color = emotion_symbols.get(emotion, "• #ffffff").split(" ")
        
        # Create bar
        bar_length = int(percentage)
        
        emotion_vis += f'<div style="margin: 10px 0;">'
        emotion_vis += f'<div style="margin-bottom: 5px;"><span style="color: {color};">{symbol} {emotion}</span>: {count} ({percentage:.1f}%)</div>'
        emotion_vis += f'<div style="background-color: #1e1e2f; width: 100%; height: 20px; border: 1px solid #00ffff;">'
        emotion_vis += f'<div style="background-color: {color}; height: 100%; width: {percentage}%"></div>'
        emotion_vis += '</div></div>'
    
    emotion_vis += '</div>'
    
    st.markdown(emotion_vis, unsafe_allow_html=True)

# Friction Points section with text-based displays
def show_friction_points():
    st.markdown('<div class="section-header">FRICTION POINT ANALYSIS</div>', unsafe_allow_html=True)
    
    # Filter controls in text-based format
    st.markdown('''
    <div class="terminal" style="margin-bottom: 20px;">
        <div style="color: #ff0066; font-family: 'VT323', monospace; font-size: 20px; margin-bottom: 10px;">FRICTION FILTERS</div>
        <div class="terminal-text">
            <span class="terminal-highlight">SELECT JOURNEY STAGE:</span> All
            <span class="terminal-highlight">SELECT TOUCHPOINT:</span> All
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Pain point frequency analysis
    st.markdown('<div class="section-header">PAIN POINT FREQUENCY</div>', unsafe_allow_html=True)
    
    # Filter and count pain points
    filtered_interactions = interactions_df.copy()
    filtered_interactions = filtered_interactions[filtered_interactions["pain_point"].notna()]
    
    pain_point_counts = filtered_interactions["pain_point"].value_counts().reset_index()
    pain_point_counts.columns = ["pain_point", "count"]
    pain_point_counts = pain_point_counts.sort_values("count", ascending=False)
    
    # Create text-based visualization
    pain_point_vis = '<div class="terminal">'
    pain_point_vis += '<div style="margin-bottom: 15px;">PAIN POINT FREQUENCY ANALYSIS</div>'
    
    # Calculate max for scaling
    max_count = pain_point_counts["count"].max()
    
    for _, row in pain_point_counts.iterrows():
        percentage = (row["count"] / max_count) * 100
        bar_length = int(percentage / 2)  # Scale to fit
        
        pain_point_vis += f'<div style="margin: 10px 0;">'
        pain_point_vis += f'<div style="margin-bottom: 5px;">{row["pain_point"]}: {row["count"]}</div>'
        pain_point_vis += f'<div style="background-color: #1e1e2f; width: 100%; height: 20px; border: 1px solid #00ffff;">'
        pain_point_vis += f'<div style="background-color: #ff0066; height: 100%; width: {percentage}%"></div>'
        pain_point_vis += '</div></div>'
    
    pain_point_vis += '</div>'
    
    st.markdown(pain_point_vis, unsafe_allow_html=True)
    
    # Pain point impact analysis
    st.markdown('<div class="section-header">PAIN POINT IMPACT</div>', unsafe_allow_html=True)
    
    # Calculate average NPS, CSAT, and CES for each pain point
    pain_point_impact = filtered_interactions.groupby("pain_point").agg({
        "nps": "mean",
        "csat": "mean",
        "ces": "mean",
        "customer_id": "count"
    }).reset_index()
    
    pain_point_impact.columns = ["pain_point", "avg_nps", "avg_csat", "avg_ces", "frequency"]
    
    # Calculate impact score (lower NPS and CSAT, higher CES, and higher frequency mean higher impact)
    pain_point_impact["impact_score"] = (
        (10 - pain_point_impact["avg_nps"]) * 0.3 +
        (5 - pain_point_impact["avg_csat"]) * 0.3 +
        pain_point_impact["avg_ces"] * 0.2 +
        pain_point_impact["frequency"] * 0.2
    )
    
    # Round values
    pain_point_impact["avg_nps"] = pain_point_impact["avg_nps"].round(1)
    pain_point_impact["avg_csat"] = pain_point_impact["avg_csat"].round(1)
    pain_point_impact["avg_ces"] = pain_point_impact["avg_ces"].round(1)
    pain_point_impact["impact_score"] = pain_point_impact["impact_score"].round(1)
    
    # Sort by impact score
    pain_point_impact = pain_point_impact.sort_values("impact_score", ascending=False)
    
    # Create text-based table
    impact_table = '<div class="terminal"><table class="text-table">'
    impact_table += '<tr><th>PAIN POINT</th><th>IMPACT</th><th>NPS</th><th>CSAT</th><th>CES</th><th>FREQ</th></tr>'
    
    for _, row in pain_point_impact.iterrows():
        # Color coding based on impact score
        impact_color = "#ff0066" if row["impact_score"] >= 6 else ("#ffcc00" if row["impact_score"] >= 4 else "#00ffff")
        
        impact_table += f'''
        <tr>
            <td>{row["pain_point"]}</td>
            <td style="color: {impact_color};">{row["impact_score"]}</td>
            <td>{row["avg_nps"]}</td>
            <td>{row["avg_csat"]}</td>
            <td>{row["avg_ces"]}</td>
            <td>{row["frequency"]}</td>
        </tr>
        '''
    
    impact_table += '</table></div>'
    st.markdown(impact_table, unsafe_allow_html=True)
    
    # Top pain points breakdown with recommendations
    st.markdown('<div class="section-header">TOP PAIN POINTS WITH RECOMMENDATIONS</div>', unsafe_allow_html=True)
    
    # Display top 3 pain points with detailed analysis
    for i, row in pain_point_impact.head(3).iterrows():
        st.markdown(f'''
        <div class="alert-box">
            <div class="alert-title">{i+1}. {row["pain_point"].upper()} - IMPACT SCORE: {row["impact_score"]}</div>
            <div class="alert-content">
                <p><span style="color: #00ffff;">Metrics</span>: NPS {row["avg_nps"]} | CSAT {row["avg_csat"]} | CES {row["avg_ces"]} | Frequency {row["frequency"]}</p>
                <p><span style="color: #00ffff;">Analysis</span>: This pain point significantly impacts customer satisfaction and retention. 
                It occurs most frequently during the {get_most_common_stage_for_pain_point(row["pain_point"], filtered_interactions)} stage.</p>
                <p><span style="color: #00ffff;">Recommendation</span>: {get_recommendation_for_pain_point(row["pain_point"])}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Pain point by journey stage analysis
    st.markdown('<div class="section-header">PAIN POINTS BY JOURNEY STAGE</div>', unsafe_allow_html=True)
    
    # Count pain points by journey stage
    pain_stage_counts = filtered_interactions.groupby(['journey_stage', 'pain_point']).size().reset_index(name='count')
    
    # Pivot the data
    pivot_data = {}
    journey_order = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
    
    for _, row in pain_stage_counts.iterrows():
        stage = row['journey_stage']
        pain_point = row['pain_point']
        count = row['count']
        
        if stage not in pivot_data:
            pivot_data[stage] = {}
        
        pivot_data[stage][pain_point] = count
    
    # Create text-based heatmap
    heatmap = '<div class="terminal">'
    heatmap += '<div style="margin-bottom: 15px;">PAIN POINT OCCURRENCE BY JOURNEY STAGE</div>'
    
    # Create a table
    heatmap += '<table class="text-table">'
    heatmap += '<tr><th>JOURNEY STAGE</th><th>TOP PAIN POINTS</th></tr>'
    
    # Sort stages by journey order
    sorted_stages = sorted(pivot_data.keys(), key=lambda x: journey_order.index(x) if x in journey_order else 999)
    
    for stage in sorted_stages:
        # Sort pain points by count
        pain_points = sorted(pivot_data[stage].items(), key=lambda x: x[1], reverse=True)
        
        # Format pain points as a list
        pain_point_list = ""
        for pain_point, count in pain_points[:3]:  # Show top 3
            pain_point_list += f'<span style="color: #ff0066;">{pain_point}</span> ({count}), '
        
        pain_point_list = pain_point_list.rstrip(', ')
        
        heatmap += f'<tr><td>{stage}</td><td>{pain_point_list}</td></tr>'
    
    heatmap += '</table>'
    heatmap += '</div>'
    
    st.markdown(heatmap, unsafe_allow_html=True)

# Helper function to get most common stage for a pain point
def get_most_common_stage_for_pain_point(pain_point, filtered_interactions):
    pain_point_data = filtered_interactions[filtered_interactions["pain_point"] == pain_point]
    if pain_point_data.empty:
        return "Unknown"
    
    stage_counts = pain_point_data["journey_stage"].value_counts()
    return stage_counts.index[0] if not stage_counts.empty else "Unknown"

# Improvements section with text-based displays
def show_improvements():
    st.markdown('<div class="section-header">CX IMPROVEMENT INITIATIVES</div>', unsafe_allow_html=True)
    
    # Filter controls in text-based format
    st.markdown('''
    <div class="terminal" style="margin-bottom: 20px;">
        <div style="color: #ff0066; font-family: 'VT323', monospace; font-size: 20px; margin-bottom: 10px;">IMPROVEMENT FILTERS</div>
        <div class="terminal-text">
            <span class="terminal-highlight">SELECT PAIN POINT:</span> All
            <span class="terminal-highlight">SELECT STATUS:</span> All
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Improvement status summary
    st.markdown('<div class="section-header">IMPROVEMENT STATUS SUMMARY</div>', unsafe_allow_html=True)
    
    # Count improvements by status
    status_counts = improvements_df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    
    # Create text-based visualization
    status_vis = '<div class="terminal">'
    status_vis += '<div style="margin-bottom: 15px;">IMPROVEMENT STATUS DISTRIBUTION</div>'
    
    # Calculate total
    total = status_counts["count"].sum()
    
    # Status colors
    status_colors = {
        "Completed": "#00ff66",
        "In Progress": "#ffcc00",
        "Planned": "#00ffff",
        "Not Started": "#ff0066"
    }
    
    for _, row in status_counts.iterrows():
        status = row["status"]
        count = row["count"]
        percentage = (count / total) * 100
        
        # Get color
        color = status_colors.get(status, "#ffffff")
        
        # Create bar
        bar_length = int(percentage)
        
        status_vis += f'<div style="margin: 10px 0;">'
        status_vis += f'<div style="margin-bottom: 5px;"><span style="color: {color};">{status}</span>: {count} ({percentage:.1f}%)</div>'
        status_vis += f'<div style="background-color: #1e1e2f; width: 100%; height: 20px; border: 1px solid #00ffff;">'
        status_vis += f'<div style="background-color: {color}; height: 100%; width: {percentage}%"></div>'
        status_vis += '</div></div>'
    
    status_vis += '</div>'
    
    st.markdown(status_vis, unsafe_allow_html=True)
    
    # Improvements by pain point
    st.markdown('<div class="section-header">IMPROVEMENTS BY PAIN POINT</div>', unsafe_allow_html=True)
    
    # Count improvements by pain point
    pain_point_improvements = improvements_df.groupby("pain_point").size().reset_index(name="count")
    
    # Join with impact data
    filtered_interactions = interactions_df[interactions_df["pain_point"].notna()]
    pain_point_impact = filtered_interactions.groupby("pain_point").agg({
        "nps": "mean",
        "customer_id": "count"
    }).reset_index()
    pain_point_impact.columns = ["pain_point", "avg_nps", "frequency"]
    
    # Merge data
    pain_point_data = pd.merge(pain_point_improvements, pain_point_impact, on="pain_point", how="left")
    
    # Sort by frequency
    pain_point_data = pain_point_data.sort_values("frequency", ascending=False)
    
    # Create text-based table
    pain_point_table = '<div class="terminal"><table class="text-table">'
    pain_point_table += '<tr><th>PAIN POINT</th><th>IMPROVEMENTS</th><th>FREQUENCY</th><th>AVG NPS</th></tr>'
    
    for _, row in pain_point_data.iterrows():
        # Format NPS with color
        nps_value = row["avg_nps"] if not pd.isna(row["avg_nps"]) else 0
        nps_color = "#00ff66" if nps_value >= 7 else ("#ffcc00" if nps_value >= 5 else "#ff0066")
        
        pain_point_table += f'''
        <tr>
            <td>{row["pain_point"]}</td>
            <td>{row["count"]}</td>
            <td>{row["frequency"]}</td>
            <td style="color: {nps_color};">{nps_value:.1f}</td>
        </tr>
        '''
    
    pain_point_table += '</table></div>'
    st.markdown(pain_point_table, unsafe_allow_html=True)
    
    # Improvement details
    st.markdown('<div class="section-header">IMPROVEMENT DETAILS</div>', unsafe_allow_html=True)
    
    # Create detailed table of all improvements
    filtered_improvements = improvements_df.copy()
    
    # Sort by pain point frequency
    pain_point_counts = filtered_interactions.groupby("pain_point").size().reset_index(name="frequency")
    improvements_with_frequency = pd.merge(filtered_improvements, pain_point_counts, on="pain_point", how="left")
    improvements_with_frequency = improvements_with_frequency.sort_values(["frequency", "status"], ascending=[False, True])
    
    # Status indicators
    status_indicators = {
        "Completed": "✓",
        "In Progress": "►",
        "Planned": "⚑",
        "Not Started": "✕"
    }
    
    # Create a card for each improvement
    for i, row in improvements_with_frequency.iterrows():
        # Status color
        status_color = status_colors.get(row["status"], "#ffffff")
        status_indicator = status_indicators.get(row["status"], "•")
        
        st.markdown(f'''
        <div class="alert-box">
            <div class="alert-title">
                <span style="color: {status_color};">[{status_indicator}] {row["status"].upper()}</span>: {row["suggestion"]}
            </div>
            <div class="alert-content">
                <p><span style="color: #00ffff;">Pain Point</span>: {row["pain_point"]} (Frequency: {row["frequency"]})</p>
                <p><span style="color: #00ffff;">Expected Impact</span>: {row["impact"]}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # AI Personalization Recommendations
    st.markdown('<div class="section-header">AI PERSONALIZATION RECOMMENDATIONS</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="terminal">
        <div style="color: #ff0066; font-family: 'VT323', monospace; font-size: 20px; margin-bottom: 15px;">AI-POWERED CX ENHANCEMENT OPPORTUNITIES</div>
        
        <div style="margin: 15px 0; padding-left: 20px; border-left: 3px solid #ff0066;">
            <div style="color: #ff0066; font-weight: bold;">PREDICTIVE CUSTOMER NEEDS</div>
            <div>Implement AI to analyze past behavior and predict when customers are likely to need support, 
            reaching out proactively before issues arise.</div>
        </div>
        
        <div style="margin: 15px 0; padding-left: 20px; border-left: 3px solid #ffcc00;">
            <div style="color: #ffcc00; font-weight: bold;">PERSONALIZED ONBOARDING</div>
            <div>Use AI to customize onboarding paths based on customer segment, industry, and user persona to 
            reduce "Complex Onboarding" pain points.</div>
        </div>
        
        <div style="margin: 15px 0; padding-left: 20px; border-left: 3px solid #00ffff;">
            <div style="color: #00ffff; font-weight: bold;">INTELLIGENT SUPPORT ROUTING</div>
            <div>Develop AI-powered routing system that matches customer issues with the most qualified support agent 
            based on issue type, customer segment, and past interactions.</div>
        </div>
        
        <div style="margin: 15px 0; padding-left: 20px; border-left: 3px solid #00ff66;">
            <div style="color: #00ff66; font-weight: bold;">CUSTOMIZED COMMUNICATION</div>
            <div>Utilize AI to tailor communication frequency, channel, and content based on customer preferences 
            and behavior to enhance engagement during the renewal stage.</div>
        </div>
        
        <div style="text-align: center; margin-top: 20px; font-family: 'VT323', monospace; font-size: 18px; color: #00ffff;">
            [ PRESS SELECT TO IMPLEMENT AI ENHANCEMENTS ]
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Main app function
def main():
    # Title and subtitle with retro gaming style
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-family: 'VT323', monospace; font-size: 48px; color: #00ffff; text-shadow: 2px 2px 0px #ff0066; margin-bottom: 5px; letter-spacing: 2px;">
            ZETRA CUSTOMER JOURNEY
        </div>
        <div style="font-family: 'VT323', monospace; font-size: 28px; color: #ff0066; text-shadow: 1px 1px 0px #00ffff; letter-spacing: 1px;">
            CX OPTIMIZATION DASHBOARD
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create simple text-based tabs with options
    tabs = ["OVERVIEW", "JOURNEY MAP", "CX METRICS", "FRICTION POINTS", "IMPROVEMENTS"]
    
    tab_html = '<div class="nav-menu">'
    for i, tab in enumerate(tabs):
        if i == 0:  # Always make the first tab active for demo
            tab_html += f'<div class="nav-item-active">{tab}</div>'
        else:
            tab_html += f'<div class="nav-item">{tab}</div>'
    tab_html += '</div>'
    
    st.markdown(tab_html, unsafe_allow_html=True)
    
    # Display the Overview section (for demo, we'll always show this)
    show_overview()

# Check if loading is complete
if 'loading_complete' not in st.session_state:
    st.session_state.loading_complete = False
    loading_screen()
    st.stop()

# Run the main function
if __name__ == "__main__":
    main()