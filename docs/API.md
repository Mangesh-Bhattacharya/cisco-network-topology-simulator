# API Documentation

## NetworkTopologyGenerator

### Class: `NetworkTopologyGenerator`

Generate network topologies with AI optimization.

#### Methods

##### `generate_topology()`

Generate network topology based on parameters.

**Parameters:**
- `network_type` (str): Type of network - "enterprise", "datacenter", "campus", "cloud", "hybrid"
- `num_routers` (int): Number of routers (default: 5)
- `num_switches` (int): Number of switches (default: 10)
- `num_hosts` (int): Number of end hosts (default: 50)
- `security_level` (str): Security level - "low", "medium", "high", "critical"
- `redundancy` (bool): Enable redundant paths (default: True)
- `ai_optimize` (bool): Use AI for optimization (default: True)

**Returns:**
- `Dict`: Topology data containing devices, links, and metadata

**Example:**
```python
from src.topology_generator import NetworkTopologyGenerator

generator = NetworkTopologyGenerator()
topology = generator.generate_topology(
    network_type="enterprise",
    num_routers=5,
    num_switches=10,
    num_hosts=50,
    security_level="high",
    redundancy=True
)
```

---

## SecurityAuditor

### Class: `SecurityAuditor`

Network security auditing and compliance checking.

#### Methods

##### `run_audit()`

Run comprehensive security audit.

**Parameters:**
- `audit_types` (List[str]): Types of audits - ["Vulnerability Scan", "Configuration Audit", "Penetration Test", "CVE Database Check"]
- `compliance_standards` (List[str]): Standards - ["PCI-DSS", "HIPAA", "ISO 27001", "NIST", "SOC 2"]

**Returns:**
- `Dict`: Audit report with vulnerabilities, compliance results, and recommendations

**Example:**
```python
from src.security_auditor import SecurityAuditor

auditor = SecurityAuditor(topology)
report = auditor.run_audit(
    audit_types=["Vulnerability Scan", "Compliance Check"],
    compliance_standards=["ISO 27001", "PCI-DSS"]
)

print(f"Security Score: {report['security_score']}/100")
```

---

## CloudNetworkBuilder

### Class: `CloudNetworkBuilder`

Build hybrid cloud network architectures.

#### Methods

##### `create_hybrid_topology()`

Create hybrid cloud network topology.

**Parameters:**
- `on_premise` (Dict): On-premise network topology
- `cloud_provider` (str): Cloud provider - "aws", "azure", "gcp"
- `integration_type` (str): Integration type - "site-to-site vpn", "direct connect", "hybrid cloud"
- `vpn_encryption` (str): VPN encryption - "AES-256", "AES-128"
- `bandwidth` (int): Bandwidth in Mbps

**Returns:**
- `Dict`: Hybrid network configuration

**Example:**
```python
from src.cloud_integrator import CloudNetworkBuilder

cloud_builder = CloudNetworkBuilder()
hybrid = cloud_builder.create_hybrid_topology(
    on_premise=topology,
    cloud_provider="aws",
    integration_type="site-to-site vpn",
    vpn_encryption="AES-256",
    bandwidth=1000
)
```

---

## NetworkAnalytics

### Class: `NetworkAnalytics`

Analyze network performance and generate insights.

#### Methods

##### `analyze()`

Perform comprehensive network analysis.

**Returns:**
- `Dict`: Analytics data with performance metrics, traffic analysis, capacity planning

**Example:**
```python
from src.analytics_engine import NetworkAnalytics

analytics = NetworkAnalytics(topology)
data = analytics.analyze()

print(f"Average Latency: {data['performance_metrics']['average_latency_ms']}ms")
print(f"Throughput: {data['performance_metrics']['throughput_gbps']}Gbps")
```

---

## PacketTracerExporter

### Class: `PacketTracerExporter`

Export network topology to various formats.

#### Methods

##### `export_to_pkt()`

Export topology to Cisco Packet Tracer format.

**Parameters:**
- `include_configs` (bool): Include device configurations (default: True)
- `include_docs` (bool): Include documentation (default: True)

**Returns:**
- `bytes`: Binary data for .pkt file

**Example:**
```python
from src.packet_tracer_exporter import PacketTracerExporter

exporter = PacketTracerExporter(topology)
pkt_data = exporter.export_to_pkt(
    include_configs=True,
    include_docs=True
)

with open('network.pkt', 'wb') as f:
    f.write(pkt_data)
```

---

## Data Structures

### Topology Dictionary

```python
{
    'network_type': str,
    'devices': List[Dict],
    'links': List[Dict],
    'total_devices': int,
    'total_links': int,
    'segments': int,
    'security_level': str,
    'redundancy_enabled': bool,
    'ai_optimized': bool,
    'metadata': Dict
}
```

### Device Dictionary

```python
{
    'name': str,
    'type': str,  # 'router', 'switch', 'host', 'firewall', 'ips'
    'subtype': str,
    'model': str,
    'ip_address': str,
    'interfaces': List[Dict],
    'management_ip': str
}
```

### Link Dictionary

```python
{
    'source': str,
    'target': str,
    'type': str,
    'bandwidth': str
}
```

### Security Report Dictionary

```python
{
    'timestamp': str,
    'vulnerabilities': List[Dict],
    'compliance': Dict,
    'recommendations': List[str],
    'security_score': int
}
```

---

## Error Handling

All methods may raise the following exceptions:

- `ValueError`: Invalid parameter values
- `TypeError`: Invalid parameter types
- `RuntimeError`: Runtime errors during generation/analysis

**Example:**
```python
try:
    topology = generator.generate_topology(num_routers=-1)
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

---

## Best Practices

1. **Always validate input parameters** before calling methods
2. **Handle exceptions** appropriately in production code
3. **Use context managers** when working with files
4. **Cache topology data** to avoid regeneration
5. **Run security audits** after topology generation
6. **Export configurations** for backup and documentation

---

## Performance Considerations

- Large topologies (>500 devices) may take several seconds to generate
- Security audits scale linearly with device count
- AI optimization adds ~20% overhead but improves topology quality
- Export operations are I/O bound

---

## Version Compatibility

- Python: 3.9+
- Streamlit: 1.28+
- NetworkX: 3.1+

---

## Support

For API questions or issues:
- GitHub Issues: https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator/issues
- Email: mangesh.bhattacharya@ontariotechu.net
