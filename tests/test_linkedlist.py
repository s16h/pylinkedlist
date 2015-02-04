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
        self.assertIsNone(self.node.value)
        self.assertIsNone(self.node.next)

        self.node = _SinglyNode(42)
        self.assertEqual(self.node.value, 42)
        self.assertIsNone(self.node.next)

        new_node = _SinglyNode(next=self.node)
        self.assertIsNone(new_node.value)
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
        self.assertIsNone(self.ll.head)
        self.assertEqual(self.ll.tail, self.ll.head)

        elements = [1, 2, 3, 4, 5]
        self.ll = SinglyLinkedList(elements)
        self.__compare_with_list(self.ll, elements)

    def test_append(self):
        """Does appending a value to the end of a list have the expected effect?"""
        values_to_append = [1, 2, 3, 4, 5]
        for i, value in enumerate(values_to_append):
            self.ll.append(value)
            self.__compare_with_list(self.ll, values_to_append[:i+1])

    def test_prepend(self):
        """Does prepending a value to the beginning of a list have the expected effect?"""
        values_to_prepend = [5, 4, 3, 2, 1]

        for i, value in enumerate(values_to_prepend):
            self.ll.prepend(value)
            self.__compare_with_list(self.ll, values_to_prepend[i::-1])

    def test_remove_first_occurence(self):
        """Does remove_first_occurence() behave as expected?"""
        self.assertFalse(self.ll.remove_first_occurence(42))

        values = [1, 2, 3, 4, 5]

        self.ll = SinglyLinkedList(values)
        for i, element in enumerate(values):
            self.assertTrue(self.ll.remove_first_occurence(element))
            if i != len(values) - 1:
                self.assertEqual(self.ll.head.value, values[i+1])
                self.assertEqual(self.ll.tail.value, values[-1])
            else:
                self.assertIsNone(self.ll.head)
                self.assertIsNone(self.ll.tail)

        self.ll = SinglyLinkedList(values)
        for i, element in enumerate(values[::-1]):
            j = len(values) - 1 - i
            self.assertTrue(self.ll.remove_first_occurence(element))
            if j != 0:
                self.assertEqual(self.ll.head.value, values[0])
                self.assertEqual(self.ll.tail.value, values[j-1])
            else:
                self.assertIsNone(self.ll.head)
                self.assertIsNone(self.ll.tail)

        self.assertFalse(self.ll.remove_first_occurence(None))

    def test_remove_last_occurence(self):
        """Does remove_last_occurence() behave as expected?"""
        self.assertFalse(self.ll.remove_last_occurence(666))

        values = [1, 2, 3, 3, 2, 1]
        assert values == values[::-1]

        self.ll = SinglyLinkedList(values)
        for i, element in enumerate(values):
            self.assertTrue(self.ll.remove_last_occurence(element))
            if i != len(values) - 1:
                self.assertEqual(self.ll.head.value, values[0])
                self.assertEqual(self.ll.tail.value, values[-i-2])
            else:
                self.assertIsNone(self.ll.head)
                self.assertIsNone(self.ll.tail)

    def test_remove_all_occurences(self):
        """Does remove_all_occurences() behave as expected?"""
        values = [1]
        self.ll = SinglyLinkedList(values)
        self.assertTrue(self.ll.remove_all_occurences(values[0]))
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

        values = [1, 2, 3, 3, 2, 1]
        assert len(list(set(values))) < len(values)

        self.ll = SinglyLinkedList(values)

        first_value_to_remove = 1
        self.assertTrue(self.ll.remove_all_occurences(first_value_to_remove))
        self.assertEqual(self.ll.head.value, 2)
        self.assertEqual(self.ll.tail.value, 2)
        self.__compare_with_list(self.ll, [v for v in values
                                             if v != first_value_to_remove])

        second_value_to_remove = 2
        self.assertTrue(self.ll.remove_all_occurences(second_value_to_remove))
        self.assertEqual(self.ll.head.value, 3)
        self.assertEqual(self.ll.tail.value, 3)
        self.__compare_with_list(self.ll, [v for v in values
                                             if v not in (first_value_to_remove, second_value_to_remove)])

        third_value_to_remove = 3
        self.assertTrue(self.ll.remove_all_occurences(third_value_to_remove))
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    def test_remove_head(self):
        """Does remove_head() behave as expected?"""
        self.assertFalse(self.ll.remove_head())

        self.ll = SinglyLinkedList([1])
        self.assertTrue(self.ll.remove_head())
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertFalse(self.ll.remove_head())

        self.ll = SinglyLinkedList([1, 2])
        self.assertTrue(self.ll.remove_head())
        self.assertEqual(self.ll.head.value, 2)
        self.assertEqual(self.ll.tail, self.ll.head)

    def test_reverse(self):
        """Is a linked list reversed as expected?"""
        self.ll.reverse()
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

        all_values = [
            [1],
            [1, 2],
            [1, 2, 3],
            [1, None, 1, None]
        ]

        for values in all_values:
            self.ll = SinglyLinkedList(values)
            self.ll.reverse()
            self.__compare_with_list(self.ll, values[::-1])

    def test_remove_tail(self):
        self.assertFalse(self.ll.remove_tail())

        self.ll = SinglyLinkedList([1])
        self.assertTrue(self.ll.remove_tail())
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertFalse(self.ll.remove_tail())

        self.ll = SinglyLinkedList([1, 2])
        self.assertTrue(self.ll.remove_tail())
        self.assertEqual(self.ll.tail.value, 1)
        self.assertIsNone(self.ll.tail.next)
        self.assertEqual(self.ll.tail, self.ll.head)

    def __compare_with_list(self, ll, list_):
        """Helper to compare the order and size of a linked list with a list"""
        current = ll.head
        for value in list_:
            self.assertEqual(current.value, value)
            current = current.next
        self.assertIsNone(current)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SinglyNodeTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SinglyLinkedListTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()