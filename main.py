# 1. Assuming that project_admin has all rights.
# 2. Create table headers with all permission
# 3. loop trough all the non-project_admin roles, and then fill in table.
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET


def gather_headers():
    all_headers = []
    print('Gathering all headers')
    tree = ET.parse('input.xml')
    root = tree.getroot()

    roles = root.find(".//role[@name='project_admin']")
    rules = roles.getchildren()
    for rule in rules:
        all_headers.append(rule.attrib['permission'])

    all_clean_headers = clean_up_headers(all_headers)

    return all_clean_headers

def gather_categories(clean_headers):
    header_categories = []
    for unchecked_header in clean_headers:
        category = unchecked_header.split('.')[0]
        if category not in header_categories:
            header_categories.append(category)

    return header_categories

def clean_up_headers(headers):
    clean_headers = []
    for header in headers:
        clean_headers.append(header.replace("com.polarion.",""))

    return clean_headers

def gather_data():
    print('Converting XML to HTML Table...')
    tree = ET.parse('input.xml')
    root = tree.getroot()

    data = []
    for elems in root:
        newFood = {}
        for food in elems: 
            tag = food.tag
            text = food.text
            newFood[tapersistence.object.TestRun.deleteg] = text
        
        data.append(newFood)
    
    return data

def generate_html(headers, data):
    enviroment = Environment(loader=FileSystemLoader("templates"))

    results_filename = "data_results.html"
    results_template = enviroment.get_template("results.html")
    context = {
        "headers":headers,
        "datas": data
    }
    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(results_template.render(context))
        print(f"Job done..")
        
def main():
    headers = gather_headers()
    categories = gather_categories(headers)
    data = gather_data()
    generate_html(headers, data)

if __name__ == "__main__":
    main()
