from _utils import mutates_length

class _SinglyNode(object):
    __slots__ = ['value', 'next']

    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next

    def __bool__(self):
        return (self.value is not None) or (self.next is not None)

    def __bytes__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, _SinglyNode):
            return (self.value == other.value) and (self.next == other.next)
        return NotImplemented

    def __format__(self, format_spec):
        if format_spec == 'l':
            as_list = []
            current = self
            while current is not None:
                as_list.append(current.value)
                current = current.next
            return str(as_list)
        return str(self)

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        string = '_SinglyNode(value={}, next={})'
        return string.format(self.value, repr(self.next))

    def __str__(self):
        return '{} -> {}'.format(str(self.value), str(self.next))

class SinglyLinkedList(object):
    """
    A singly linked list implementation.
    """
    def __init__(self, elements=None):
        # TODO: Make head and tail properties. Restrict modification using a descriptor?
        self.head = None
        self.tail = self.head
        self._length = 0

        self.append_all(elements)

    def append_all(self, values):
        """Insert all the values, one by one, at the end of the list

        :param iterable values: The values to append to the list
        :Worst-case Time Complexity: If `vaues` is a `SinglyLinkedList`, then
        O(1). If `values` is any other `Iterable`, then O(``len(values)``).
        """
        if isinstance(values, SinglyLinkedList):
            if self.head is not None:
                self.tail.next = values.head
            else:
                self.head = values.head
            self.tail = values.tail
            return

        values = values or []
        for value in values:
            self.append(value)

    @mutates_length(always=True)
    def append(self, value):
        """Insert value at the end of the list

        :param object value: The value to append to the end of the list
        :Worst-case Time Complexity: O(1)
        """
        node = _SinglyNode(value)
        if self.head is not None:
            self.tail.next = node
            self.tail = self.tail.next
        else:
            self.tail = node
            self.head = self.tail

    @mutates_length(always=True)
    def prepend(self, value):
        """Insert value at the start of the linked list

        :param object value: The value to prepend to the beginning of the list
        :Worst-case Time Complexity: O(1)
        """
        node = _SinglyNode(value)
        node.next = self.head
        if self.head is None:
            self.tail = node
        self.head = node

    @mutates_length(decrements=True)
    def remove_first_occurence(self, value):
        """Removes the first occurence of `value` from the linked list

        :param object value: The value to remove first occurence from the list
        :returns: ``True`` if value is removed, ``False`` otherwise
        :rtype: bool
        :Worst-case Time Complexity: O(``len(self)``)
        """
        return self.__remove(value, only_first=True)

    @mutates_length(decrements=True)
    def remove_last_occurence(self, value):
        """Removes the last occurence of `value` from the linked list

        :param object value: The value to remove last occurence from the list
        :returns: ``True`` if value is removed, ``False`` otherwise
        :rtype: bool
        :Worst-case Time Complexity: O(``len(self)``)
        """
        # Keep track of the last found node and its previous node
        found_previous, found_node = None, None
        
        previous, current = None, self.head
        while current is not None:
            if current.value == value:
                found_node = current
                found_previous = previous
            previous = current
            current = current.next

        if (found_previous is None) and (found_node is None):
            return False

        if found_previous is None:
            if found_node.next is None:
                self.tail = found_node.next
            self.head = found_node.next
        else:
            if found_node.next is None:
                self.tail = found_previous
            found_previous.next = found_node.next

        return True

    @mutates_length(decrements=True)
    def remove_all_occurences(self, value):
        """Removes all occurences of `value` from the linked list

        :param object value: The value to remove all occurences from the list
        :returns: ``True`` if value is removed, ``False`` otherwise
        :rtype: bool
        :Worst-case Time Complexity: O(``len(self)``)
        """
        return self.__remove(value, only_first=False)

    def __remove(self, value, only_first):
        """Helper to remove either first or all occurences of a value

        :param object value: The value to remove first or all occurences from the list
        :param bool only_first: If ``True``, only first occurence will be removed,
        otherwise all occurences will be removed
        :returns: The number of values removed
        :rtype: int
        """
        count = 0 # number of values removed

        previous, current = None, self.head
        while current is not None:
            if current.value == value:
                count += 1
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = self.head.next
                if current.next is None:
                    self.tail = previous
                if only_first:
                    break
            else:
                previous = current
            current = current.next

        return count

    @mutates_length(decrements=True)
    def remove_head(self):
        """Removes the first element of the linked list

        :returns: ``True`` if head is removed, ``False`` otherwise
        :rtype: bool
        :Worst-case Time Complexity: O(1)
        """
        if self.head is None:
            return False

        self.head = self.head.next
        if self.head is None:
            self.tail = self.head 

        return True

    @mutates_length(decrements=True)
    def remove_tail(self):
        """Removes the last element of the linked list

        :returns: ``True`` if tail is removed, ``False`` otherwise
        :rtype: bool
        :Worst-case Time Complexity: O(``len(self)``)
        """
        if self.head is None:
            return False

        previous, current = None, self.head
        while current is not None:
            if current.next is None:
                self.tail = previous
                if previous is None:
                    self.head = previous
                else:
                    previous.next = None
            previous = current
            current = current.next

        return True

    def reverse(self):
        """Reverses the list in-place; it can then be traversed backwards

        :Worst-case Time Complexity: O(``len(self)``)
        """
        if self.head is None:
            return

        previous, current, next = None, self.head, self.head.next

        while next is not None:
            current.next = previous
            previous = current
            current = next
            next = current.next
        
        current.next = previous

        self.tail = self.head
        self.head = current

    def __add__(self, other):
        if isinstance(other, SinglyLinkedList):
            pass
        else:
            self.append_all(other)
        raise NotImplementedError()

    def __bool__(self):
        return self.head is not None

    def __eq__(self, other):
        """
        Two linked lists are equal if they have equal values in the same order.
        """
        if isinstance(other, self.__class__):
            self_is_empty = self.head is None
            other_is_empty = other.head is None

            if self_is_empty and other_is_empty:
                return True

            if (self_is_empty and not other_is_empty) or \
               (not self_is_empty and other_is_empty):
                return False

            if (self.head.value != other.head.value) or \
               (self.tail.value != other.tail.value):
               return False

            current_self = self.head
            current_other = other.head

            while current_self is not None:
                if current_other is None:
                    return False
                if current_self.value != current_other.value:
                    return False
                current_self = current_self.next
                current_other = current_other.next

            return (current_self is None) and (current_other is None)

        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __format__(self, formatstr):
        raise NotImplementedError()

    def __iadd__(self, other):
        raise NotImplementedError()

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self):
        return self._length

    def __nonzero__(self):
        return self.__bool__()

    def __radd__(self, other):
        raise NotImplementedError()

    def __repr__(self):
        repr_format = '{}({})'
        class_name = self.__class__.__name__
        if self.head is None:
            return repr_format.format(class_name, '')
        else:
            return repr_format.format(class_name, format(self.head, 'l'))

    def __str__(self):
        return '[{}]'.format(str(self.head))

    def __sizeof__(self):
        raise NotImplementedError()
