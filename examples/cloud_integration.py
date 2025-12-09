"""
Example: Cloud Integration
Demonstrates hybrid cloud network design
"""

from src.topology_generator import NetworkTopologyGenerator
from src.cloud_integrator import CloudNetworkBuilder
import json


def main():
    print("=" * 60)
    print("Cloud Network Integration Example")
    print("=" * 60)
    
    # Generate on-premise network
    print("\n1. Creating on-premise network...")
    generator = NetworkTopologyGenerator()
    on_premise = generator.generate_topology(
        network_type="enterprise",
        num_routers=2,
        num_switches=4,
        num_hosts=20,
        security_level="high"
    )
    
    print(f"✓ On-premise network created")
    print(f"  - Devices: {on_premise['total_devices']}")
    
    # AWS Integration
    print("\n2. Integrating with AWS...")
    cloud_builder = CloudNetworkBuilder()
    aws_hybrid = cloud_builder.create_hybrid_topology(
        on_premise=on_premise,
        cloud_provider="aws",
        integration_type="site-to-site vpn",
        vpn_encryption="AES-256",
        bandwidth=1000
    )
    
    print(f"✓ AWS integration configured")
    print(f"  - VPC ID: {aws_hybrid['cloud_resources']['vpc']['vpc_id']}")
    print(f"  - VPN Gateway: {aws_hybrid['cloud_resources']['vpn_gateway']['gateway_id']}")
    print(f"  - Estimated latency: {aws_hybrid['estimated_latency']}")
    print(f"  - Monthly cost: {aws_hybrid['cost_estimate']['total_monthly']}")
    
    # Azure Integration
    print("\n3. Integrating with Azure...")
    azure_hybrid = cloud_builder.create_hybrid_topology(
        on_premise=on_premise,
        cloud_provider="azure",
        integration_type="site-to-site vpn",
        vpn_encryption="AES-256",
        bandwidth=1000
    )
    
    print(f"✓ Azure integration configured")
    print(f"  - VNet ID: {azure_hybrid['cloud_resources']['virtual_network']['vnet_id']}")
    print(f"  - VPN Gateway: {azure_hybrid['cloud_resources']['vpn_gateway']['gateway_id']}")
    print(f"  - Monthly cost: {azure_hybrid['cost_estimate']['total_monthly']}")
    
    # GCP Integration
    print("\n4. Integrating with GCP...")
    gcp_hybrid = cloud_builder.create_hybrid_topology(
        on_premise=on_premise,
        cloud_provider="gcp",
        integration_type="site-to-site vpn",
        vpn_encryption="AES-256",
        bandwidth=1000
    )
    
    print(f"✓ GCP integration configured")
    print(f"  - VPC Network: {gcp_hybrid['cloud_resources']['vpc_network']['network_id']}")
    print(f"  - VPN Gateway: {gcp_hybrid['cloud_resources']['vpn_gateway']['gateway_id']}")
    print(f"  - Monthly cost: {gcp_hybrid['cost_estimate']['total_monthly']}")
    
    # Cost comparison
    print("\n5. Cost Comparison:")
    print(f"  - AWS:   {aws_hybrid['cost_estimate']['total_monthly']}/month")
    print(f"  - Azure: {azure_hybrid['cost_estimate']['total_monthly']}/month")
    print(f"  - GCP:   {gcp_hybrid['cost_estimate']['total_monthly']}/month")
    
    # Save configurations
    print("\n6. Saving configurations...")
    
    with open('aws_hybrid_config.json', 'w') as f:
        json.dump(aws_hybrid, f, indent=2)
    print("✓ Saved AWS configuration")
    
    with open('azure_hybrid_config.json', 'w') as f:
        json.dump(azure_hybrid, f, indent=2)
    print("✓ Saved Azure configuration")
    
    with open('gcp_hybrid_config.json', 'w') as f:
        json.dump(gcp_hybrid, f, indent=2)
    print("✓ Saved GCP configuration")
    
    print("\n" + "=" * 60)
    print("Cloud integration example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
