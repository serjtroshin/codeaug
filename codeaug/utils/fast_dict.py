import random

class ListDict(object):
    # https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice
    def __init__(self):
        self.item_to_position = {}
        self.items = []
        
    def add(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choice(self):
        return random.choice(self.items)
    
    def __len__(self): return self.items.__len__()
    

if __name__=="__main__":
    st = ListDict()
    st.add("aa")
    st.add("bb")
    print(st.item_to_position)
    st.remove("aa")
    print(st.item_to_position)
    st.add("aa")
    print(st.item_to_position)