''' Test Kubernetes_api.py methods '''

import os
import sys
import unittest
from unittest.mock import patch, Mock
import web_service.kub.KubernetesAPI as ut
from web_service.ontap.ontap_service import OntapService as ontap

# Set project root directory so coverage.py can generate coverage
BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class TestKubernetesAPIMethods(unittest.TestCase):
    ''' Test Kubernetes API '''
    def setUp(self):
        self.kube_api = ut.KubernetesAPI("12345", "abcdef")

    def test_create_pv_config(self):
        ''' Test helper to create config dictionary '''
        expected_config = {
            "apiVersion": "v1",
            "kind": "PersistentVolume",
            "metadata": {
                "name": "api-test-vol-2-pv",
                "labels": {
                    "netapp-use": "api-test-vol-2-vol"
                    }
                },
            "spec": {
                "capacity": {
                    "storage": "100000M"
                    },
                "accessModes": ["ReadWriteMany"],
                "nfs": {
                    "server": "169.47.240.183",
                    "path": "/api_test_vol_2"
                    }
                }
            }

        result_config = self.kube_api.create_pv_config("api-test-vol-2", 100000, "169.47.240.183")
        self.assertEqual(expected_config, result_config)

    def test_create_pvc_config(self):
        ''' Test helper to create config dictionary '''
        expected_config = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "name": "create-test-pvc",
                "annotations": {
                    "volume.beta.kubernetes.io/storage-class": ""
                    }
                },
            "spec":{
                "accessModes": [
                    "ReadWriteMany"
                    ],
                "resources": {
                    "requests": {
                        "storage": 100000
                        }
                    },
                "selector":{
                    "matchLabels": {
                        "netapp-use": "create-test-vol"
                        }
                    }
                }
            }

        result_config = self.kube_api.create_pvc_config("create-test", 100000)

        self.assertEqual(expected_config, result_config)

    def test_set_status(self):
        '''Test helper to create status dictionary'''
        expected_status = {
            'resource': 'Volume',
            'resource_name': 'test-vol',
            'code': 200,
            'status': 'SUCCESS',
            'message': 'Volume test-vol already exists',
            'error_message': ''
        }

        attempted_status = ontap.set_status(200, 'Volume', 'test-vol')
        self.assertEqual(expected_status, attempted_status)

    def test_set_status_for_failure(self):
        '''Test helper to create status dictionary'''
        expected_status = {
            'resource': 'Volume',
            'resource_name': 'test-vol',
            'code': 400,
            'status': 'FAILED',
            'message': '',
            'error_message': 'Error creating PV'
        }

        attempted_status = ontap.set_status(400, 'Volume', 'test-vol', 'Error creating PV')
        self.assertEqual(expected_status, attempted_status)

    # disable unit test until mock bug is fixed
    # @patch('web_service.kub.KubernetesAPI.KubernetesAPI.get_worker_node')
    # @patch('kubernetes.client.CoreV1Api.read_namespaced_service')
    # def test_get_service_url(
    #         self, mock_read_namespaced_service, mock_get_worker_node):
    #     '''Test get_service_url function '''
    #     mock_node = "kube-worker-node-01.devops.com"
    #     mock_get_worker_node.return_value = mock_node
    #     mock_read_namespaced_service.return_value = {
    #         'api_version': 'v1',
    #         'kind': 'Service',
    #         'metadata': {'annotations': None,
    #                      'cluster_name': None,
    #                      'labels': {'component': 'apiserver', 'provider': 'kubernetes'},
    #                      'name': 'kubernetes',
    #                      'namespace': 'default',
    #                      'owner_references': None,
    #                      'resource_version': '91',
    #                      'self_link': '/api/v1/namespaces/default/services/kubernetes',
    #                      'uid': '47ce8895-d941-11e7-ba12-00505693776b'},
    #         'spec': {'cluster_ip': '10.96.0.1',
    #                  'external_i_ps': None,
    #                  'ports': [{'name': 'https',
    #                             'node_port': 31455,
    #                             'port': 443,
    #                             'protocol': 'TCP',
    #                             'target_port': 6443}],
    #                  'publish_not_ready_addresses': None,
    #                  'selector': None,
    #                  'session_affinity': 'ClientIP',
    #                  'session_affinity_config': {'client_ip': {'timeout_seconds': 10800}},
    #                  'type': 'ClusterIP'},
    #         'status': {'load_balancer': {'ingress': None}}
    #     }
    #
    #     service_name = 'kubernetes'
    #     result = self.kube_api.get_service_url(service_name)
    #     self.assertEqual(result, "%s:%s" % (mock_node, "31455"))

if __name__ == '__main__':
    unittest.main()
    unittest.TestLoader().loadTestsFromTestCase(TestKubernetesAPIMethods)
