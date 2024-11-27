from flask import Flask, request, jsonify
from facebook_page_scraper import FacebookPageScraper
from rich import print

app = Flask(__name__)

@app.route('/scrape', methods=['POST', 'GET'])
def scrape_facebook_page():
    try:
        if request.method == 'POST':
            # Kiểm tra Content-Type
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 415

            # Lấy dữ liệu từ request body
            data = request.json
            if not data or "url" not in data:
                return jsonify({"error": "Missing 'url' in request body"}), 400

            url = data["url"]

        elif request.method == 'GET':
            # Lấy URL từ query string
            url = request.args.get('url')
            if not url:
                return jsonify({"error": "Missing 'url' in query parameters"}), 400

        # Gọi hàm scrape từ thư viện FacebookPageScraper
        print(f">= Scraping URL/Username: {url}\n")
        scraper = FacebookPageScraper()
        page_info = scraper.PageInfo(url)
        print("Page Information:")
        print(page_info)

        # Trả về kết quả dưới dạng JSON
        return jsonify({
            "success": True,
            "message": "Success",
            "data": page_info
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
