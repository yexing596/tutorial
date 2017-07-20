def extract(selector,path):
    return selector.xpath(path).extract()

def extract_one(selector,path):
    result=selector.xpath(path).extract()
    return result[0] if len(result) else None