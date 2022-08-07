from pprint import pprint
from re import search
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
from time import sleep
import pyperclip
import os


class GetHtml:
    def __init__(self, link: str) -> None:
        self.link_recebido = link
        self.pg = pyautogui
        self.pp = pyperclip

        self.pg.PAUSE = 2

        self.html = ''
        self.link_produto = []
        self.nome_produto = []

        self.dict_name_link = {}

    def open_google(self) -> None:
        self.pg.press('win')
        self.pg.write('chrome')
        self.pg.press('enter')
        sleep(5)

    def open_link_facebook(self) -> None:
        self.pp.copy(self.link_recebido)
        self.pg.hotkey('ctrl', 'v')
        self.pg.press('enter')
        sleep(5)

    def collect_html(self) -> None:
        step_count = 1
        while True:
            if step_count == 1:
                get_position = self.pg.locateOnScreen('img/icon_market.png')
                if get_position:
                    self.pg.moveTo(get_position.left, 300)
                    self.pg.click(button='right')
                    step_count += 1
                pass
            elif step_count == 2:
                btn_inspect = self.pg.locateOnScreen('img/inspecionar.png')
                if btn_inspect:
                    self.pg.click(btn_inspect)
                    step_count += 1
                pass
            elif step_count == 3:
                open_inspect = self.pg.locateOnScreen(
                    'img/class.png', confidence=0.4)
                if open_inspect:
                    self.pg.moveTo(open_inspect)
                    step_count += 1
                pass
            elif step_count == 4:
                self.pg.scroll(400)
                search_class = self.pg.locateOnScreen(
                    'img/class.png', confidence=0.9)
                if search_class:
                    self.pg.click(search_class, button='right')

                    button_copy = self.pg.locateOnScreen(
                        'img/btnCopy.png', confidence=0.9)
                    self.pg.moveTo(button_copy)

                    copy_html = self.pg.locateOnScreen(
                        'img/copiar.png', confidence=0.9)
                    self.pg.click(copy_html)
                    break

    def use_pycharm(self) -> None:
        while True:
            return_pycharm = self.pg.locateOnScreen(
                'img/pycharm.png', confidence=0.9)
            if return_pycharm:
                self.pg.click(return_pycharm)
                break
            pass

    def use_vscode(self) -> None:
        while True:
            return_vscode = self.pg.locateOnScreen(
                'img/vscode.png', confidence=0.9)
            if return_vscode:
                self.pg.click(return_vscode)
                break
            pass

    def return_save_html(self) -> None:
        while True:
            search_file = self.pg.locateOnScreen(
                'img/file_html.png', confidence=0.8)
            if search_file:
                self.pg.click(search_file)
                self.pg.click(700, search_file.top)
                self.pg.hotkey('ctrl', 'a')
                self.pg.press('del')
                self.pg.hotkey('ctrl', 'v')
                self.pg.hotkey('ctrl', 's')
                break

    def open_file_html(self) -> str:
        with open('html.txt', mode='r', encoding="utf8") as html:
            self.html = html.read()
        return self.html

    def clean_html(self):
        html = BeautifulSoup(self.html, 'html.parser')
        text = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 " \
            "cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl " \
            "gmql0nx0 p8dawk7l"

        for link in html.find_all("a", attrs={"class": text}):
            self.link_produto.append(link["href"])

        for name in html.find_all("img", attrs={
                "class": "idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm"}):
            clean_name = name["alt"].split(' ')
            step_count = 1
            while step_count <= 5:
                clean_name = clean_name[:-1]
                step_count += 1
            clean_name = ' '.join(clean_name)
            self.nome_produto.append(clean_name)

    def create_file_excel(self):
        step_count = 0
        while step_count <= len(self.link_produto):
            if step_count == len(self.link_produto):
                break
            self.link_produto[step_count] = 'https://www.facebook.com' + \
                self.link_produto[step_count]
            step_count += 1
        self.dict_name_link = {
            "Nome": self.nome_produto, "Link": self.link_produto}

        dados = pd.DataFrame(data=self.dict_name_link)

        try:
            dados.to_excel('produtos.xls')
        except:
            os.remove('produtos.xls')
            dados.to_excel('produtos.xls')


if __name__ == '__main__':
    get_html = GetHtml(
        'https://www.facebook.com/marketplace/108164929217905/search?query=celular')
    sleep(3)
    get_html.open_google()
    get_html.open_link_facebook()
    get_html.collect_html()
    get_html.use_vscode()
    get_html.return_save_html()
    get_html.open_file_html()
    get_html.clean_html()
    get_html.create_file_excel()
