import random


class EditingListView:
    network_list = []

    def __init__(self, edit_field_obj, list_obj):
        self.edit_field_obj = edit_field_obj
        self.list_obj = list_obj
        self.edit_field_obj.returnPressed.connect(self.add_text_to_list_widget)
        self.list_obj.itemClicked.connect(self.remove_item_from_list)

    def remove_item_from_list(self, item):
        text = item.text()
        try:
            self.network_list.remove(text)
        except ValueError:
            pass

        row  = self.list_obj.row(item)
        self.list_obj.takeItem(row)

    def add_text_to_list_widget(self):
        text = ((self.edit_field_obj.text()).strip()).upper()
        if text:
            self.network_list.append(text)
            self.list_obj.addItem(text)
            self.edit_field_obj.clear()

    def get_list_widget_contents(self):
        items = [self.list_obj.item(i).text() for i in range(self.list_obj.count())]
        return items

    def fetch_random_element_from_list_widget(self):
        list_widget_array = self.get_list_widget_contents()
        if len(list_widget_array) == 0:
            print('List widget пуст')
            return False

        random_network = random.choice(list_widget_array)

        return random_network