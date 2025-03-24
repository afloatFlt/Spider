import requests
from bs4 import BeautifulSoup
import time
import csv

# 设置请求头，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 由于本地爬取次数过多，打不开谷歌学术，因此使用镜像网址
baseurl = 'https://scholar.lanfanshu.cn/scholar?start={start}&q={search_term}&hl=zh-CN&as_sdt=0,5'

# 多页解析
def fetch_all_papers(search_term, num_pages):
    all_papers = []
    for page_num in range(num_pages):
        print(f"正在抓取第 {page_num + 1} 页...")

        # 动态构建url并发送请求 -> start=0为第一页，start=10为第二页
        url = baseurl.format(start=page_num * 10, search_term=search_term)
        response = requests.get(url, headers=headers)

        # 解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})

        # 提取论文信息
        for paper in papers:
            title = paper.find('h3').get_text()
            link = paper.find('h3').find('a')['href']
            authors_and_info = paper.find('div', {'class': 'gs_a'}).get_text()
            citation_info = paper.find('div', {'class': 'gs_fl'}).get_text()

            all_papers.append({
                'title': title,
                'link': link,
                'authors_and_info': authors_and_info,
                'citation_info': citation_info
            })

        time.sleep(2)  # 添加延时，避免请求过于频繁

    return all_papers


# 保存内容
def save_to_csv(papers, filename="papers.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'authors_and_info', 'citation_info'])
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)

    print(f"论文信息已成功保存到 {filename}")


def main():
    search_term = input("请输入搜索词：")

    # 将空格替换为加号，适应URL参数
    search_term = search_term.replace(" ", "+")

    num_pages_to_scrape = 1
    all_papers = fetch_all_papers(search_term, num_pages_to_scrape)
    save_to_csv(all_papers)


if __name__ == "__main__":
    main()
