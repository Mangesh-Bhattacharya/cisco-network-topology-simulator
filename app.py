import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from src.topology_generator import NetworkTopologyGenerator
import json
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Cisco Network Topology Simulator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'topology' not in st.session_state:
    st.session_state.topology = None
if 'generator' not in st.session_state:
    st.session_state.generator = None

# Header
st.title("🌐 Cisco Network Topology Simulator")
st.markdown("""
Generate professional Cisco-style network topology diagrams with AI-powered optimization.  
Perfect for network planning, documentation, and cybersecurity analysis.
""")

# Sidebar configuration
st.sidebar.header("⚙️ Topology Configuration")
st.sidebar.markdown("---")

network_type = st.sidebar.selectbox(
    "🏢 Network Type",
    ["enterprise", "datacenter", "campus", "cloud", "hybrid"],
    help="Select the type of network infrastructure"
)

st.sidebar.markdown("### 📊 Network Size")
num_routers = st.sidebar.slider("Routers", 1, 10, 3, help="Number of core routers")
num_switches = st.sidebar.slider("Switches", 2, 20, 6, help="Distribution and access switches")
num_hosts = st.sidebar.slider("Hosts/Endpoints", 5, 50, 20, help="End devices (PCs, servers)")

st.sidebar.markdown("### 🛡️ Security & Optimization")
security_level = st.sidebar.selectbox(
    "Security Level",
    ["low", "medium", "high", "critical"],
    index=2,
    help="Determines firewall and IPS placement"
)

redundancy = st.sidebar.checkbox("Enable Redundancy", value=True, help="Add redundant links for high availability")
ai_optimize = st.sidebar.checkbox("AI Optimization", value=True, help="Use AI to optimize topology design")
show_bandwidth = st.sidebar.checkbox("Show Bandwidth Labels", value=True, help="Display link speeds on diagram")

st.sidebar.markdown("---")

# Generate topology button
if st.sidebar.button("🚀 Generate Topology", type="primary", use_container_width=True):
    with st.spinner("🔄 Generating network topology..."):
        try:
            generator = NetworkTopologyGenerator()
            topology = generator.generate_topology(
                network_type=network_type,
                num_routers=num_routers,
                num_switches=num_switches,
                num_hosts=num_hosts,
                security_level=security_level,
                redundancy=redundancy,
                ai_optimize=ai_optimize
            )
            st.session_state.topology = topology
            st.session_state.generator = generator
            st.success("✅ Topology generated successfully!")
        except Exception as e:
            st.error(f"❌ Error generating topology: {str(e)}")
            with st.expander("🔍 View Error Details"):
                import traceback
                st.code(traceback.format_exc())


def compute_hierarchical_positions(topology):
    """
    Compute deterministic 3-tier hierarchical layout positions.
    Architecture: Core → Distribution → Access → Endpoints
    """
    devices = topology['devices']
    
    # Group devices by type and layer
    routers = [d for d in devices if d['type'] == 'router']
    switches = [d for d in devices if d['type'] == 'switch']
    hosts = [d for d in devices if d['type'] == 'host']
    firewalls = [d for d in devices if d['type'] == 'firewall']
    ips_devices = [d for d in devices if d['type'] == 'ips']
    clouds = [d for d in devices if d['type'] == 'cloud']
    
    # Separate distribution and access switches
    dist_switches = [s for s in switches if 'distribution' in s.get('subtype', '').lower()]
    access_switches = [s for s in switches if 'access' in s.get('subtype', '').lower()]
    
    # If no subtypes defined, split switches into dist/access layers
    if not dist_switches and not access_switches and switches:
        mid = len(switches) // 2
        dist_switches = switches[:mid] if mid > 0 else []
        access_switches = switches[mid:] if mid < len(switches) else switches
    
    pos = {}
    
    # Spacing parameters for clean layout
    spacing_x = 4.5
    spacing_y = 4.0
    
    # Layer 0: Cloud (top-most)
    y_cloud = 5 * spacing_y
    if clouds:
        start_x = -spacing_x * (len(clouds) - 1) / 2
        for i, cloud in enumerate(clouds):
            pos[cloud['name']] = (start_x + i * spacing_x, y_cloud)
    
    # Layer 1: Core Routers
    y_core = 4 * spacing_y
    if routers:
        start_x = -spacing_x * (len(routers) - 1) / 2
        for i, router in enumerate(routers):
            pos[router['name']] = (start_x + i * spacing_x, y_core)
    
    # Layer 2: Security Layer (Firewalls & IPS)
    y_security = 3.2 * spacing_y
    security_devices = firewalls + ips_devices
    if security_devices:
        start_x = -spacing_x * (len(security_devices) - 1) / 2
        for i, sec in enumerate(security_devices):
            pos[sec['name']] = (start_x + i * spacing_x, y_security)
    
    # Layer 3: Distribution Switches
    y_dist = 2.5 * spacing_y
    if dist_switches:
        start_x = -spacing_x * (len(dist_switches) - 1) / 2
        for i, switch in enumerate(dist_switches):
            pos[switch['name']] = (start_x + i * spacing_x, y_dist)
    
    # Layer 4: Access Switches
    y_access = 1.7 * spacing_y
    if access_switches:
        start_x = -spacing_x * (len(access_switches) - 1) / 2
        for i, switch in enumerate(access_switches):
            pos[switch['name']] = (start_x + i * spacing_x, y_access)
    
    # Layer 5: Hosts/Endpoints (limit display for clean visualization)
    y_host = 0.8 * spacing_y
    max_hosts = min(30, len(hosts))
    if hosts:
        host_spacing_x = 3.0
        start_x = -host_spacing_x * (max_hosts - 1) / 2
        for i, host in enumerate(hosts[:max_hosts]):
            pos[host['name']] = (start_x + i * host_spacing_x, y_host)
    
    return pos


def create_cisco_diagram(topology, show_bandwidth=True):
    """
    Create professional Cisco-style hierarchical network diagram with emoji icons
    """
    # Icon mapping for device types
    icon_map = {
        'router': '🛜',      # Router icon
        'switch': '🔀',      # Switch icon
        'host': '💻',        # PC icon
        'firewall': '🧱',    # Firewall icon
        'ips': '🔒',         # IPS icon
        'cloud': '☁️'        # Cloud icon
    }
    
    # Build NetworkX graph
    G = nx.Graph()
    
    for device in topology['devices']:
        G.add_node(device['name'], **device)
    
    for link in topology['links']:
        G.add_edge(link['source'], link['target'], **link)
    
    # Get hierarchical positions
    pos = compute_hierarchical_positions(topology)
    
    # Create Plotly figure
    fig = go.Figure()
    
    # ========== Draw Connection Lines (Background Layer) ==========
    for u, v, data in G.edges(data=True):
        if u not in pos or v not in pos:
            continue
        
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        
        # Draw connection line
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color='#4B5563', width=2.5),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Add bandwidth label on link
        if show_bandwidth:
            bandwidth = data.get('bandwidth', '')
            if bandwidth:
                mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
                
                # Add bandwidth text with background
                fig.add_annotation(
                    x=mid_x,
                    y=mid_y,
                    text=f"<b>{bandwidth}</b>",
                    showarrow=False,
                    font=dict(
                        size=10,
                        family='Courier New, monospace',
                        color='#DC2626'
                    ),
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#E5E7EB',
                    borderwidth=1,
                    borderpad=3,
                    opacity=0.95
                )
    
    # ========== Draw Device Icons and Labels (Foreground Layer) ==========
    for node in G.nodes():
        if node not in pos:
            continue
        
        x, y = pos[node]
        node_data = G.nodes[node]
        device_type = node_data['type']
        ip_addr = node_data.get('ip_address', '')
        model = node_data.get('model', 'N/A')
        
        # Get emoji icon for device type
        device_icon = icon_map.get(device_type, '📦')
        
        # Add device icon as large emoji
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='text',
            text=[device_icon],
            textfont=dict(size=50),
            hovertext=(
                f"<b>{node}</b><br>"
                f"─────────────────<br>"
                f"<b>Type:</b> {device_type.upper()}<br>"
                f"<b>IP:</b> {ip_addr}<br>"
                f"<b>Model:</b> {model}"
            ),
            hoverinfo='text',
            showlegend=False
        ))
        
        # Device name label (below icon)
        fig.add_annotation(
            x=x,
            y=y - 0.55,
            text=f"<b>{node}</b>",
            showarrow=False,
            font=dict(
                size=11,
                family='Arial, sans-serif',
                color='#1F2937'
            ),
            yanchor='top'
        )
        
        # IP address label (only for network infrastructure devices)
        if device_type in ['router', 'switch', 'firewall', 'ips']:
            fig.add_annotation(
                x=x,
                y=y - 0.85,
                text=ip_addr,
                showarrow=False,
                font=dict(
                    size=9,
                    family='Courier New, monospace',
                    color='#6B7280'
                ),
                yanchor='top'
            )
    
    # ========== Layout Configuration ==========
    fig.update_layout(
        title=dict(
            text=f"<b>{topology['network_type'].upper()} Network Topology</b>",
            font=dict(
                size=26,
                color='#111827',
                family='Arial Black, sans-serif'
            ),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='#F9FAFB',
        paper_bgcolor='#FFFFFF',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-22, 22]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1, 22]
        ),
        height=900,
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    return fig


# ========== Main Application Display ==========
if st.session_state.topology is not None:
    topology = st.session_state.topology
    
    # Metrics Dashboard
    st.markdown("### 📊 Network Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Devices",
            value=topology['total_devices'],
            delta=None,
            help="Total number of network devices"
        )
    with col2:
        st.metric(
            label="Network Links",
            value=topology['total_links'],
            delta=None,
            help="Total connections between devices"
        )
    with col3:
        st.metric(
            label="Network Segments",
            value=topology['segments'],
            delta=None,
            help="Logical network segments"
        )
    with col4:
        st.metric(
            label="Security Devices",
            value=topology['metadata'].get('security_devices', 0),
            delta=None,
            help="Firewalls and IPS/IDS systems"
        )
    
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Topology Diagram",
        "📋 Device Inventory",
        "🔗 Network Links",
        "💾 Export & Config"
    ])
    
    # ========== Tab 1: Topology Diagram ==========
    with tab1:
        st.markdown("### 🎨 Network Topology Visualization")
        st.markdown("Interactive diagram showing hierarchical network architecture")
        
        try:
            fig = create_cisco_diagram(topology, show_bandwidth)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'{network_type}_topology',
                    'height': 1200,
                    'width': 1600,
                    'scale': 2
                }
            })
            
            # Device Legend
            st.markdown("---")
            st.markdown("### 🎨 Device Legend")
            cols = st.columns(6)
            with cols[0]:
                st.markdown("🛜 **Router**")
            with cols[1]:
                st.markdown("🔀 **Switch**")
            with cols[2]:
                st.markdown("💻 **Host/PC**")
            with cols[3]:
                st.markdown("🧱 **Firewall**")
            with cols[4]:
                st.markdown("🔒 **IPS/IDS**")
            with cols[5]:
                st.markdown("☁️ **Cloud**")
            
            # Network layers explanation
            with st.expander("ℹ️ Network Architecture Layers"):
                st.markdown("""
                **Hierarchical Network Design:**
                - **Layer 5 (Top):** ☁️ Cloud Services & External Connectivity
                - **Layer 4:** 🛜 Core Routers - High-speed backbone routing
                - **Layer 3:** 🧱🔒 Security Layer - Firewalls and IPS/IDS
                - **Layer 2:** 🔀 Distribution Switches - Inter-VLAN routing
                - **Layer 1:** 🔀 Access Switches - End-device connectivity
                - **Layer 0 (Bottom):** 💻 Endpoints - Workstations and servers
                """)
                
        except Exception as e:
            st.error(f"❌ Error creating visualization: {str(e)}")
            with st.expander("🔍 View Error Details"):
                import traceback
                st.code(traceback.format_exc())
    
    # ========== Tab 2: Device Inventory ==========
    with tab2:
        st.markdown("### 📋 Complete Device Inventory")
        
        # Group devices by type
        device_types = {}
        for device in topology['devices']:
            dev_type = device['type']
            if dev_type not in device_types:
                device_types[dev_type] = []
            device_types[dev_type].append(device)
        
        # Device type icons for headers
        type_icons = {
            'router': '🛜',
            'switch': '🔀',
            'host': '💻',
            'firewall': '🧱',
            'ips': '🔒',
            'cloud': '☁️'
        }
        
        # Display each device type in expandable sections
        for dev_type, devices in sorted(device_types.items()):
            icon = type_icons.get(dev_type, '📦')
            with st.expander(
                f"{icon} **{dev_type.upper()}** ({len(devices)} devices)",
                expanded=(dev_type in ['router', 'switch'])
            ):
                df = pd.DataFrame(devices)
                cols_to_show = ['name', 'type', 'ip_address', 'model']
                # Add subtype if exists
                if 'subtype' in df.columns:
                    cols_to_show.append('subtype')
                
                st.dataframe(
                    df[cols_to_show],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Device Name", width="medium"),
                        "type": st.column_config.TextColumn("Type", width="small"),
                        "ip_address": st.column_config.TextColumn("IP Address", width="medium"),
                        "model": st.column_config.TextColumn("Model", width="medium"),
                    }
                )
    
    # ========== Tab 3: Network Links ==========
    with tab3:
        st.markdown("### 🔗 Network Connection Matrix")
        
        links_df = pd.DataFrame(topology['links'])
        
        st.dataframe(
            links_df,
            use_container_width=True,
            height=400,
            column_config={
                "source": st.column_config.TextColumn("Source Device", width="medium"),
                "target": st.column_config.TextColumn("Target Device", width="medium"),
                "type": st.column_config.TextColumn("Link Type", width="small"),
                "bandwidth": st.column_config.TextColumn("Bandwidth", width="small"),
            }
        )
        
        # Link Statistics
        st.markdown("---")
        st.markdown("### 📈 Link Statistics & Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Link types distribution
            link_types = links_df['type'].value_counts()
            fig_types = go.Figure(data=[
                go.Bar(
                    x=link_types.index,
                    y=link_types.values,
                    marker_color='#3B82F6',
                    text=link_types.values,
                    textposition='auto',
                )
            ])
            fig_types.update_layout(
                title="Links by Type",
                xaxis_title="Link Type",
                yaxis_title="Count",
                height=350,
                plot_bgcolor='#F9FAFB',
                paper_bgcolor='#FFFFFF',
                showlegend=False
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Summary metrics
            st.markdown("#### Connection Summary")
            st.metric("Total Connections", len(links_df))
            st.metric("Unique Link Types", len(link_types))
            
            # Bandwidth distribution if available
            if 'bandwidth' in links_df.columns:
                bw_counts = links_df['bandwidth'].value_counts()
                st.markdown("**Bandwidth Distribution:**")
                for bw, count in bw_counts.items():
                    st.write(f"• {bw}: {count} links")
    
    # ========== Tab 4: Export & Configuration ==========
    with tab4:
        st.markdown("### 💾 Export Options & Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Download Topology Data")
            
            if st.session_state.generator is not None:
                # JSON Export
                json_data = st.session_state.generator.get_topology_json()
                st.download_button(
                    label="📄 Download JSON Configuration",
                    data=json_data,
                    file_name=f"{network_type}_topology_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                # CSV Export for devices
                devices_df = pd.DataFrame(topology['devices'])
                csv_devices = devices_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Device List (CSV)",
                    data=csv_devices,
                    file_name=f"{network_type}_devices.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # CSV Export for links
                links_csv = links_df.to_csv(index=False)
                st.download_button(
                    label="🔗 Download Links List (CSV)",
                    data=links_csv,
                    file_name=f"{network_type}_links.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("#### ⚙️ Topology Configuration")
            
            config_summary = {
                'network_type': topology['network_type'],
                'total_devices': topology['total_devices'],
                'total_links': topology['total_links'],
                'segments': topology['segments'],
                'security_level': topology['security_level'],
                'redundancy_enabled': topology['redundancy_enabled'],
                'ai_optimized': topology['ai_optimized'],
                'generation_timestamp': pd.Timestamp.now().isoformat()
            }
            
            st.json(config_summary, expanded=True)
            
            # Device breakdown
            st.markdown("**Device Breakdown:**")
            device_counts = pd.DataFrame(topology['devices'])['type'].value_counts()
            for dev_type, count in device_counts.items():
                type_icons = {'router': '🛜', 'switch': '🔀', 'host': '💻', 
                             'firewall': '🧱', 'ips': '🔒', 'cloud': '☁️'}
                icon = type_icons.get(dev_type, '📦')
                st.write(f"{icon} **{dev_type.capitalize()}:** {count}")

else:
    # ========== Welcome Screen ==========
    st.info("👈 **Get Started:** Configure your network topology using the sidebar and click **Generate Topology**")
    
    st.markdown("---")
    st.markdown("## 🎯 Quick Start Examples")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏢 Small Office Network
        **Configuration:**
        - 🛜 2 Routers
        - 🔀 4 Switches
        - 💻 20 Hosts
        - 🛡️ Medium Security
        
        **Use Case:**  
        Ideal for small-to-medium business with 20-50 employees.
        Basic security with firewall protection.
        """)
    
    with col2:
        st.markdown("""
        ### 🏭 Enterprise Campus
        **Configuration:**
        - 🛜 5 Routers
        - 🔀 10 Switches
        - 💻 50 Hosts
        - 🛡️ High Security
        
        **Use Case:**  
        Multi-building campus deployment with redundancy.
        Advanced security with IPS/IDS systems.
        """)
    
    with col3:
        st.markdown("""
        ### 🖥️ Data Center
        **Configuration:**
        - 🛜 10 Routers
        - 🔀 20 Switches
        - 💻 100 Hosts
        - 🛡️ Critical Security
        
        **Use Case:**  
        High-availability data center design.
        Full redundancy and critical security controls.
        """)
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("""
        **🎨 Visualization:**
        - Professional Cisco-style diagrams
        - Hierarchical network layouts
        - Interactive exploration
        - Export to high-res PNG
        
        **🤖 AI Optimization:**
        - Intelligent topology design
        - Automatic redundancy planning
        - Security device placement
        - Performance optimization
        """)
    
    with feat_col2:
        st.markdown("""
        **📊 Analysis & Export:**
        - Device inventory management
        - Link analysis and statistics
        - JSON/CSV data export
        - Configuration documentation
        
        **🛡️ Security:**
        - Firewall integration
        - IPS/IDS placement
        - Security level controls
        - Compliance-ready designs
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 20px;'>
    <p><b>Cisco Network Topology Simulator</b> | AI-Powered Network Design Tool</p>
    <p>Built for cybersecurity professionals, network engineers, and IT architects</p>
</div>
""", unsafe_allow_html=True)
