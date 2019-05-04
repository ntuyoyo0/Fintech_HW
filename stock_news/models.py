class News():
    # title:string
    # text:list of string
    # timestamp:datetime
    # link:string
    def __init__(self,title,text,timestamp,link):
        self.title = title
        self.text = text
        self.timestamp = timestamp
        self.link = link
    def to_dict(self):
    	return {
    		'title':self.title,
    		'text':self.text,
    		'timestamp':self.timestamp,
    		'link':self.link
    	}
