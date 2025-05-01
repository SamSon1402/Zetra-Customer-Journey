import pandas as pd
import numpy as np

def calculate_nps_distribution(df):
    """Calculate NPS distribution and overall NPS score"""
    # Calculate NPS categories
    df["nps_category"] = pd.cut(
        df["nps"],
        bins=[-1, 6, 8, 10],
        labels=["Detractor", "Passive", "Promoter"]
    )
    
    # Count NPS categories
    nps_counts = df["nps_category"].value_counts().reset_index()
    nps_counts.columns = ["category", "count"]
    
    # Calculate NPS score
    total = nps_counts["count"].sum()
    promoters = nps_counts[nps_counts["category"] == "Promoter"]["count"].iloc[0] if "Promoter" in nps_counts["category"].values else 0
    detractors = nps_counts[nps_counts["category"] == "Detractor"]["count"].iloc[0] if "Detractor" in nps_counts["category"].values else 0
    
    nps_score = int(((promoters - detractors) / total) * 100)
    
    return nps_counts, nps_score

def get_recommendation_for_pain_point(pain_point):
    """Return recommendation based on pain point type"""
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

def get_most_common_stage_for_pain_point(pain_point, df):
    """Determine which journey stage a pain point most commonly occurs in"""
    pain_point_data = df[df["pain_point"] == pain_point]
    if pain_point_data.empty:
        return "Unknown"
    
    stage_counts = pain_point_data["journey_stage"].value_counts()
    return stage_counts.index[0] if not stage_counts.empty else "Unknown"

def calculate_cx_health_score(df):
    """Calculate overall CX health score based on NPS and CSAT"""
    avg_nps = round(df["nps"].mean(), 1)
    avg_csat = round(df["csat"].mean(), 1)
    
    # Scale metrics to 0-1 range and combine with weights
    cx_health_score = (avg_nps / 10 * 0.5) + (avg_csat / 5 * 0.5)
    cx_health_percentage = cx_health_score * 100
    
    # Determine health level
    if cx_health_percentage >= 80:
        health_level = "EXCELLENT"
    elif cx_health_percentage >= 60:
        health_level = "GOOD"
    elif cx_health_percentage >= 40:
        health_level = "AVERAGE"
    elif cx_health_percentage >= 20:
        health_level = "POOR"
    else:
        health_level = "CRITICAL"
    
    return cx_health_percentage, health_level, avg_nps, avg_csat

def calculate_metrics_by_segment(df):
    """Calculate CX metrics aggregated by customer segment"""
    segment_metrics = df.groupby("segment").agg({
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
    
    return segment_metrics

def calculate_metrics_by_journey_stage(df):
    """Calculate CX metrics aggregated by journey stage"""
    journey_order = ["Awareness", "Consideration", "Purchase", "Onboarding", "Usage", "Renewal", "Advocacy"]
    stage_metrics = df.groupby("journey_stage").agg({
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
    
    return stage_metrics

def calculate_pain_point_impact(df):
    """Calculate impact scores for pain points based on metrics and frequency"""
    # Only include interactions with pain points
    filtered_df = df[df["pain_point"].notna()]
    
    # Calculate average NPS, CSAT, and CES for each pain point
    pain_point_impact = filtered_df.groupby("pain_point").agg({
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
    
    return pain_point_impact