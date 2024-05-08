from flask import jsonify, Flask, request
import json
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def register_company(c_name, o_name, r_no, o_email, access_code):
    url = "http://20.244.56.144/test/register"
    request_data = {
        "companyName": c_name,
        "ownerName": o_name,
        "rollNo": r_no,
        "ownerEmail": o_email,
        "accessCode": access_code
    }

    response = requests.post(url, json=request_data)
    print(response.json())
    if response.status_code == 200:
        with open("creds.json", "w") as f:
            f.write(response.text)

def save_auth_data(auth_json):
    try:
        access_token = auth_json.get("access_token")
        expires_in = auth_json.get("expires_in")
        # Calculate the expiry date
        expires_in = int(expires_in) / 10  # expires_in is in seconds
        current_time = datetime.now()
        expiry_date = current_time + timedelta(seconds=expires_in)

        # Prepare the data to save
        data_to_save = {
            "access_token": access_token,
            "expiry_date": expiry_date.isoformat()
        }
        print(data_to_save)
        # Save the data to a file (e.g., auth_data.json)
        with open("auth_data.json", "w") as file:
            json.dump(data_to_save, file)

        print("Auth data saved successfully.")
    except Exception as e:
        print("Error while saving auth data:", str(e))

# Wrapper for auth
def auth_wrapper():
    url = "http://20.244.56.144/test/auth"  
    with open("creds.json", "r+") as f:
        data = f.read()
    req_data = json.loads(data)
    response = requests.post(url, json=req_data)
    print(response.text)
    if response.status_code == 200:
      save_auth_data(response.json())
      return response.json()["access_token"]
    
test_server_url = 'http://20.244.56.144/test/companies/'

@app.route('/categories/<category_name>/products')
def get_top_products(category_name):
    top_n = request.args.get('top', default=10, type=int)
    min_price = request.args.get('minPrice', default=0, type=int)
    max_price = request.args.get('maxPrice', default=999999, type=int)

    # List of companies
    companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]

    products = []
    for company in companies:
        url = f"{test_server_url}{company}/categories/{category_name}/products?top={top_n}&minPrice={min_price}&maxPrice={max_price}"
        try:
            response = requests.get(url)
            products.extend(response.json())
        except requests.RequestException as e:
            print(f"Failed to fetch products for {company}: {e}")

    return jsonify(products)

@app.route('/categories/<category_name>/products/<product_id>')
def get_product_details(category_name, product_id):
    # Assuming product_id is unique across all companies
    companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
    for company in companies:
        url = f"{test_server_url}{company}/categories/{category_name}/products"
        try:
            response = requests.get(url)
            products = response.json()
            for product in products:
                if product.get('productId') == product_id:
                    return jsonify(product)
        except requests.RequestException as e:
            print(f"Failed to fetch products for {company}: {e}")

    return jsonify({'error': 'Product not found'}), 404


if __name__ == "__main__":
    #register_company("goMart", "OM SINGH", "2128032", "2128032@kiit.ac.in", "mjPQGJ")
    #auth_wrapper()

    app.run(debug=True, port=5000)
