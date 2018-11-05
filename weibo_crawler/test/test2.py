import scrapy

class FansItem(scrapy.Item):
	id = scrapy.Field()	
	nickname = scrapy.Field()		
	profile_image_url = scrapy.Field()			
	profile_url = scrapy.Field()

	def get(self, key):
		if key in self.keys():
			return self[key]
		else:
			return None

if __name__ == "__main__":
    item = FansItem()
    item["id"] = 100
    item["nickname"] = "test"
    print(item["id"])	
    print(item.get("id"))	
    print(item.get("id2"))	
    print(item["id2"])	