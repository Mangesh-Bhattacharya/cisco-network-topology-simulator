import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from src.topology_generator import NetworkTopologyGenerator
import json
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Cisco Network Topology Simulator",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state
if 'topology' not in st.session_state:
    st.session_state.topology = None
if 'generator' not in st.session_state:
    st.session_state.generator = None

st.title("🌐 Cisco Network Topology Simulator")
st.markdown("Generate professional Cisco-style network topology diagrams")

# Sidebar configuration
st.sidebar.header("Topology Configuration")

network_type = st.sidebar.selectbox(
    "Network Type",
    ["enterprise", "datacenter", "campus", "cloud", "hybrid"]
)

num_routers = st.sidebar.slider("Number of Routers", 1, 10, 3)
num_switches = st.sidebar.slider("Number of Switches", 2, 20, 6)
num_hosts = st.sidebar.slider("Number of Hosts", 5, 50, 20)

security_level = st.sidebar.selectbox(
    "Security Level",
    ["low", "medium", "high", "critical"]
)

redundancy = st.sidebar.checkbox("Enable Redundancy", value=True)
ai_optimize = st.sidebar.checkbox("AI Optimization", value=True)
show_labels = st.sidebar.checkbox("Show Interface Labels", value=True)

if st.sidebar.button("Generate Topology", type="primary"):
    with st.spinner("Generating network topology..."):
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
            st.error(f"❌ Error: {str(e)}")

def get_device_icon_data_uri(device_type):
    """Return data URI for device icons using Unicode/emoji fallback"""
    
    # Icon mappings using Unicode symbols
    icon_map = {
        'router': '🛜',  # Router icon
        'switch': '🔀',  # Switch icon
        'host': '💻',    # PC icon
        'firewall': '🧱', # Firewall icon
        'ips': '🔒',     # IPS icon
        'cloud': '☁️'    # Cloud icon
    }
    
    return icon_map.get(device_type, '📦')

def create_hierarchical_layout(topology):
    """Create organized hierarchical layout"""
    
    devices = topology['devices']
    
    # Group devices
    routers = [d for d in devices if d['type'] == 'router']
    switches = [d for d in devices if d['type'] == 'switch']
    hosts = [d for d in devices if d['type'] == 'host']
    security = [d for d in devices if d['type'] in ['firewall', 'ips']]
    
    dist_switches = [s for s in switches if 'distribution' in s.get('subtype', '')]
    access_switches = [s for s in switches if 'access' in s.get('subtype', '')]
    
    pos = {}
    
    # Calculate spacing
    h_space = 4  # Horizontal spacing
    v_space = 3  # Vertical spacing
    
    # Layer 1: Routers (top layer)
    y_router = 5 * v_space
    if routers:
        total_width = len(routers) * h_space
        start_x = -total_width / 2
        for i, router in enumerate(routers):
            pos[router['name']] = (start_x + i * h_space, y_router)
    
    # Layer 2: Security devices
    y_security = 4 * v_space
    if security:
        total_width = len(security) * h_space
        start_x = -total_width / 2
        for i, dev in enumerate(security):
            pos[dev['name']] = (start_x + i * h_space, y_security)
    
    # Layer 3: Distribution switches
    y_dist = 3 * v_space
    if dist_switches:
        total_width = len(dist_switches) * h_space
        start_x = -total_width / 2
        for i, sw in enumerate(dist_switches):
            pos[sw['name']] = (start_x + i * h_space, y_dist)
    
    # Layer 4: Access switches
    y_access = 2 * v_space
    if access_switches:
        total_width = len(access_switches) * h_space
        start_x = -total_width / 2
        for i, sw in enumerate(access_switches):
            pos[sw['name']] = (start_x + i * h_space, y_access)
    
    # Layer 5: Hosts
    y_host = 1 * v_space
    max_display = min(len(hosts), 25)
    if hosts:
        h_space_host = 2.5
        total_width = max_display * h_space_host
        start_x = -total_width / 2
        for i, host in enumerate(hosts[:max_display]):
            pos[host['name']] = (start_x + i * h_space_host, y_host)
    
    return pos

def create_cisco_diagram(topology, show_labels=True):
    """Create professional Cisco network diagram"""
    
    G = nx.Graph()
    
    # Build graph
    for device in topology['devices']:
        G.add_node(device['name'], **device)
    
    for link in topology['links']:
        G.add_edge(link['source'], link['target'], **link)
    
    pos = create_hierarchical_layout(topology)
    
    # Create figure
    fig = go.Figure()
    
    # Draw connection lines first (background layer)
    for edge in G.edges():
        if edge[0] not in pos or edge[1] not in pos:
            continue
        
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # Add connection line
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color='#2C3E50', width=2),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Add bandwidth label on link
        if show_labels:
            edge_data = G.edges[edge]
            bandwidth = edge_data.get('bandwidth', '')
            if bandwidth:
                mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
                fig.add_trace(go.Scatter(
                    x=[mid_x],
                    y=[mid_y],
                    mode='text',
                    text=[bandwidth],
                    textfont=dict(size=9, color='#E74C3C', family='Courier New, monospace'),
                    textposition='middle center',
                    hoverinfo='none',
                    showlegend=False
                ))
    
    # Draw device nodes with icons
    for node in G.nodes():
        if node not in pos:
            continue
        
        x, y = pos[node]
        node_data = G.nodes[node]
        device_type = node_data['type']
        ip_addr = node_data.get('ip_address', '')
        
        # Get icon
        icon = get_device_icon_data_uri(device_type)
        
        # Add device icon as text
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='text',
            text=[icon],
            textfont=dict(size=40),
            hovertext=f"<b>{node}</b><br>Type: {device_type}<br>IP: {ip_addr}",
            hoverinfo='text',
            showlegend=False
        ))
        
        # Add device name label
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y - 0.5],
            mode='text',
            text=[f"<b>{node}</b>"],
            textfont=dict(size=10, color='#2C3E50', family='Arial'),
            textposition='bottom center',
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Add IP address label
        if device_type in ['router', 'switch', 'firewall', 'ips']:
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y - 0.8],
                mode='text',
                text=[ip_addr],
                textfont=dict(size=8, color='#7F8C8D', family='Courier New'),
                textposition='bottom center',
                hoverinfo='skip',
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{topology['network_type'].title()} Network Topology</b>",
            font=dict(size=22, color='#2C3E50', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-20, 20]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 18]
        ),
        height=900,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    return fig

# Main display
if st.session_state.topology is not None:
    topology = st.session_state.topology
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Devices", topology['total_devices'])
    with col2:
        st.metric("🔗 Total Links", topology['total_links'])
    with col3:
        st.metric("🌐 Network Segments", topology['segments'])
    with col4:
        st.metric("🛡️ Security Devices", topology['metadata']['security_devices'])
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Topology Diagram", "📋 Devices", "🔗 Links", "💾 Export"])
    
    with tab1:
        st.subheader("Professional Cisco Network Diagram")
        
        try:
            fig = create_cisco_diagram(topology, show_labels)
            st.plotly_chart(fig, use_container_width=True)
            
            # Legend
            st.markdown("---")
            st.markdown("### Legend")
            cols = st.columns(5)
            with cols[0]:
                st.markdown("⛀ **Router**")
            with cols[1]:
                st.markdown("[▣▣▣▣▣⭘] **Switch**")
            with cols[2]:
                st.markdown("💻 **Host/PC**")
            with cols[3]:
                st.markdown("🧱 **Firewall**")
            with cols[4]:
                st.markdown("🔒 **IPS**")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab2:
        st.subheader("Device Inventory")
        import pandas as pd
        
        devices_df = pd.DataFrame(topology['devices'])
        st.dataframe(devices_df[['name', 'type', 'ip_address', 'model']], 
                    use_container_width=True, height=400)
    
    with tab3:
        st.subheader("Network Links")
        import pandas as pd
        
        links_df = pd.DataFrame(topology['links'])
        st.dataframe(links_df, use_container_width=True, height=400)
    
    with tab4:
        st.subheader("Export Topology")
        
        if st.session_state.generator:
            json_data = st.session_state.generator.get_topology_json()
            st.download_button(
                "📥 Download JSON",
                json_data,
                "network_topology.json",
                "application/json"
            )
            
            st.markdown("### Configuration Summary")
            st.json({
                'network_type': topology['network_type'],
                'total_devices': topology['total_devices'],
                'total_links': topology['total_links'],
                'security_level': topology['security_level']
            })

else:
    st.info("👈 Configure and generate your network topology using the sidebar")
    
    st.markdown("### 📚 Quick Start Examples")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🏢 Small Office\n- 2 Routers\n- 4 Switches\n- 20 Hosts")
    with col2:
        st.markdown("#### 🏭 Enterprise\n- 5 Routers\n- 10 Switches\n- 50 Hosts")
    with col3:
        st.markdown("#### 🖥️ Data Center\n- 10 Routers\n- 20 Switches\n- 100 Hosts")
