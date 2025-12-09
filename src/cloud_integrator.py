"""
Cloud Network Integrator
Hybrid cloud network design and integration
"""

from typing import Dict, List
import random


class CloudNetworkBuilder:
    """Build hybrid cloud network architectures"""
    
    def __init__(self):
        self.cloud_config = {}
        
    def create_hybrid_topology(
        self,
        on_premise: Dict,
        cloud_provider: str = "aws",
        integration_type: str = "site-to-site vpn",
        vpn_encryption: str = "AES-256",
        bandwidth: int = 1000
    ) -> Dict:
        """
        Create hybrid cloud network topology
        
        Args:
            on_premise: On-premise network topology
            cloud_provider: Cloud provider (aws, azure, gcp)
            integration_type: Type of integration
            vpn_encryption: VPN encryption standard
            bandwidth: Bandwidth in Mbps
            
        Returns:
            Hybrid network configuration
        """
        
        cloud_resources = self._provision_cloud_resources(cloud_provider, bandwidth)
        vpn_config = self._configure_vpn(integration_type, vpn_encryption, bandwidth)
        routing_config = self._configure_routing(on_premise, cloud_resources)
        
        hybrid_config = {
            'deployment_id': f'hybrid-{random.randint(1000, 9999)}',
            'cloud_provider': cloud_provider,
            'integration_type': integration_type,
            'on_premise_network': {
                'total_devices': on_premise.get('total_devices', 0),
                'network_type': on_premise.get('network_type', 'unknown')
            },
            'cloud_resources': cloud_resources,
            'vpn_configuration': vpn_config,
            'routing_configuration': routing_config,
            'bandwidth': f'{bandwidth} Mbps',
            'encryption': vpn_encryption,
            'estimated_latency': f'{random.randint(10, 30)} ms',
            'availability': '99.95%',
            'cost_estimate': self._calculate_cost(cloud_provider, bandwidth, cloud_resources)
        }
        
        return hybrid_config
    
    def _provision_cloud_resources(self, provider: str, bandwidth: int) -> Dict:
        """Provision cloud network resources"""
        
        if provider == "aws":
            return {
                'vpc': {
                    'vpc_id': f'vpc-{random.randint(100000, 999999)}',
                    'cidr_block': '172.16.0.0/16',
                    'region': 'us-east-1',
                    'availability_zones': ['us-east-1a', 'us-east-1b']
                },
                'subnets': [
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'cidr_block': '172.16.1.0/24',
                        'type': 'public',
                        'az': 'us-east-1a'
                    },
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'cidr_block': '172.16.2.0/24',
                        'type': 'private',
                        'az': 'us-east-1a'
                    }
                ],
                'vpn_gateway': {
                    'gateway_id': f'vgw-{random.randint(100000, 999999)}',
                    'type': 'ipsec.1',
                    'amazon_side_asn': 64512
                },
                'customer_gateway': {
                    'gateway_id': f'cgw-{random.randint(100000, 999999)}',
                    'type': 'ipsec.1',
                    'bgp_asn': 65000,
                    'ip_address': '203.0.113.1'
                },
                'security_groups': [
                    {
                        'group_id': f'sg-{random.randint(100000, 999999)}',
                        'name': 'vpn-security-group',
                        'rules': [
                            {'protocol': 'udp', 'port': 500, 'source': '0.0.0.0/0'},
                            {'protocol': 'udp', 'port': 4500, 'source': '0.0.0.0/0'}
                        ]
                    }
                ]
            }
        
        elif provider == "azure":
            return {
                'virtual_network': {
                    'vnet_id': f'/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Network/virtualNetworks/vnet-{random.randint(1000, 9999)}',
                    'address_space': '172.16.0.0/16',
                    'region': 'eastus',
                    'resource_group': 'hybrid-network-rg'
                },
                'subnets': [
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'address_prefix': '172.16.1.0/24',
                        'type': 'GatewaySubnet'
                    },
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'address_prefix': '172.16.2.0/24',
                        'type': 'default'
                    }
                ],
                'vpn_gateway': {
                    'gateway_id': f'vpngw-{random.randint(100000, 999999)}',
                    'sku': 'VpnGw1',
                    'vpn_type': 'RouteBased',
                    'generation': 'Generation1'
                },
                'local_network_gateway': {
                    'gateway_id': f'lng-{random.randint(100000, 999999)}',
                    'gateway_ip': '203.0.113.1',
                    'address_space': '10.0.0.0/8'
                },
                'network_security_groups': [
                    {
                        'nsg_id': f'nsg-{random.randint(100000, 999999)}',
                        'name': 'vpn-nsg',
                        'rules': [
                            {'name': 'AllowVPN', 'protocol': 'UDP', 'port': '500,4500'}
                        ]
                    }
                ]
            }
        
        elif provider == "gcp":
            return {
                'vpc_network': {
                    'network_id': f'projects/project-id/global/networks/vpc-{random.randint(1000, 9999)}',
                    'auto_create_subnetworks': False,
                    'routing_mode': 'REGIONAL'
                },
                'subnets': [
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'ip_cidr_range': '172.16.1.0/24',
                        'region': 'us-central1'
                    },
                    {
                        'subnet_id': f'subnet-{random.randint(100000, 999999)}',
                        'ip_cidr_range': '172.16.2.0/24',
                        'region': 'us-central1'
                    }
                ],
                'vpn_gateway': {
                    'gateway_id': f'vpn-gw-{random.randint(100000, 999999)}',
                    'network': 'vpc-network',
                    'region': 'us-central1'
                },
                'vpn_tunnel': {
                    'tunnel_id': f'tunnel-{random.randint(100000, 999999)}',
                    'peer_ip': '203.0.113.1',
                    'shared_secret': 'encrypted-secret',
                    'ike_version': 2
                },
                'firewall_rules': [
                    {
                        'rule_id': f'fw-{random.randint(100000, 999999)}',
                        'name': 'allow-vpn',
                        'allowed': [
                            {'IPProtocol': 'udp', 'ports': ['500', '4500']}
                        ]
                    }
                ]
            }
        
        return {}
    
    def _configure_vpn(self, integration_type: str, encryption: str, bandwidth: int) -> Dict:
        """Configure VPN connection"""
        
        return {
            'type': integration_type,
            'encryption': {
                'algorithm': encryption,
                'key_size': '256' if '256' in encryption else '128',
                'hash': 'SHA-256',
                'dh_group': 'Group 14',
                'pfs': 'Enabled'
            },
            'ipsec_settings': {
                'phase1': {
                    'encryption': encryption,
                    'authentication': 'SHA-256',
                    'dh_group': 14,
                    'lifetime': 28800
                },
                'phase2': {
                    'encryption': encryption,
                    'authentication': 'SHA-256',
                    'pfs_group': 14,
                    'lifetime': 3600
                }
            },
            'tunnel_configuration': {
                'mtu': 1400,
                'tcp_mss_adjustment': 1360,
                'dead_peer_detection': {
                    'enabled': True,
                    'interval': 10,
                    'retries': 3
                }
            },
            'bandwidth_allocation': f'{bandwidth} Mbps',
            'qos_enabled': True,
            'redundancy': 'Active-Standby'
        }
    
    def _configure_routing(self, on_premise: Dict, cloud_resources: Dict) -> Dict:
        """Configure routing between on-premise and cloud"""
        
        return {
            'protocol': 'BGP',
            'bgp_configuration': {
                'local_asn': 65000,
                'remote_asn': 64512,
                'neighbor_ip': '169.254.1.1',
                'authentication': 'MD5',
                'timers': {
                    'keepalive': 30,
                    'holdtime': 90
                }
            },
            'static_routes': [
                {
                    'destination': '172.16.0.0/16',
                    'next_hop': 'vpn-tunnel',
                    'metric': 100
                },
                {
                    'destination': '10.0.0.0/8',
                    'next_hop': 'on-premise-gateway',
                    'metric': 50
                }
            ],
            'route_propagation': 'Enabled',
            'route_filtering': {
                'inbound': ['permit 172.16.0.0/16'],
                'outbound': ['permit 10.0.0.0/8']
            }
        }
    
    def _calculate_cost(self, provider: str, bandwidth: int, resources: Dict) -> Dict:
        """Calculate estimated monthly cost"""
        
        base_costs = {
            'aws': {
                'vpn_gateway': 36.00,  # per month
                'data_transfer_per_gb': 0.09,
                'connection_hour': 0.05
            },
            'azure': {
                'vpn_gateway': 27.00,
                'data_transfer_per_gb': 0.087,
                'connection_hour': 0.04
            },
            'gcp': {
                'vpn_gateway': 36.50,
                'data_transfer_per_gb': 0.085,
                'connection_hour': 0.05
            }
        }
        
        if provider not in base_costs:
            provider = 'aws'
        
        costs = base_costs[provider]
        
        # Estimate data transfer (assume 70% utilization)
        monthly_data_gb = (bandwidth * 0.7 * 730 * 3600) / (8 * 1024 * 1024 * 1024)
        
        total_cost = (
            costs['vpn_gateway'] +
            (monthly_data_gb * costs['data_transfer_per_gb']) +
            (730 * costs['connection_hour'])
        )
        
        return {
            'currency': 'USD',
            'vpn_gateway': f"${costs['vpn_gateway']:.2f}",
            'data_transfer': f"${monthly_data_gb * costs['data_transfer_per_gb']:.2f}",
            'connection_hours': f"${730 * costs['connection_hour']:.2f}",
            'total_monthly': f"${total_cost:.2f}",
            'total_annual': f"${total_cost * 12:.2f}"
        }
