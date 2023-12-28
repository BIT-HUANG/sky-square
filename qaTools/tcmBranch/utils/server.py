from atlassian import Confluence
from bs4 import BeautifulSoup
import pandas as pd
from qaTools.config import BaseConfig as BC


class ConfluenceOperation:
    def __init__(self):
        self.server = Confluence(url=BC.CONFLUENCE_URL, username=BC.USERNAME, password=BC.ATLAS_PASSWORD)

    def get_tcm_pages_by_tag(self):
        try:
            page_list = list()
            pages = self.server.get_all_pages_by_label(label='tcm')
            for page in pages:
                page_list.append({'tcm_page_id': page['id'], 'tcm_page_title': page['title']})

            page_list.reverse()
            print(page_list)
            return page_list
        except BaseException as e:
            return e

    def get_tcm_pages_by_cql(self):
        try:
            cql = "title ~ 'TCM' AND (title ~ '常规发版' OR title ~ '紧急发版') AND type = 'page' ORDER BY title DESC"
            page_list = list()
            pages = self.server.cql(cql=cql)
            for page in pages['results']:
                if page['content']['id'] != '5450518':
                    page_list.append({'tcm_page_id': page['content']['id'], 'tcm_page_title': page['content']['title']})
            print(page_list)
            return page_list
        except BaseException as e:
            return e

    def get_branch_dict_list_from_table_by_title(self, title):
        try:
            page_dict = self.server.get_page_by_title(space='TCM', title=title, expand='body.view')
            page_content = page_dict['body']['view']['value']
            soup = BeautifulSoup(page_content, 'html.parser')
            table = soup.find('table', attrs={'class': 'confluenceTable'})
            dfs = pd.read_html(str(table))[0]  # 使用Pandas将网页table转换为表格 list形式
            df = dfs.dropna(subset=['项目'])
            branch_dict_list = list()
            for index, row in df.iterrows():  # 按行遍历，将DataFrame的每一行迭代为(index, Series)对，可以通过row[name]对元素进行访问。
                branch_dict = {'service': str(getattr(row, '项目')), 'tcm': str(getattr(row, '版本'))}
                branch_dict_list.append(branch_dict)
            return branch_dict_list

        except BaseException as e:
            return e

    def get_branch_dict_list_from_comment_by_title(self, title):
        try:
            page_id = self.server.get_page_id(space='TCM', title=title)
            page_comment_list = self.server.get_page_comments(content_id=page_id, expand='body.view')['results']
            print(page_comment_list)
            comment_list = list()
            for comment in page_comment_list:
                comment_list.append(comment['body']['view']['value'])
            print(comment_list)
            return comment_list
        except BaseException as e:
            return e

    @staticmethod
    def comment_parser(comment):
        soup = BeautifulSoup(comment, 'html.parser')
        results = []
        for p_tag in soup.find_all('p'):
            if len(p_tag.contents) == 1 and isinstance(p_tag.contents[0], str):
                results.append(p_tag.get_text().replace('\n', '').replace('\xa0', ''))
        return results
