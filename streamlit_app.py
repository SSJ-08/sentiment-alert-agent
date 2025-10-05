import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from review_loader import get_new_alerts
from sample_reviews import sample_alerts
import requests
import json
EMAILJS_PUBLIC_KEY = "8vEMRpl9AFImFQ0fX"
EMAILJS_SERVICE_ID = "service_urmnk7u"
EMAILJS_TEMPLATE_ID = "template_2muqoj5"
existing_ids = set()
alerts = get_new_alerts(existing_ids, n=5)
existing_ids.update([int(a["id"]) for a in alerts])
print(alerts)
st.set_page_config(
    page_title="Customer Sentiment Alert System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if 'alerts' not in st.session_state:
    st.session_state.alerts = sample_alerts.copy()
if 'responded_alerts' not in st.session_state:
    st.session_state.responded_alerts = set()
def send_email(alert):
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "alert_id": alert['id'],
            "platform": alert['platform'],
            "author": alert['author'],
            "urgency": alert['urgency'],
            "sentiment": alert['sentiment'],
            "timestamp": alert['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            "customer_message": alert['text'],
            "recommended_response": alert['recommendedResponse'],
            "metrics": json.dumps(alert['metrics']),
            "alert_url": "https://example.com/alert/" + alert['id']
        }
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        st.success(f"Email sent for alert {alert['id']}")
    else:
        st.error(f"Failed to send email: {response.text}")
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .alert-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .alert-card-responded {
        opacity: 0.5;
    }
    
    .urgency-high {
        color: #dc2626;
        font-weight: bold;
    }
    
    .urgency-medium {
        color: #ea580c;
        font-weight: bold;
    }
    
    .urgency-low {
        color: #16a34a;
        font-weight: bold;
    }
    
    .sentiment-very-negative {
        color: #dc2626;
    }
    
    .sentiment-negative {
        color: #ea580c;
    }
    
    .platform-icon {
        display: inline-block;
        width: 1rem;
        height: 1rem;
        margin-right: 0.5rem;
    }
    
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .filter-container {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'alerts' not in st.session_state:
    st.session_state.alerts = [
        {
            "id": "1",
            "timestamp": datetime.now() - timedelta(minutes=5),
            "source": "Twitter",
            "platform": "twitter",
            "sentiment": "very-negative",
            "text": "Terrible customer service experience with @company. Waited 2 hours for basic support. Switching to competitors.",
            "author": "@frustrated_user",
            "urgency": "high",
            # "recommendedResponse": "Immediate personal outreach with senior support manager. Offer expedited resolution and service credit.",
            "metrics": {"engagement": 45, "reach": 1200}
        },
        {
            "id": "2",
            "timestamp": datetime.now() - timedelta(minutes=15),
            "source": "Google Reviews",
            "platform": "reviews",
            "sentiment": "negative",
            "text": "Product quality has declined significantly. Last three orders had defects. Very disappointed.",
            "author": "Sarah M.",
            "urgency": "medium",
            # "recommendedResponse": "Quality team investigation recommended. Proactive outreach to address specific issues and offer replacement.",
            "metrics": {"rating": 2, "helpful": 8}
        },
        {
            "id": "3",
            "timestamp": datetime.now() - timedelta(minutes=30),
            "source": "Reddit",
            "platform": "forum",
            "sentiment": "negative",
            "text": "Anyone else having issues with their recent update? App crashes constantly now.",
            "author": "techuser2024",
            "urgency": "medium",
            # "recommendedResponse": "Technical team to provide update timeline. Community management to acknowledge and provide workaround.",
            "metrics": {"upvotes": 23, "comments": 12}
        },
        {
            "id": "4",
            "timestamp": datetime.now() - timedelta(minutes=45),
            "source": "App Store",
            "platform": "reviews",
            "sentiment": "very-negative",
            "text": "Latest update broke everything. Can't even log in anymore. Worst app experience ever.",
            "author": "AppUser_iOS",
            "urgency": "high",
            # "recommendedResponse": "Immediate technical response required. Escalate to development team and provide emergency patch timeline.",
            "metrics": {"rating": 1, "helpful": 15}
        }
    ]

if 'responded_alerts' not in st.session_state:
    st.session_state.responded_alerts = set()

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Auto-refresh functionality
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True


def get_platform_emoji(platform):
    """Get emoji for platform"""
    platform_emojis = {
        "twitter": "🐦",
        "reviews": "⭐",
        "forum": "💬"
    }
    return platform_emojis.get(platform, "📱")

def get_urgency_color(urgency):
    """Get color class for urgency"""
    colors = {
        "high": "urgency-high",
        "medium": "urgency-medium", 
        "low": "urgency-low"
    }
    return colors.get(urgency, "urgency-low")

def get_sentiment_color(sentiment):
    """Get color class for sentiment"""
    colors = {

        "negative": "sentiment-negative"
    }
    return colors.get(sentiment, "")

def create_platform_pie_chart(alerts):
    """Create platform distribution pie chart"""
    platform_counts = {}
    for alert in alerts:
        platform_counts[alert['platform']] = platform_counts.get(alert['platform'], 0) + 1
    
    if not platform_counts:
        return go.Figure()
    
    colors = ['#1da1f2', '#4285f4', '#ff4500', '#10b981']
    
    fig = go.Figure(data=[go.Pie(
        labels=list(platform_counts.keys()),
        values=list(platform_counts.values()),
        hole=.3,
        marker_colors=colors[:len(platform_counts)]
    )])
    
    fig.update_layout(
        title="Alert Sources",
        height=300,
        showlegend=True,
        margin=dict(t=40, b=0, l=0, r=0)
    )
    
    return fig

def create_hourly_trend_chart(alerts):
    """Create 24-hour trend bar chart"""
    hourly_data = []
    
    for i in range(24):
        hour_time = datetime.now() - timedelta(hours=23-i)
        hour_alerts = sum(1 for alert in alerts 
                         if alert['timestamp'].hour == hour_time.hour and 
                         alert['timestamp'].date() == hour_time.date())
        
        hourly_data.append({
            'hour': hour_time.hour,
            'alerts': hour_alerts if hour_alerts > 0 else random.randint(0, 3)
        })
    
    df = pd.DataFrame(hourly_data)
    
    fig = px.bar(
        df, 
        x='hour', 
        y='alerts',
        title='24-Hour Alert Trend',
        color_discrete_sequence=['#ef4444']
    )
    
    fig.update_layout(
        height=300,
        xaxis_title="Hour",
        yaxis_title="Alerts",
        margin=dict(t=40, b=40, l=40, r=40)
    )
    
    return fig

def filter_alerts(alerts, urgency_filter, platform_filter, sentiment_filter):
    """Filter alerts based on criteria"""
    filtered = alerts
    
    if urgency_filter != "all":
        filtered = [alert for alert in filtered if alert['urgency'] == urgency_filter]
    
    if platform_filter != "all":
        filtered = [alert for alert in filtered if alert['platform'] == platform_filter]
    
    if sentiment_filter != "all":
        filtered = [alert for alert in filtered if alert['sentiment'] == sentiment_filter]
    
    return filtered
if 'alerts' not in st.session_state:
    st.session_state.alerts = sample_alerts.copy()

if 'next_alert_index' not in st.session_state:
    st.session_state.next_alert_index = 0 
def main():
    if st.session_state.auto_refresh and (datetime.now() - st.session_state.last_update).seconds > 10:
        # simulate_new_alert()
        st.session_state.last_update = datetime.now()
        st.rerun()
    st.markdown("# Customer Sentiment Alert System")
    st.markdown("Real-time monitoring of customer feedback across all channels")
    alerts = st.session_state.alerts
    urgent_alerts = len([alert for alert in alerts if alert['urgency'] == 'high'])
    total_alerts = len(alerts)
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Urgent Alerts", urgent_alerts, delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Total Mentions", total_alerts, delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.metric("Avg Response Time", "12m", delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        platform_chart = create_platform_pie_chart(alerts)
        st.plotly_chart(platform_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
            <style>
                /* Set all main text to black */
                .stApp, 
                .stApp * {
                    color: white !important;
                }

                /* Optional: override specific card texts if needed */
                .metric-card,
                .alert-card,
                .chart-container,
                .filter-container {
                    color: white !important;
                }
            </style>
            """, unsafe_allow_html=True)
        hourly_chart = create_hourly_trend_chart(alerts)
        st.plotly_chart(hourly_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("### 🔍 Filters")
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 1, 1])
        with filter_col1:
            urgency_filter = st.selectbox(
                "Urgency Level",
                ["all", "high", "medium", "low"],
                key="urgency_filter"
            )
        with filter_col2:
            platform_filter = st.selectbox(
                "Platform",
                ["all", "twitter", "reviews", "forum"],
                key="platform_filter"
            )
        with filter_col3:
            sentiment_filter = st.selectbox(
                "Sentiment",
                ["all", "negative", "neutral", "positive"],
                key="sentiment_filter"
            )
        
        with filter_col4:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        filtered_alerts = filter_alerts(alerts, urgency_filter, platform_filter, sentiment_filter)
        st.markdown(f"### Recent Alerts")
        
        if not filtered_alerts:
            st.markdown("""
            <div class="alert-card" style="text-align: center; padding: 2rem;">
                💬<br>
                <strong>No alerts found</strong><br>
                <span style="color: #6b7280;">No alerts match the current filters. Try adjusting your filter criteria.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for alert in filtered_alerts:
                is_responded = alert['id'] in st.session_state.responded_alerts
                card_class = "alert-card-responded" if is_responded else ""
                
                with st.expander(f"{get_platform_emoji(alert['platform'])} {alert['source']} - {alert['author']} ({'✅ Responded' if is_responded else alert['urgency'].upper()})", expanded=False):
                    
                    # Alert content
                    col_content, col_actions = st.columns([3, 1])
                    
                    with col_content:
                        st.markdown(f'<span class="{get_urgency_color(alert["urgency"])}">{alert["urgency"].upper()}</span>', unsafe_allow_html=True)
                        st.markdown(f'<span class="{get_sentiment_color(alert["sentiment"])}">"{alert["text"]}"</span>', unsafe_allow_html=True)
                        
                        # Metrics
                        time_ago = datetime.now() - alert['timestamp']
                        minutes_ago = int(time_ago.total_seconds() / 60)
                        
                        metrics_text = f"🕒 {minutes_ago} minutes ago"
                        if 'engagement' in alert['metrics']:
                            metrics_text += f" • 📈 {alert['metrics']['engagement']} engagements"
                        if 'rating' in alert['metrics']:
                            metrics_text += f" • ⭐ {alert['metrics']['rating']}/5 stars"
                        
                        st.markdown(f"<small>{metrics_text}</small>", unsafe_allow_html=True)
                    
                    with col_actions:
                        if is_responded:
                            st.markdown("✅ **Response sent**")
                        else:
                            if st.button("📤 Send Response", key=f"respond_{alert['id']}"):
                                st.session_state.responded_alerts.add(alert['id'])
                                send_email(alert) 
                                st.rerun()

                    
if __name__ == "__main__":
    main()


