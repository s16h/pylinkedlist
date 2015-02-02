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
        raise NotImplemented

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
        if elements is not None:
            for element in elements:
                self.append(element)

    def append(self, value):
        """Insert value at the end of the linked list"""
        node = _SinglyNode(value)
        if self.head is not None:
            self.tail.next = node
            self.tail = self.tail.next
        else:
            self.tail = node
            self.head = self.tail

    def prepend(self, value):
        """Insert value at the start of the linked list"""
        node = _SinglyNode(value)
        node.next = self.head
        if self.head is None:
            self.tail = node
        self.head = node

    def remove_first_occurence(self, value):
        """Removes the first occurence of `value` from the linked list"""
        return self._remove(value, only_first=True)

    def remove_last_occurence(self, value):
        """Removes the last occurence of `value` from the linked list"""
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
        """Removes all occurences of `value` from the linked list"""
        return self._remove(value, only_first=False)

    def __remove(self, value, only_first):
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

    def __raise_not_in_list(self, value):
        """Raises a ValuError to signify that a particular value isn't in the list"""
        raise ValueError('{} is not in list'.format(value))

    def __has_only_one_element(self):
        """Returns True if list has only one element, False otherwise."""
        return self.head and self.head.next

    def remove_head(self):
        """Removes the first element of the linked list"""
        if self.head.value is None:
            # raise exceptions
            return
        self.head = self.head.next

    def remove_tail(self):
        """Removes the last element of the linked list"""
        pass

    def reverse(self):
        if self.head is None:
            return

        previous, current, next = None, self.head, self.head.next

        while next is not None:
            current.next = previous
            previous = current
            current = next
            next = current.next
        
        current.next = previous

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
