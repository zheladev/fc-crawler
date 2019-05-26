from fc_scrapper.items.thread import ThreadItem


class ThreadPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ThreadItem):
            print('thread!')
            pass

        return item
