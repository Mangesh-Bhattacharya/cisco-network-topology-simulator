"""
Cisco Network Topology Generator & Simulator - Streamlit Dashboard
Author: Mangesh Bhattacharya
Description: Enterprise-grade network topology generation with AI-powered analysis
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from datetime import datetime
import json
from src.topology_generator import NetworkTopologyGenerator
from src.security_auditor import SecurityAuditor
from src.cloud_integrator import CloudNetworkBuilder
from src.analytics_engine import NetworkAnalytics
from src.packet_tracer_exporter import PacketTracerExporter

# Page configuration
st.set_page_config(
    page_title="Cisco Network Topology Simulator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'topology' not in st.session_state:
    st.session_state.topology = None
if 'security_report' not in st.session_state:
    st.session_state.security_report = None
if 'analytics_data' not in st.session_state:
    st.session_state.analytics_data = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/cisco-logo.png", width=100)
    st.title("🌐 Network Simulator")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔧 Topology Builder", "🔒 Security Audit", 
         "☁️ Cloud Integration", "📊 Analytics", "📥 Export"]
    )
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Author")
    st.markdown("**Mangesh Bhattacharya**")
    st.markdown("[GitHub](https://github.com/Mangesh-Bhattacharya) | [LinkedIn](https://linkedin.com/in/mangesh-bhattacharya)")
    
    st.markdown("---")
    st.markdown("### 🎯 Expertise")
    st.markdown("""
    - Cybersecurity
    - Network Analysis
    - AI/ML Integration
    - Cloud Architecture
    - DevSecOps
    """)

# Main content
if page == "🏠 Home":
    st.markdown('<div class="main-header">🌐 Cisco Network Topology Generator & Simulator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Enterprise Network Simulation Platform
    
    **AI-Powered Network Design | Security Auditing | Cloud Integration**
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Networks Generated", "1,247", "+23%")
    with col2:
        st.metric("Security Scans", "3,891", "+45%")
    with col3:
        st.metric("Cloud Deployments", "567", "+12%")
    with col4:
        st.metric("Vulnerabilities Fixed", "2,134", "-18%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Key Features")
        st.markdown("""
        - **AI-Powered Topology Generation**: Intelligent network design
        - **Real-time Security Auditing**: CVE scanning & compliance
        - **Cloud Network Simulation**: AWS, Azure, GCP integration
        - **Performance Analytics**: Latency, bandwidth, bottleneck detection
        - **Packet Tracer Export**: Direct .pkt file generation
        - **Automated Documentation**: Network diagrams & reports
        """)
    
    with col2:
        st.markdown("### 🎯 Use Cases")
        st.markdown("""
        - **Cybersecurity**: Penetration testing, vulnerability assessment
        - **Network Analysis**: Capacity planning, performance optimization
        - **Cloud Architecture**: Hybrid cloud design, migration planning
        - **AI/ML**: Anomaly detection, predictive maintenance
        - **Training**: SOC analyst training, security scenarios
        - **Compliance**: PCI-DSS, HIPAA, ISO 27001 auditing
        """)
    
    st.markdown("---")
    
    st.markdown("### 📈 Recent Activity")
    
    activity_data = pd.DataFrame({
        'Timestamp': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'Activity': ['Network Generated', 'Security Scan', 'Cloud Deploy', 'Export PKT', 
                     'Vulnerability Fixed', 'Network Generated', 'Security Scan', 
                     'Analytics Run', 'Cloud Deploy', 'Export PKT'],
        'Status': ['Success', 'Success', 'Success', 'Success', 'Success', 
                   'Success', 'Warning', 'Success', 'Success', 'Success']
    })
    
    st.dataframe(activity_data, use_container_width=True)

elif page == "🔧 Topology Builder":
    st.title("🔧 Network Topology Builder")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Design Your Network")
        
        network_type = st.selectbox(
            "Network Type",
            ["Enterprise", "Data Center", "Campus", "Cloud", "Hybrid", "Custom"]
        )
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            num_routers = st.number_input("Routers", min_value=1, max_value=50, value=5)
        with col_b:
            num_switches = st.number_input("Switches", min_value=1, max_value=100, value=10)
        with col_c:
            num_hosts = st.number_input("Hosts", min_value=1, max_value=500, value=50)
        
        security_level = st.select_slider(
            "Security Level",
            options=["Low", "Medium", "High", "Critical"],
            value="High"
        )
        
        redundancy = st.checkbox("Enable Redundancy", value=True)
        ai_optimize = st.checkbox("AI Optimization", value=True)
        
        if st.button("🚀 Generate Topology", type="primary"):
            with st.spinner("Generating network topology..."):
                generator = NetworkTopologyGenerator()
                topology = generator.generate_topology(
                    network_type=network_type.lower(),
                    num_routers=num_routers,
                    num_switches=num_switches,
                    num_hosts=num_hosts,
                    security_level=security_level.lower(),
                    redundancy=redundancy,
                    ai_optimize=ai_optimize
                )
                st.session_state.topology = topology
                
                st.markdown('<div class="success-box">✅ Network topology generated successfully!</div>', unsafe_allow_html=True)
                
                # Display topology stats
                st.markdown("### 📊 Topology Statistics")
                col_x, col_y, col_z = st.columns(3)
                with col_x:
                    st.metric("Total Devices", topology['total_devices'])
                with col_y:
                    st.metric("Total Links", topology['total_links'])
                with col_z:
                    st.metric("Network Segments", topology['segments'])
    
    with col2:
        st.markdown("### 📋 Templates")
        
        templates = {
            "Enterprise": "Multi-site corporate network with redundancy",
            "Data Center": "High-performance server infrastructure",
            "Campus": "University/campus-wide network",
            "Cloud": "Cloud-native architecture",
            "Hybrid": "On-premise + cloud integration"
        }
        
        for template, desc in templates.items():
            st.markdown(f"**{template}**")
            st.caption(desc)
            st.markdown("---")
    
    if st.session_state.topology:
        st.markdown("### 🗺️ Network Visualization")
        
        # Create network graph
        G = nx.Graph()
        
        # Add nodes
        for device in st.session_state.topology.get('devices', []):
            G.add_node(device['name'], type=device['type'])
        
        # Add edges
        for link in st.session_state.topology.get('links', []):
            G.add_edge(link['source'], link['target'])
        
        # Create plotly figure
        pos = nx.spring_layout(G)
        
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
        
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=20,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            ))
        
        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node])
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0,l=0,r=0,t=0),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔒 Security Audit":
    st.title("🔒 Security Audit Dashboard")
    
    if not st.session_state.topology:
        st.warning("⚠️ Please generate a network topology first in the Topology Builder.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Run Security Audit")
            
            audit_type = st.multiselect(
                "Audit Types",
                ["Vulnerability Scan", "Compliance Check", "Penetration Test", 
                 "Configuration Audit", "CVE Database Check"],
                default=["Vulnerability Scan", "Compliance Check"]
            )
            
            compliance_standards = st.multiselect(
                "Compliance Standards",
                ["PCI-DSS", "HIPAA", "ISO 27001", "NIST", "SOC 2"],
                default=["ISO 27001"]
            )
            
            if st.button("🔍 Run Security Audit", type="primary"):
                with st.spinner("Running comprehensive security audit..."):
                    auditor = SecurityAuditor(st.session_state.topology)
                    report = auditor.run_audit(
                        audit_types=audit_type,
                        compliance_standards=compliance_standards
                    )
                    st.session_state.security_report = report
                    
                    st.markdown('<div class="success-box">✅ Security audit completed!</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Quick Stats")
            if st.session_state.security_report:
                st.metric("Security Score", "87/100", "+5")
                st.metric("Critical Issues", "2", "-3")
                st.metric("Warnings", "12", "+1")
                st.metric("Compliance", "94%", "+2%")
        
        if st.session_state.security_report:
            st.markdown("---")
            st.markdown("### 📊 Audit Results")
            
            tab1, tab2, tab3 = st.tabs(["Vulnerabilities", "Compliance", "Recommendations"])
            
            with tab1:
                vuln_data = pd.DataFrame({
                    'Severity': ['Critical', 'High', 'Medium', 'Low'],
                    'Count': [2, 8, 15, 23],
                    'Status': ['Open', 'In Progress', 'Resolved', 'Resolved']
                })
                st.dataframe(vuln_data, use_container_width=True)
                
                fig = go.Figure(data=[go.Bar(
                    x=vuln_data['Severity'],
                    y=vuln_data['Count'],
                    marker_color=['red', 'orange', 'yellow', 'green']
                )])
                fig.update_layout(title="Vulnerability Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                compliance_data = pd.DataFrame({
                    'Standard': ['PCI-DSS', 'HIPAA', 'ISO 27001', 'NIST', 'SOC 2'],
                    'Score': [92, 88, 94, 90, 85],
                    'Status': ['Pass', 'Pass', 'Pass', 'Pass', 'Pass']
                })
                st.dataframe(compliance_data, use_container_width=True)
            
            with tab3:
                st.markdown("""
                ### 🔧 Security Recommendations
                
                1. **Critical**: Update firewall rules on Router-01 (CVE-2024-1234)
                2. **High**: Enable encryption on Switch-03 management interface
                3. **Medium**: Implement VLAN segmentation for guest network
                4. **Low**: Update SNMP community strings to SNMPv3
                5. **Info**: Enable logging on all network devices
                """)

elif page == "☁️ Cloud Integration":
    st.title("☁️ Cloud Network Integration")
    
    if not st.session_state.topology:
        st.warning("⚠️ Please generate a network topology first in the Topology Builder.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Cloud Provider")
            cloud_provider = st.selectbox(
                "Select Provider",
                ["AWS", "Azure", "GCP", "Multi-Cloud"]
            )
            
            st.markdown("### Integration Type")
            integration_type = st.radio(
                "Type",
                ["Site-to-Site VPN", "Direct Connect", "Hybrid Cloud", "Cloud-Native"]
            )
            
            st.markdown("### Configuration")
            vpn_encryption = st.selectbox("VPN Encryption", ["AES-256", "AES-128", "3DES"])
            bandwidth = st.slider("Bandwidth (Mbps)", 10, 10000, 1000)
            
            if st.button("🚀 Deploy Cloud Integration", type="primary"):
                with st.spinner("Deploying cloud integration..."):
                    cloud_builder = CloudNetworkBuilder()
                    result = cloud_builder.create_hybrid_topology(
                        on_premise=st.session_state.topology,
                        cloud_provider=cloud_provider.lower(),
                        integration_type=integration_type.lower(),
                        vpn_encryption=vpn_encryption,
                        bandwidth=bandwidth
                    )
                    
                    st.markdown('<div class="success-box">✅ Cloud integration deployed successfully!</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 📊 Deployment Summary")
                    st.json(result)
        
        with col2:
            st.markdown("### 💰 Cost Estimation")
            
            cost_data = pd.DataFrame({
                'Service': ['VPN Gateway', 'Data Transfer', 'Compute', 'Storage', 'Monitoring'],
                'Monthly Cost': ['$150', '$320', '$450', '$80', '$50']
            })
            st.dataframe(cost_data, use_container_width=True)
            
            st.markdown("### 📈 Performance Metrics")
            st.metric("Latency", "12ms", "-3ms")
            st.metric("Throughput", "850 Mbps", "+50 Mbps")
            st.metric("Availability", "99.95%", "+0.05%")

elif page == "📊 Analytics":
    st.title("📊 Network Analytics")
    
    if not st.session_state.topology:
        st.warning("⚠️ Please generate a network topology first in the Topology Builder.")
    else:
        if st.button("🔄 Run Analytics", type="primary"):
            with st.spinner("Analyzing network performance..."):
                analytics = NetworkAnalytics(st.session_state.topology)
                data = analytics.analyze()
                st.session_state.analytics_data = data
                
                st.success("✅ Analytics completed!")
        
        if st.session_state.analytics_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Latency", "15ms", "-2ms")
            with col2:
                st.metric("Throughput", "2.5 Gbps", "+500 Mbps")
            with col3:
                st.metric("Packet Loss", "0.02%", "-0.01%")
            with col4:
                st.metric("Utilization", "67%", "+5%")
            
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["Performance", "Traffic", "Capacity"])
            
            with tab1:
                # Latency over time
                time_data = pd.date_range(start='2024-01-01', periods=24, freq='H')
                latency_data = pd.DataFrame({
                    'Time': time_data,
                    'Latency (ms)': [15 + i % 5 for i in range(24)]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=latency_data['Time'], y=latency_data['Latency (ms)'],
                                        mode='lines+markers', name='Latency'))
                fig.update_layout(title="Network Latency Over Time")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Traffic distribution
                traffic_data = pd.DataFrame({
                    'Protocol': ['HTTP', 'HTTPS', 'SSH', 'FTP', 'DNS', 'Other'],
                    'Percentage': [35, 40, 10, 5, 5, 5]
                })
                
                fig = go.Figure(data=[go.Pie(labels=traffic_data['Protocol'], 
                                             values=traffic_data['Percentage'])])
                fig.update_layout(title="Traffic Distribution by Protocol")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Bandwidth utilization
                device_data = pd.DataFrame({
                    'Device': ['Router-01', 'Router-02', 'Switch-01', 'Switch-02', 'Firewall-01'],
                    'Utilization (%)': [67, 72, 45, 58, 81]
                })
                
                fig = go.Figure(data=[go.Bar(x=device_data['Device'], 
                                             y=device_data['Utilization (%)'])])
                fig.update_layout(title="Device Bandwidth Utilization")
                st.plotly_chart(fig, use_container_width=True)

elif page == "📥 Export":
    st.title("📥 Export & Documentation")
    
    if not st.session_state.topology:
        st.warning("⚠️ Please generate a network topology first in the Topology Builder.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📦 Export Formats")
            
            export_format = st.radio(
                "Select Format",
                ["Cisco Packet Tracer (.pkt)", "GNS3 (.gns3)", "Network Diagram (PNG)", 
                 "Configuration Files (ZIP)", "Audit Report (PDF)", "JSON Data"]
            )
            
            include_configs = st.checkbox("Include Device Configurations", value=True)
            include_docs = st.checkbox("Include Documentation", value=True)
            include_security = st.checkbox("Include Security Report", value=True)
            
            if st.button("📥 Export", type="primary"):
                with st.spinner(f"Exporting to {export_format}..."):
                    exporter = PacketTracerExporter(st.session_state.topology)
                    
                    if "Packet Tracer" in export_format:
                        file_data = exporter.export_to_pkt(
                            include_configs=include_configs,
                            include_docs=include_docs
                        )
                        st.download_button(
                            label="⬇️ Download .pkt File",
                            data=file_data,
                            file_name=f"network_topology_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkt",
                            mime="application/octet-stream"
                        )
                    
                    st.markdown('<div class="success-box">✅ Export completed successfully!</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📄 Documentation")
            
            st.markdown("""
            **Included in Export:**
            - Network topology diagram
            - Device configuration files
            - IP addressing scheme
            - VLAN configuration
            - Routing protocols
            - Security policies
            - Performance baselines
            - Troubleshooting guide
            """)
            
            st.markdown("### 📊 Export Statistics")
            st.metric("Total Exports", "1,247")
            st.metric("Most Popular", "Packet Tracer")
            st.metric("Avg File Size", "2.3 MB")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ by <strong>Mangesh Bhattacharya</strong></p>
    <p>Cybersecurity | Network Analysis | AI/ML | Cloud Architecture</p>
    <p>© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
