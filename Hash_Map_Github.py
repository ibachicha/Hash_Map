from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the content of the hash map.
        """
        self.buckets = DynamicArray()

        for _ in range(self.capacity): #clear array (like line 34)
            self.buckets.append(LinkedList())

        self.size = 0 # Reset the size to 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        """
        hash_value = self.hash_function(key) #get the hash value of the key
        target_bucket = self.buckets.get_at_index(hash_value % self.capacity) #get the bucket to check for key
        contain_node = target_bucket.contains(key) #get the node that contains the key in the target bucket

        if contain_node != None:
            return contain_node.value #return the value inside contain_node if !None
        else:
            return None

    def put(self, key: str, value: object) -> None: #double check
        """
        Updates the key / value pair in the hash map. If a given key already
        exists in the hash map, its associated value is replaced with the new value.
        If a given key is not in the hash map, a key / value pair
        is added.
        """
        hash_value = self.hash_function(key) #get the hash value
        target_bucket = self.buckets.get_at_index(hash_value % self.capacity) #get the bucket to insert at
        contain_node = target_bucket.contains(key) # get the node that contains the key from the target bucket

        if contain_node != None:       #if the contain node is not None,
            contain_node.value = value #the key has been found, so update to the value
        else:
            target_bucket.insert(key, value) #else, insert new key & value pair
            self.size += 1 #increment size bc we are adding to the hash table

    def remove(self, key: str) -> None:  # not good
        """
        This function removes a key from the hash table
        """

        hash_value = self.hash_function(key) # get the hash value
        target_bucket = self.buckets.get_at_index(hash_value % self.capacity) # get the target bucket of the key
        remove_key = target_bucket.remove(key) # Create variable for Removing Key. Not that Remove() is T/F.

        if remove_key == True:  # If the key to be removed has been found and removed
            self.size -= 1  # decrement size

    def contains_key(self, key: str) -> bool: #good
        """
        This method returns True if the given key is in the hash map,
        otherwise it returns False
        """
        hash_value = self.hash_function(key) #get the hask value
        target_bucket = self.buckets.get_at_index(hash_value % self.capacity) #get the bucket index of key
        contain_node = target_bucket.contains(key) #get the node that contains the key from the TB

        if contain_node != None: #if node is not None and is found
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty bucket in the hash table
        """
        empty_bucket_count = 0 #set count to zero

        for i in range(self.capacity): #initialize empty hash map
            if self.buckets.get_at_index(i).length() == 0: #(like line 47)
                empty_bucket_count += 1 #increment count if == 0
        return empty_bucket_count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.size / self.capacity #load factor is always computed as size/capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key / value pairs must remain in the new hash map and
        all hash table links must be rehashed. If new_capacity is less than 1,
        this method does nothing.
        """
        if new_capacity < 1: #if less than one, do nothing
            return

        tempDA = DynamicArray() #create new DA

        for i in range(self.capacity):
            tempDA.append(self.buckets.get_at_index(i))# Append the content of self.buckets into tempDA

        self.buckets = DynamicArray() # initialize self.buckets again with the new capacity
        for _ in range(new_capacity): #clear array
            self.buckets.append(LinkedList())
        self.capacity = new_capacity #create new capacity
        self.size = 0

        for i in range(tempDA.length()): # add the content of temp back into self.buckets to rehash
            bucket = tempDA.get_at_index(i) # each key to the appropriate bucket
            for node in bucket:
                self.put(node.key, node.value) #put back into newly created bucket

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys
        stored in hash map
        """
        keys = DynamicArray() #creat new DA
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)  # get the bucket at the index value i
            for node in bucket:  # get the value from each bucket
                keys.append(node.key)  # append to new DA
        return keys


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2 function 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_2)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - table_load example function2")
    print("--------------------------")
    m = HashMap(50, hash_function_2)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
