import re
import json


# 2.1 Write the python code that uses regular expressions to extract the numerical product count 
# from the variable product_count_text below, and converts it to integer (int) format

numeric_pattern = re.compile('^[0-9]+$')
product_count_text = "381 Products found"
product_count_int = int(re.match("^[0-9]+", product_count_text).group())
print("2.1 Solution: " + str(product_count_int))


# 2.2 Write the python code that uses a single search pattern to extract the sequence of characters 
# after the final "/", before the "-" character, in each url.

generic_urls = ["https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img", "https://www.genericdomain.com/abc/31287bdwakj-jkl.img", "https://www.genericdomain.com/19unioawd02-jkl.img"]

for url in generic_urls:
    special_sequence = re.search(r"[0-9]+[a-z0-9]+", url)
    print("2.2 Solution: " + special_sequence.group())


# 2.3 Assume that you have extracted the below string from the 'script' tag of a web page. 
# Use python regular expressions (i.e the 're' library) to convert the string into a format that 
# can be loaded via the python json library. I.e the below code should not throw any errors 
# after the code is formatted properly.

with open('data.txt', 'r') as file:
    product_storage_string_raw = file.read().replace('\n', '')
    pattern = re.compile(r"products_storage= (.*);")
    product_storage_parsed = pattern.search(product_storage_string_raw)
    product_storage_json = json.loads(product_storage_parsed.group(1))
    print("2.3 Solution")
    print(product_storage_json)
    print(type(product_storage_json))




