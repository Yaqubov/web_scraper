import socket
import argparse
from bs4 import BeautifulSoup
import requests


def recv_all(sock, data_lenght):
    r_data = b""
    while len(r_data) < data_lenght:
        temp = sock.recv(data_lenght-len(r_data))
        if not temp:
            break
        r_data += temp
    return r_data


class Server:

    def __init__(self):
        self.leaf_tag = 0

    def myRecur(self, list):
        for tag in list:
            children = tag.findChildren()
            if children:
                self.myRecur(children)
            else:
                self.leaf_tag += 1
        return self.leaf_tag

    def get_leaf_tag_cnt(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")
        soup = soup.find_all("p")
        return self.myRecur(soup)

    def get_img_cnt(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")

        return len(soup.find_all('img'))

    def run(self, website):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('127.0.0.1', 3040))
        soc.listen(1)
        print('Listening at', soc.getsockname())

        while True:
            sc, address = soc.accept()
            print('We have accepted a connection from', address)
            print(' Socket name:', sc.getsockname())

            web = recv_all(sc, 1024)
            print("Website is " + web.decode('UTF-8'))

            image_count = self.get_img_cnt("http://" + web.decode("UTF-8"))

            child_tag_count = self.get_leaf_tag_cnt(
                "http://" + web.decode("UTF-8"))

            sc.sendall(f'{image_count} {child_tag_count}'.encode('UTF-8'))

            sc.close()


class Client:

    def run(self, website):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('127.0.0.1', 3040))
        print('Client has been assigned ', soc.getsockname())

        soc.sendall(website.encode('UTF-8'))
        soc.shutdown(socket.SHUT_WR)

        respond = recv_all(soc, 1024)

        print(respond.decode('UTF-8'))

        soc.close()


def main():

    choises = {'server': Server, 'client': Client}

    parser = argparse.ArgumentParser(description="Web Scraper")
    parser.add_argument("role", choices=choises)
    parser.add_argument("-p", help="website address")

    args = parser.parse_args()

    clss = choises[args.role]()

    clss.run(args.p)


if __name__ == '__main__':
    main()
