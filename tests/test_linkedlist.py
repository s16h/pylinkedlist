import unittest
from linkedlist.linkedlist import _SinglyNode, SinglyLinkedList

class SinglyNodeTestCase(unittest.TestCase):
    """Tests for the _SinglyNode class in `linkedlist.py`."""

    def setUp(self):
        self.node = _SinglyNode()
        assert self.node.value is None
        assert self.node.next is None

    def test_ctor(self):
        """Is a new node created with its value and next node correcty initialised?"""
        self.assertEqual(self.node.value, None)
        self.assertEqual(self.node.next, None)

        self.node = _SinglyNode(42)
        self.assertEqual(self.node.value, 42)
        self.assertEqual(self.node.next, None)

        new_node = _SinglyNode(next=self.node)
        self.assertEqual(new_node.value, None)
        self.assertEqual(new_node.next.value, self.node.value)
        self.assertEqual(new_node.next.next, self.node.next)

    def test_value(self):
        """Is the value of a node set and retrieved correctly?"""
        values = [
            42,
            '42',
            [1, 2, 3],
            {42: 42, 666: 666},
            set([1, 1, 2, 2, 3]),
            object()
        ]

        for value in values:
            self.node.value = value
            self.assertEqual(self.node.value, value)

    def test_truthiness(self):
        """Is a node's truthiness evaluated correctly?"""
        self.assertFalse(self.node)

        self.node.value = 42
        self.assertTrue(self.node)

        self.node.value = None 
        self.node.next = _SinglyNode()
        self.assertTrue(self.node)

    def test_eq(self):
        """Does __eq__() compare node objects as expected?"""
        other = _SinglyNode()
        self.assertEqual(self.node, other)

        self.node.value = 1
        self.assertNotEqual(self.node, other)

        other.value = 1
        self.assertEqual(self.node, other)

        self.node.next = other
        self.assertNotEqual(self.node, other)
        self.assertEqual(self.node.next, other)

    def test_acyclic_str(self):
        """Is an acyclic node evaluated correctly as a str?"""        
        EXPECTED_STR = 'None -> None'
        self.assertEqual(str(self.node), EXPECTED_STR)

        self.node.value = 1
        EXPECTED_STR = '1 -> None'
        self.assertEqual(str(self.node), EXPECTED_STR)

        self.node.next = _SinglyNode(2)
        EXPECTED_STR = '1 -> 2 -> None'
        self.assertEqual(str(self.node), EXPECTED_STR)

    def test_acyclic_repr(self):
        """Is an acyclic node represented correctly (i.e. with repr())?"""
        EXPECTED_REPR = '_SinglyNode(value=None, next=None)'
        self.assertEqual(repr(self.node), EXPECTED_REPR)

        self.node.value = 1
        EXPECTED_REPR = '_SinglyNode(value=1, next=None)'
        self.assertEqual(repr(self.node), EXPECTED_REPR)

        self.node.next = _SinglyNode(2)
        EXPECTED_REPR = '_SinglyNode(value=1, next=_SinglyNode(value=2, next=None))'
        self.assertEqual(repr(self.node), EXPECTED_REPR)

class SinglyLinkedListTestCase(unittest.TestCase):
    """Tests for the LinkedList class in `linkedlist.py`."""

    def setUp(self):
        self.ll = SinglyLinkedList()
        assert self.ll.head is None
        assert self.ll.tail is None

    def test_ctor(self):
        """Is a newly constructed list correcty initialised?"""
        self.assertEqual(self.ll.head, None)
        self.assertEqual(self.ll.tail, self.ll.head)

    def test_append(self):
        """Does appending a value to the end of a list have the expected effect?"""
        values_to_append = [1, 2, 3, 4, 5]

        for i, value in enumerate(values_to_append):
            self.ll.append(value)
            current = self.ll.head
            for j in range(i + 1):
                self.assertEqual(current.value, values_to_append[j])
                if j == i:
                    self.assertEqual(current.next, None)
                else:
                    current = current.next

    def test_prepend(self):
        """Does prepending a value to the beginning of a list have the expected effect?"""
        values_to_prepend = [5, 4, 3, 2, 1]

        for i, value in enumerate(values_to_prepend):
            self.ll.prepend(value)
            current = self.ll.head
            for j in range(i, 0, -1):
                self.assertEqual(current.value, values_to_prepend[j])
                if j == i + 1:
                    self.assertEqual(current.next, None)
                else:
                    current = current.next

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SinglyNodeTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SinglyLinkedListTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()