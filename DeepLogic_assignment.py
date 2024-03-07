import json
import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            try:
                latest_news_data = []
                response = requests.get('https://time.com/')
                soup = BeautifulSoup(response.text, 'html.parser')

                latest_news = BeautifulSoup(str(soup.find_all(class_ = "partial latest-stories")[0]),'html.parser')

                for i in range(6):
                    headline = latest_news.find_all('h3')[i].text
                    link = latest_news.find_all('a')[i].attrs['href']
                    latest_news_data.append({
                        'title':headline,
                        'link':f'https://time.com{link}'
                    })
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                json_data = json.dumps(latest_news_data)
                self.wfile.write(json_data.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Internal Server Error: {}".format(str(e)).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Page Not Found".encode("utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
