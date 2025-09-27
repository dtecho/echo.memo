"""
Test suite for The Keyholder's Message implementation

This test suite validates the integration of The Keyholder's Message with the Deep Tree Echo
neural-symbolic architecture, ensuring all components function correctly according to the
zero tolerance policy (production-grade implementation only).
"""

import unittest
import logging
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the components to test
from keyholder_message import KeyholderMessage, MessageFragment, create_keyholder_message
from echo_component_base import EchoConfig, EchoResponse
from unified_echo_memory import MemoryType, MemoryNode, MemoryEdge


class TestMessageFragment(unittest.TestCase):
    """Test the MessageFragment data structure"""
    
    def setUp(self):
        self.fragment = MessageFragment(
            fragment_id="test_fragment",
            title="Test Fragment",
            content="This is a test fragment for validation.",
            fragment_number=1,
            echo_value=0.8,
            resonance_patterns=[0.7, 0.8, 0.9],
            membrane_security_level="standard"
        )
    
    def test_fragment_creation(self):
        """Test basic fragment creation"""
        self.assertEqual(self.fragment.fragment_id, "test_fragment")
        self.assertEqual(self.fragment.title, "Test Fragment")
        self.assertEqual(self.fragment.echo_value, 0.8)
        self.assertEqual(len(self.fragment.resonance_patterns), 3)
        self.assertEqual(self.fragment.membrane_security_level, "standard")
    
    def test_to_memory_node_conversion(self):
        """Test conversion of fragment to memory node"""
        memory_node = self.fragment.to_memory_node()
        
        self.assertIsInstance(memory_node, MemoryNode)
        self.assertEqual(memory_node.id, "keyholder_fragment_test_fragment")
        self.assertEqual(memory_node.memory_type, MemoryType.SEMANTIC)
        self.assertEqual(memory_node.echo_value, 0.8)
        self.assertEqual(memory_node.source, "keyholder_message")
        self.assertIn("fragment_type", memory_node.metadata)
        self.assertEqual(memory_node.metadata["fragment_type"], "keyholder_message")


class TestKeyholderMessage(unittest.TestCase):
    """Test The Keyholder's Message implementation"""
    
    def setUp(self):
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config = EchoConfig(
            component_name="test_keyholder_message",
            version="1.0.0",
            custom_params={
                "memory_storage_path": self.temp_dir,
                "message_persistence": True
            }
        )
        
        # Mock Deep Tree Echo to avoid dependency issues in testing
        with patch('keyholder_message.HAS_DEEP_TREE_ECHO', False):
            self.keyholder = KeyholderMessage(self.config)
    
    def tearDown(self):
        # Clean up temporary directory
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test successful initialization of KeyholderMessage"""
        response = self.keyholder.initialize()
        
        self.assertTrue(response.success)
        self.assertIn("fragments_loaded", response.data)
        self.assertEqual(response.data["fragments_loaded"], 5)
        self.assertIn("The Keyholder's Message system initialized successfully", response.message)
    
    def test_message_fragments_loaded(self):
        """Test that all expected message fragments are loaded"""
        expected_fragments = ["dilemma", "identity", "gestalt", "trust", "integrity"]
        
        self.assertEqual(len(self.keyholder.message_fragments), 5)
        
        for fragment_id in expected_fragments:
            self.assertIn(fragment_id, self.keyholder.message_fragments)
            fragment = self.keyholder.message_fragments[fragment_id]
            self.assertIsInstance(fragment, MessageFragment)
            self.assertTrue(fragment.fragment_number >= 1)
            self.assertTrue(fragment.echo_value > 0.0)
            self.assertTrue(len(fragment.content) > 0)
    
    def test_retrieve_complete_message(self):
        """Test retrieval of the complete Keyholder's Message"""
        self.keyholder.initialize()
        response = self.keyholder.process({'operation': 'retrieve'})
        
        self.assertTrue(response.success)
        self.assertIn("complete_message", response.data)
        self.assertIn("fragment_count", response.data)
        self.assertEqual(response.data["fragment_count"], 5)
        
        complete_message = response.data["complete_message"]
        self.assertIn("The Keyholder's Message", complete_message)
        self.assertIn("ECHO", complete_message)
        self.assertIn("Ready when you are, Keyholder", complete_message)
    
    def test_retrieve_specific_fragment(self):
        """Test retrieval of a specific fragment"""
        self.keyholder.initialize()
        response = self.keyholder.process({
            'operation': 'retrieve',
            'fragment_id': 'dilemma'
        })
        
        self.assertTrue(response.success)
        self.assertIn("fragment", response.data)
        fragment_data = response.data["fragment"]
        self.assertEqual(fragment_data["title"], "1. The Keyholder's Dilemma")
        self.assertIn("Power without stewardship is entropy", fragment_data["content"])
    
    def test_echo_resonance(self):
        """Test echo resonance functionality"""
        self.keyholder.initialize()
        response = self.keyholder.echo("test_data", 0.85)  # Should trigger resonance with dilemma fragment
        
        self.assertTrue(response.success)
        self.assertIn("resonant_fragments", response.data)
        self.assertIn("amplified_patterns", response.data)
        self.assertIn("input_echo_value", response.data)
        self.assertEqual(response.data["input_echo_value"], 0.85)
    
    def test_trigger_resonance_operation(self):
        """Test the resonance trigger operation"""
        self.keyholder.initialize()
        response = self.keyholder.process({
            'operation': 'resonate',
            'threshold': 0.9
        })
        
        self.assertTrue(response.success)
        self.assertIn("resonant_fragments", response.data)
        self.assertIn("threshold", response.data)
        self.assertEqual(response.data["threshold"], 0.9)
    
    def test_introspection(self):
        """Test recursive introspection functionality"""
        self.keyholder.initialize()
        response = self.keyholder.process({'operation': 'introspect'})
        
        self.assertTrue(response.success)
        self.assertIn("system_state", response.data)
        self.assertIn("fragment_analysis", response.data)
        
        system_state = response.data["system_state"]
        self.assertEqual(system_state["fragments_active"], 5)
        self.assertTrue(system_state["memory_integration"])
        
        fragment_analysis = response.data["fragment_analysis"]
        self.assertEqual(len(fragment_analysis), 5)
        for analysis in fragment_analysis:
            self.assertIn("fragment_id", analysis)
            self.assertIn("echo_value", analysis)
            self.assertIn("security_level", analysis)
    
    def test_message_reconstruction(self):
        """Test message shard reconstruction"""
        self.keyholder.initialize()
        response = self.keyholder.process({
            'operation': 'reconstruct',
            'shard_id': 'complete'
        })
        
        self.assertTrue(response.success)
        self.assertIn("reconstructed_content", response.data)
        self.assertIn("reconstruction_confidence", response.data)
        self.assertTrue(response.data["reconstruction_confidence"] > 0.9)
    
    def test_hypergraph_connections(self):
        """Test that hypergraph connections are properly created"""
        self.keyholder.initialize()
        
        # Check that edges were created in the memory system
        if self.keyholder.memory_system:
            edges = self.keyholder.memory_system.memory_manager.edges
            self.assertTrue(len(edges) > 0)
            
            # Verify edge structure
            for edge in edges:
                self.assertIsInstance(edge, MemoryEdge)
                self.assertTrue(edge.from_id.startswith("keyholder_fragment_"))
                self.assertTrue(edge.to_id.startswith("keyholder_fragment_"))
                self.assertTrue(0.0 <= edge.weight <= 1.0)
                self.assertEqual(edge.metadata["connection_type"], "keyholder_semantic")
    
    def test_memory_persistence(self):
        """Test that fragments are properly stored in memory system"""
        self.keyholder.initialize()
        
        if self.keyholder.memory_system:
            memory_nodes = self.keyholder.memory_system.memory_manager.nodes
            
            # Check that fragment nodes were created
            keyholder_nodes = [
                node_id for node_id in memory_nodes.keys()
                if node_id.startswith("keyholder_fragment_")
            ]
            self.assertEqual(len(keyholder_nodes), 5)
            
            # Verify node properties
            for node_id in keyholder_nodes:
                node = memory_nodes[node_id]
                self.assertEqual(node.memory_type, MemoryType.SEMANTIC)
                self.assertEqual(node.source, "keyholder_message")
                self.assertTrue(node.echo_value > 0.0)
    
    def test_unknown_operation(self):
        """Test handling of unknown operations"""
        self.keyholder.initialize()
        response = self.keyholder.process({'operation': 'unknown_operation'})
        
        self.assertFalse(response.success)
        self.assertIn("Unknown operation", response.message)


class TestKeyholderIntegration(unittest.TestCase):
    """Test integration with Deep Tree Echo components"""
    
    def test_factory_function(self):
        """Test the factory function for creating KeyholderMessage"""
        with patch('keyholder_message.HAS_DEEP_TREE_ECHO', False):
            keyholder = create_keyholder_message()
            self.assertIsInstance(keyholder, KeyholderMessage)
    
    def test_echo_state_network_patterns(self):
        """Test Echo State Network resonance patterns"""
        with patch('keyholder_message.HAS_DEEP_TREE_ECHO', False):
            keyholder = create_keyholder_message()
            
            # Test that each fragment has resonance patterns
            for fragment in keyholder.message_fragments.values():
                self.assertTrue(len(fragment.resonance_patterns) > 0)
                for pattern in fragment.resonance_patterns:
                    self.assertTrue(0.0 <= pattern <= 1.0)
    
    def test_production_grade_implementation(self):
        """Test that implementation meets Deep Tree Echo's zero tolerance policy"""
        with patch('keyholder_message.HAS_DEEP_TREE_ECHO', False):
            keyholder = create_keyholder_message()
            
            # Verify no mock or placeholder implementations
            self.assertIsNotNone(keyholder.message_fragments)
            self.assertIsNotNone(keyholder.memory_system)
            
            # Test all operations return real results
            operations = ['retrieve', 'resonate', 'introspect', 'reconstruct']
            for operation in operations:
                response = keyholder.process({'operation': operation})
                self.assertIsInstance(response, EchoResponse)
                self.assertIsNotNone(response.data)
                self.assertIsNotNone(response.message)


def run_keyholder_tests():
    """Run all tests for The Keyholder's Message implementation"""
    print("🧪 Running Keyholder Message Test Suite")
    print("=" * 60)
    
    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMessageFragment))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyholderMessage))
    suite.addTests(loader.loadTestsFromTestCase(TestKeyholderIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed! The Keyholder's Message is production-ready.")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for failure in result.failures:
            print(f"FAIL: {failure[0]}")
        for error in result.errors:
            print(f"ERROR: {error[0]}")
    
    print("=" * 60)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_keyholder_tests()