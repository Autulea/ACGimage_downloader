import getopt
import sys
import requests


def grabDanbooru(nPages, tags, out_folder):
    page_no = 1
    currImg = 0
    while page_no <= nPages:
        params = {"limit": 100, "page": page_no, "tags": tags}
        try:
            response = requests.get(url="https://danbooru.donmai.us/posts.json", params=params)
            data = response.json()
            for i in range(len(data)):
                if 'file_url' in data[i]:
                    print(data[i]['file_url'])
                    img_url = data[i]['file_url']
                    try:
                        img_data = requests.get(img_url).content
                        currImg += 1
                        with(open(out_folder + "/" + str(currImg), 'wb')) as f:
                            f.write(img_data)
                    except:
                        print("img get error")
        except:
            print("error getting posts")
        page_no = page_no + 1


def grabGelbooru(nPages, tags, out_folder):
    page_no = 1
    currImg = 0
    while page_no <= nPages:
        params = {"limit": 100, "pid": page_no, "tags": tags, "json": 1}
        try:
            response = requests.get(url="https://gelbooru.com/index.php?page=dapi&s=post&q=index", params=params)
            data = response.json()
            for i in range(len(data)):
                if 'file_url' in data[i]:
                    print(data[i]['file_url'])
                    img_url = data[i]['file_url']
                    try:
                        img_data = requests.get(img_url).content
                        currImg += 1
                        with(open(out_folder + "/" + str(currImg), 'wb')) as f:
                            f.write(img_data)
                    except:
                        print("img get error")
        except:
            print("error getting posts")
        page_no = page_no + 1


def main():
    tags = ''
    try:
        options, args = getopt.getopt(sys.argv[1:], "hp:t:", ["pages=", "tags="])
    except getopt.GetoptError:
        sys.exit(2)
    out_folder = args[0]
    nPages = int(args[1])
    source = int(args[2])
    for (option, arg) in options:
        if option == "-h":
            print("grabber.py -t <tags> out_folder number_of_pages source")
            sys.exit()
        elif option in ("-t", "--tags"):
            tags = arg
    if source == 1:
        grabDanbooru(nPages, tags, out_folder)
    elif source == 2:
        grabGelbooru(nPages, tags, out_folder)
    else:
        print("unknown source")
        sys.exit(1)
    print('Download successful!')


if __name__ == '__main__':
    main()
