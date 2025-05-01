import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_customer_data(num_customers=200):
    """Generate synthetic customer data"""
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
    
    # Customer data
    customer_data = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 4, 1)
    
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
    return customers_df

def generate_interaction_data(customers_df):
    """Generate synthetic customer interactions based on customer data"""
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
    return interactions_df

def generate_improvement_data(interactions_df):
    """Generate improvement suggestions based on pain points from interactions data"""
    # Only include interactions with pain points
    filtered_interactions = interactions_df[interactions_df["pain_point"].notna()]
    
    # Group pain points by frequency
    pain_point_counts = filtered_interactions.groupby("pain_point").size().reset_index(name="count")
    pain_point_counts = pain_point_counts.sort_values("count", ascending=False)
    
    improvements_data = []
    
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
    return improvements_df

def load_all_data():
    """Load or generate all required data"""
    customers_df = generate_customer_data()
    interactions_df = generate_interaction_data(customers_df)
    improvements_df = generate_improvement_data(interactions_df)
    return customers_df, interactions_df, improvements_df