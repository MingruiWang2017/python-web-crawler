from datetime import datetime


class TidyUp(object):
    def process_item(self, item, spider):
        item['date'] = list(map(datetime.isoformat, item['date']))
        return item
