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
        raise NotImplementedError()

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return '_SinglyNode(value={}, next={})'.format(self.value, repr(self.next))

    def __str__(self):
        return '{} -> {}'.format(str(self.value), str(self.next))

class SinglyLinkedList(object):
    def __init__(self, elements=None):
        self.head = None
        self.tail = self.head

        self.append_all(elements)

    def append_all(self, values=None):
        """Insert all the values, one by one, at the end of the list

        :param iterable values: The values to append to the list
        """
        # Check if values is a SinglyLinkedList, drops time compl. to O(1)
        values = values or []
        for value in values:
            self.append(value)

    def append(self, value):
        """Insert value at the end of the list

        Worst-case Time Complexity: O(1)

        :param object value: The value to append to the end of the list
        """
        node = _SinglyNode(value)
        if self.head is not None:
            self.tail.next = node
            self.tail = self.tail.next
        else:
            self.tail = node
            self.head = self.tail

    def prepend(self, value):
        """Insert value at the start of the linked list

        Worst-case Time Complexity: O(1)

        :param object value: The value to prepend to the beginning of the list
        """
        node = _SinglyNode(value)
        node.next = self.head
        if self.head is None:
            self.tail = node
        self.head = node

    def remove_first_occurence(self, value):
        """Removes the first occurence of `value` from the linked list

        Worst-case Time Complexity: O(``len(self)``)

        :param object value: The value to remove first occurence from the list
        """
        return self.__remove(value, only_first=True)

    def remove_last_occurence(self, value):
        """Removes the last occurence of `value` from the linked list

        Worst-case Time Complexity: O(``len(self)``)

        :param object value: The value to remove last occurence from the list
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

    def remove_all_occurences(self, value):
        """Removes all occurences of `value` from the linked list

        Worst-case Time Complexity: O(``len(self)``)

        :param object value: The value to remove all occurences from the list
        """
        return self.__remove(value, only_first=False)

    def __remove(self, value, only_first):
        """Helper to remove either first or all occurences of a value

        :param object value: The value to remove first or all occurences from the list
        :param bool only_first: If ``True``, only first occurence will be removed, otherwise all occurences will be removed
        """
        is_removed = False

        previous, current = None, self.head
        while current is not None:
            if current.value == value:
                is_removed = True
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

        return is_removed

    def remove_head(self):
        """Removes the first element of the linked list

        Worst-case Time Complexity: O(1)
        """
        if self.head is None:
            return False

        self.head = self.head.next
        if self.head is None:
            self.tail = self.head

        return True

    def remove_tail(self):
        """Removes the last element of the linked list

        Worst-case Time Complexity: O(``len(self)``)
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

        Worst-case Time Complexity: O(``len(self)``)
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
        raise NotImplementedError()

    def __bool__(self):
        return self.head is not None

    def __eq__(self, other):
        raise NotImplementedError()

    def __format__(self, formatstr):
        raise NotImplementedError()

    def __iadd__(self, other):
        raise NotImplementedError()

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __len__(self):
        # Consider storing length as an instance property.
        # Then we don't have to to an O(n) iteration everytime
        # __len__()) is called.
        length = 0
        current = self.head
        while (current is not None):
            length += 1
            current = current.next

        return length

    def __nonzero__(self):
        return self.__bool__()

    def __radd__(self, other):
        raise NotImplementedError()

    def __str__(self):
        return str(self.head)

    def __sizeof__(self):
        raise NotImplementedError()
