class HashIndex:
    """
    In-Memory Hash Index.
    Untuk implementasi file-based database sederhana, main dictionary 
    Python berfungsi sebagai Hash Index (O(1)).
    Kelas ini disiapkan untuk extensibility (misal: secondary index).
    """
    def __init__(self):
        self.indices = {}

    def update(self, key, value):
        # Saat ini hanya menyimpan key keberadaan, 
        # bisa diperluas untuk field indexing tertentu.
        self.indices[key] = True

    def remove(self, key):
        if key in self.indices:
            del self.indices[key]
            
    def exists(self, key):
        return key in self.indices
