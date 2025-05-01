def create_ascii_bar(value, max_value, width=40, fill_char='█', empty_char='░'):
    """Create a text-based progress bar"""
    ratio = min(1.0, value / max_value)
    bar_length = int(width * ratio)
    return fill_char * bar_length + empty_char * (width - bar_length)

def create_ascii_journey_map(df, journey_order):
    """Create ASCII art representation of journey stage distribution"""
    stage_counts = df["current_stage"].value_counts().reset_index()
    stage_counts.columns = ["stage", "count"]
    
    # Sort by journey progression
    stage_counts['order'] = stage_counts['stage'].apply(lambda x: journey_order.index(x) if x in journey_order else 999)
    stage_counts = stage_counts.sort_values('order')
    
    total = stage_counts["count"].sum()
    
    # Create ASCII journey map
    journey_map = '<div class="ascii-art">'
    journey_map += '  CUSTOMER JOURNEY FLOW\n'
    journey_map += '  -------------------\n\n'
    
    for _, row in stage_counts.iterrows():
        percentage = (row["count"] / total) * 100
        bar_length = int(percentage / 2)  # Scale to fit
        
        journey_map += f'  {row["stage"].ljust(15)} | {("█" * bar_length)} {row["count"]} ({percentage:.1f}%)\n'
    
    journey_map += '\n  -------------------\n'
    journey_map += '  TOTAL CUSTOMERS: ' + str(total)
    journey_map += '</div>'
    
    return journey_map

def create_journey_flow_visualization(df, journey_order, max_flows=10):
    """Create ASCII art visualization of customer journey transitions"""
    # Sort interactions by customer and date
    customer_journeys = df.sort_values(["customer_id", "interaction_date"])
    
    # Count transitions between stages
    journey_flows = []
    
    for customer_id in customer_journeys["customer_id"].unique():
        customer_stages = customer_journeys[customer_journeys["customer_id"] == customer_id]["journey_stage"].tolist()
        
        for i in range(len(customer_stages) - 1):
            source = customer_stages[i]
            target = customer_stages[i + 1]
            
            if source != target:  # Only count transitions between different stages
                journey_flows.append((source, target))
    
    # Count frequencies of transitions
    flow_counts = {}
    for source, target in journey_flows:
        if (source, target) in flow_counts:
            flow_counts[(source, target)] += 1
        else:
            flow_counts[(source, target)] = 1
    
    # Sort by frequency
    sorted_flows = sorted(flow_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Create ASCII art visualization
    flow_art = '<div class="ascii-art">'
    flow_art += '  TOP JOURNEY TRANSITIONS\n'
    flow_art += '  ---------------------\n\n'
    
    for (source, target), count in sorted_flows[:max_flows]:
        arrow_length = min(40, count)
        flow_art += f'  {source.ljust(15)} → {target.ljust(15)} {"=" * arrow_length}> {count}\n'
    
    flow_art += '</div>'
    
    return flow_art

def create_metric_table(df, metrics, title="Metrics"):
    """Create an HTML table for displaying metrics with color coding"""
    # Column headers
    header_row = '<tr>'
    for col in df.columns:
        header_row += f'<th>{col.upper()}</th>'
    header_row += '</tr>'
    
    # Table rows
    rows = ''
    for _, row in df.iterrows():
        rows += '<tr>'
        for col in df.columns:
            # Determine if this column needs color coding
            if col in metrics:
                value = row[col]
                if metrics[col]['higher_is_better']:
                    if value >= metrics[col]['good_threshold']:
                        color = "#00ff66"  # Green
                    elif value >= metrics[col]['average_threshold']:
                        color = "#ffcc00"  # Yellow
                    else:
                        color = "#ff0066"  # Red
                else:
                    if value <= metrics[col]['good_threshold']:
                        color = "#00ff66"  # Green
                    elif value <= metrics[col]['average_threshold']:
                        color = "#ffcc00"  # Yellow
                    else:
                        color = "#ff0066"  # Red
                
                rows += f'<td style="color: {color};">{value}</td>'
            else:
                rows += f'<td>{row[col]}</td>'
        rows += '</tr>'
    
    # Complete table
    table_html = f'<div class="terminal"><table class="text-table">{header_row}{rows}</table></div>'
    return table_html

def create_nps_distribution_display(nps_counts, nps_score):
    """Create text-based NPS distribution visualization"""
    total = nps_counts["count"].sum()
    
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
    
    # Add calculation explanation
    promoters = nps_counts[nps_counts["category"] == "Promoter"]["count"].iloc[0] if "Promoter" in nps_counts["category"].values else 0
    detractors = nps_counts[nps_counts["category"] == "Detractor"]["count"].iloc[0] if "Detractor" in nps_counts["category"].values else 0
    
    nps_vis += '<div style="margin-top: 15px; font-style: italic; color: #ffffff;">'
    nps_vis += 'NPS = % Promoters - % Detractors<br>'
    nps_vis += f'NPS = {(promoters/total*100):.1f}% - {(detractors/total*100):.1f}% = {nps_score}'
    nps_vis += '</div>'
    
    nps_vis += '</div>'
    
    return nps_vis

def create_health_indicator(cx_health_percentage, health_level, nps, csat, top_pain_point=None):
    """Create text-based health indicator display"""
    health_display = f'''
    <div class="terminal">
        <div style="margin-bottom: 10px; font-size: 18px;">OVERALL CUSTOMER EXPERIENCE HEALTH: {health_level}</div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {cx_health_percentage}%;">{cx_health_percentage:.1f}%</div>
        </div>
        <div style="margin-top: 15px;">
            <span class="terminal-highlight">►</span> NPS Score: {nps}/10<br>
            <span class="terminal-highlight">►</span> CSAT Score: {csat}/5<br>
    '''
    
    if top_pain_point:
        health_display += f'<span class="terminal-highlight">►</span> Top Pain Point: {top_pain_point}'
    
    health_display += '</div></div>'
    
    return health_display

def create_emotion_distribution(df):
    """Create text-based emotion distribution visualization"""
    # Count emotions
    emotion_counts = df["emotion"].value_counts().reset_index()
    emotion_counts.columns = ["emotion", "count"]
    
    # Calculate percentages
    total = emotion_counts["count"].sum()
    emotion_counts["percentage"] = emotion_counts["count"] / total * 100
    
    # Sort by count
    emotion_counts = emotion_counts.sort_values("count", ascending=False)
    
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
    
    # Create visualization
    emotion_vis = '<div class="terminal">'
    emotion_vis += '<div style="margin-bottom: 15px;">CUSTOMER EMOTION DISTRIBUTION</div>'
    
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
    
    return emotion_vis

def create_pain_point_card(pain_point, impact_score, metrics, frequency, journey_stage, recommendation):
    """Create an alert box with pain point details"""
    # Determine impact level
    impact_level = "HIGH" if impact_score >= 6 else ("MEDIUM" if impact_score >= 4 else "LOW")
    
    card = f'''
    <div class="alert-box">
        <div class="alert-title">{pain_point.upper()} - IMPACT SCORE: {impact_score} - LEVEL: {impact_level}</div>
        <div class="alert-content">
            <p><span style="color: #00ffff;">Metrics</span>: NPS {metrics["nps"]} | CSAT {metrics["csat"]} | CES {metrics["ces"]} | Frequency {frequency}</p>
            <p><span style="color: #00ffff;">Analysis</span>: This pain point significantly impacts customer satisfaction and retention. 
            It occurs most frequently during the {journey_stage} stage.</p>
            <p><span style="color: #00ffff;">Recommendation</span>: {recommendation}</p>
        </div>
    </div>
    '''
    
    return card

def create_improvement_card(improvement, status_colors):
    """Create an improvement card with status indicators"""
    # Status indicators
    status_indicators = {
        "Completed": "✓",
        "In Progress": "►",
        "Planned": "⚑",
        "Not Started": "✕"
    }
    
    # Status color
    status_color = status_colors.get(improvement["status"], "#ffffff")
    status_indicator = status_indicators.get(improvement["status"], "•")
    
    card = f'''
    <div class="alert-box">
        <div class="alert-title">
            <span style="color: {status_color};">[{status_indicator}] {improvement["status"].upper()}</span>: {improvement["suggestion"]}
        </div>
        <div class="alert-content">
            <p><span style="color: #00ffff;">Pain Point</span>: {improvement["pain_point"]} (Frequency: {improvement["frequency"]})</p>
            <p><span style="color: #00ffff;">Expected Impact</span>: {improvement["impact"]}</p>
        </div>
    </div>
    '''
    
    return card