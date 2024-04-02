import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table
import datetime
import difflib
from thefuzz import fuzz, process

# Class of a library manager in charge of all books, users and historical records.


class Library:
    def __init__(self):
        data1 = pd.read_excel(
            r"C:\Users\hugo5\Desktop\python\demo\lib\midterm_data1.xlsx", sheet_name='Sheet0')
        data2 = pd.read_excel(
            r"C:\Users\hugo5\Desktop\python\demo\lib\midterm_data2.xlsx", sheet_name='Sheet0')
        alldata = pd.concat([data1, data2], ignore_index=True)
        alldata['是否可借閱'] = True     # All books are available in the beginning.
        # The current user to the corresponding book.
        alldata['目前借用者帳號'] = None

        # Reformat the names of each book to use them as keys to access other info.
        for i in range(len(alldata)):
            new_str = alldata.at[i, '題名'].replace(' ', '')
            alldata.at[i, '題名'] = new_str

        self.books = alldata
        self.all_historical_records = pd.DataFrame(
            columns=['使用者帳號', '書名', '借閱日', '到期日', '實際還書日', '狀態'])
        self.users = users
        self.current_user_account = None

    # Update availability of books and historical records.

    def lend_book(self, lended_book_name):
        df = self.books
        df = self.books.set_index('題名')
        df.at[lended_book_name, '是否可借閱'] = False
        df.at[lended_book_name, '目前借用者帳號'] = self.current_user_account
        self.books = df.reset_index()

        self.all_historical_records.at[len(
            self.all_historical_records), '使用者帳號'] = self.current_user_account
        self.all_historical_records.at[len(
            self.all_historical_records)-1, '書名'] = lended_book_name
        self.all_historical_records.at[len(
            self.all_historical_records)-1, '借閱日'] = datetime.date.today()
        self.all_historical_records.at[len(
            self.all_historical_records)-1, '到期日'] = datetime.date.today()+datetime.timedelta(days=30)
        self.all_historical_records.at[len(
            self.all_historical_records)-1, '實際還書日'] = ' '
        self.all_historical_records.at[len(
            self.all_historical_records)-1, '狀態'] = '借閱中'

    # Update availability of books and historical records.

    def return_book(self, returned_book_name):
        df = self.books
        df = self.books.set_index('題名')
        df.at[returned_book_name, '是否可借閱'] = True
        df.at[returned_book_name, '目前借用者帳號'] = None
        self.books = df.reset_index()

        df2 = self.all_historical_records
        df2 = self.all_historical_records.set_index('書名')
        df2.at[returned_book_name, '實際還書日'] = datetime.date.today()
        df2.at[returned_book_name, '狀態'] = '已歸還'
        self.all_historical_records = df2.reset_index()

    # def add_user():
    # def delete_user():
    # def view_books():
    # def add_book():


# class User:
#     def __init__(self, name, account, password):
#         self.name = name
#         self.account = account
#         self.password = password
#         self.record = None
#     def borrow_book():
#     def return_book():
#     def get_record():


# Class to manage the login page.
class LoginPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.title('Library')
        self.root.geometry('600x600')
        self.root.resizable(False, False)
        self.name = ctk.StringVar()
        self.account = ctk.StringVar()
        self.password = ctk.StringVar()
        self.create_page()

    def create_page(self):
        self.page = ctk.CTkFrame(self.root)
        self.page.pack(pady=20, padx=60, fill='both', expand=True)
        account_label = ctk.CTkLabel(self.page, text="Account:")
        account_label.pack(pady=12, padx=10)
        account_entry = ctk.CTkEntry(self.page, textvariable=self.account)
        account_entry.pack(pady=12, padx=10)
        account_entry.focus()
        password_label = ctk.CTkLabel(self.page, text="Password:")
        password_label.pack(pady=12, padx=10)
        password_entry = ctk.CTkEntry(
            self.page, textvariable=self.password, show='*')
        password_entry.pack(pady=12, padx=10)
        login_button = ctk.CTkButton(
            self.page, text="Login", command=self.login)
        login_button.pack(pady=12, padx=10)
        register_button = ctk.CTkButton(
            self.page, text="Register", command=self.register_page)
        register_button.pack(pady=12, padx=10)
        visitor_button = ctk.CTkButton(
            self.page, text="Visitor", command=self.go_to_main_page)
        visitor_button.pack(pady=12, padx=10)

    def login(self):
        bool = lib.users['account'].str.contains(self.account.get())
        account_index = lib.users.index[lib.users['account']
                                        == self.account.get()]
        if (lib.users[bool].empty == False):
            if (self.password.get() == lib.users['password'].loc[account_index].item()):
                lib.current_user_account = self.account.get()
                self.go_to_main_page()
            else:
                messagebox.showwarning('Warning', "The password is wrong.")
        else:
            messagebox.showwarning('Warning', "The account does not exist.")

    def register_page(self):
        self.page.destroy()
        self.page = ctk.CTkFrame(self.root)
        self.page.pack(pady=20, padx=60, fill='both', expand=True)
        name_label = ctk.CTkLabel(self.page, text="Name:")
        name_label.pack(pady=12, padx=10)
        name_entry = ctk.CTkEntry(self.page, textvariable=self.name)
        name_entry.pack(pady=12, padx=10)
        name_entry.focus()
        account_label = ctk.CTkLabel(self.page, text="Account:")
        account_label.pack(pady=12, padx=10)
        account_entry = ctk.CTkEntry(self.page, textvariable=self.account)
        account_entry.pack(pady=12, padx=10)
        password_label = ctk.CTkLabel(self.page, text="Password:")
        password_label.pack(pady=12, padx=10)
        password_entry = ctk.CTkEntry(
            self.page, textvariable=self.password, show='*')
        password_entry.pack(pady=12, padx=10)
        done_button = ctk.CTkButton(self.page, text="Done",
                                    command=self.check_registration)
        done_button.pack(pady=12, padx=10)
        back_button = ctk.CTkButton(self.page, text="Back",
                                    command=self.back_to_login_page)
        back_button.pack(pady=12, padx=10)

    # Check if the user has registered already.

    def check_registration(self):
        bool = lib.users['account'].str.contains(self.account.get())
        if (lib.users[bool].empty == True):
            lib.users.loc[len(lib.users.index)] = [
                self.name.get(), self.account.get(), self.password.get()]
            lib.current_user_account = self.account.get()
            self.go_to_main_page()
        else:
            messagebox.showwarning('Warning', 'The account has been used.')

    def go_to_main_page(self):
        self.page.destroy()
        MainPage(self.root)

    def back_to_login_page(self):
        self.page.destroy()
        LoginPage(self.root)


class MainPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.title('Library')
        self.root.geometry('600x600')
        self.root.resizable(False, False)
        self.keyword = ctk.StringVar()
        self.create_page()

    def create_page(self):
        self.page = ctk.CTkFrame(self.root)
        self.page.pack(pady=20, padx=60, fill='both', expand=True)

        if lib.current_user_account == None:
            current_name = 'visitor'
        else:
            current_name_index = lib.users.index[lib.users['account']
                                                 == lib.current_user_account]
            current_name = users['name'].loc[current_name_index].item()

        greeting_label = ctk.CTkLabel(
            self.page, text="Hello, "+current_name+"!")
        greeting_label.pack(pady=12, padx=10)
        keyword_label = ctk.CTkLabel(self.page, text="Keyword:")
        keyword_label.pack(pady=12, padx=10)
        search_entry = ctk.CTkEntry(self.page, textvariable=self.keyword)
        search_entry.pack(pady=12, padx=10)
        search_entry.focus()
        search_button = ctk.CTkButton(
            self.page, text="Search for Books", command=self.search_for_books)
        search_button.pack(pady=12, padx=10)
        show_button = ctk.CTkButton(
            self.page, text="Show all Books", command=self.show_all_books)
        show_button.pack(pady=12, padx=10)
        record_button = ctk.CTkButton(
            self.page, text="Get Personal Record", command=self.get_personal_record)
        record_button.pack(pady=12, padx=10)
        logout_button = ctk.CTkButton(
            self.page, text="Log out & Leave", command=self.back_to_login_page)
        logout_button.pack(pady=12, padx=10)

    def show_all_books(self):
        window = ctk.CTkToplevel()
        window.geometry('1450x900')
        window.title('All Books')
        frame = ctk.CTkFrame(window)
        frame.pack(fill='both', expand=True)
        shown_table = lib.books[['題名', '作者/創建者', '版本', '出版者', '建立日期', '是否可借閱']]

        click_col = []
        for i in range(len(shown_table)):
            if lib.books[['是否可借閱']].loc[i, '是否可借閱'] == True:
                click_col.append('雙擊借閱')
            else:
                click_col.append(' ')
        shown_table[' '] = click_col

        table = Table(frame, dataframe=shown_table,
                      showstatusbar=True, showtoolbar=True)
        table.show()

        def click_to_lend_book(event):
            if lib.current_user_account == None:
                messagebox.showwarning(
                    'Warning', 'Please login to borrow books.')
            else:
                selected_row = table.get_row_clicked(event)
                selected_col = table.get_col_clicked(event)
                if table.model.getValueAt(selected_row, selected_col) == '雙擊借閱':
                    table.model.setValueAt('已借閱', selected_row, selected_col)
                    table.model.setValueAt(False, selected_row, selected_col-1)
                    table.updateModel(table.model)
                    table.setRowColors(rows=selected_row, cols=range(
                        selected_col+1), clr='yellow')
                    table.setSelectedCells(
                        selected_row, selected_row, selected_col, selected_col)
                    table.redraw()

                    lended_book_name = table.model.getValueAt(selected_row, 0)
                    lib.lend_book(lended_book_name)

        table.bind('<Double-Button-1>', click_to_lend_book)
        root.mainloop()

    def search_for_books(self):  # note method 1~2我先隱藏起來 ;新增method3供參考
        approximation_ratio = 75
        shown_table = pd.DataFrame(
            columns=['題名', '作者/創建者', '版本', '出版者', '建立日期', '是否可借閱'])

        # 1. Method of SequenceMatcher()
        # for i in range(len(lib.books)):
        #     if difflib.SequenceMatcher(None, lib.books.at[i, '題名'], self.keyword.get()).quick_ratio() or difflib.SequenceMatcher(None, lib.books.at[i, '作者/創建者'], self.keyword.get()).quick_ratio() >= approximation_ratio:
        #         shown_table.at[len(shown_table), '題名'] = lib.books.at[i, '題名']
        #         shown_table.at[len(shown_table)-1,
        #                        '作者/創建者'] = lib.books.at[i, '作者/創建者']
        #         shown_table.at[len(shown_table)-1,
        #                        '版本'] = lib.books.at[i, '版本']
        #         shown_table.at[len(shown_table)-1,
        #                        '出版者'] = lib.books.at[i, '出版者']
        #         shown_table.at[len(shown_table)-1,
        #                        '建立日期'] = lib.books.at[i, '建立日期']
        #         shown_table.at[len(shown_table)-1,
        #                        '是否可借閱'] = lib.books.at[i, '是否可借閱']

        # # 2. Method of substring in string
        # for index, row in lib.books.iterrows():
        #     if self.keyword.get() in row['題名']:
        #         bool = shown_table['題名'].str.contains(row['題名'])
        #         if shown_table[bool].empty == True:
        #             shown_table.at[len(shown_table), '題名'] = row['題名']
        #             shown_table.at[len(shown_table)-1,
        #                            '作者/創建者'] = row['作者/創建者']
        #             shown_table.at[len(shown_table)-1, '版本'] = row['版本']
        #             shown_table.at[len(shown_table)-1, '出版者'] = row['出版者']
        #             shown_table.at[len(shown_table)-1, '建立日期'] = row['建立日期']
        #             shown_table.at[len(shown_table)-1, '是否可借閱'] = row['是否可借閱']
        # 3. fuzzy searching # 模糊搜尋
        for index, row in lib.books.iterrows():
            if fuzz.partial_token_sort_ratio(self.keyword.get(),  row['題名']) >= approximation_ratio or fuzz.partial_token_sort_ratio(self.keyword.get(), row['作者/創建者']) >= approximation_ratio:

                # if difflib.SequenceMatcher(None, row['題名'], self.keyword.get()).quick_ratio() >= approximation_ratio:
                shown_table.at[len(shown_table), '題名'] = row['題名']
                shown_table.at[len(shown_table)-1, '作者/創建者'] = row['作者/創建者']
                shown_table.at[len(shown_table)-1, '版本'] = row['版本']
                shown_table.at[len(shown_table)-1, '出版者'] = row['出版者']
                shown_table.at[len(shown_table)-1, '建立日期'] = row['建立日期']
                shown_table.at[len(shown_table)-1, '是否可借閱'] = row['是否可借閱']
                click_col = []
                for index, row in shown_table:
                    if lib.books[['是否可借閱']].loc[i, '是否可借閱'] == True:
                        click_col.append('雙擊借閱')
                    else:
                        click_col.append(' ')
                shown_table[' '] = click_col

                print()

        if len(shown_table) == 0:
            messagebox.showwarning('Wanring', 'No related books.')
        else:
            window = ctk.CTkToplevel()
            window.geometry('1450x900')
            window.title('Searched Books')
            frame = ctk.CTkFrame(window)
            frame.pack(fill='both', expand=True)

            click_col = []
            for i in range(len(shown_table)):
                if lib.books[['是否可借閱']].loc[i, '是否可借閱'] == True:
                    click_col.append('雙擊借閱')
                else:
                    click_col.append(' ')
            shown_table[' '] = click_col

            table = Table(frame, dataframe=shown_table,
                          showstatusbar=True, showtoolbar=True)
            table.show()

            def click_to_lend_book(event):
                if lib.current_user_account == None:
                    messagebox.showwarning(
                        'Warning', 'Please login to borrow books.')
                else:
                    selected_row = table.get_row_clicked(event)
                    selected_col = table.get_col_clicked(event)
                    if table.model.getValueAt(selected_row, selected_col) == '雙擊借閱':
                        table.model.setValueAt(
                            '已借閱', selected_row, selected_col)
                        table.model.setValueAt(
                            False, selected_row, selected_col-1)
                        table.updateModel(table.model)
                        table.setRowColors(rows=selected_row, cols=range(
                            selected_col+1), clr='yellow')
                        table.setSelectedCells(
                            selected_row, selected_row, selected_col, selected_col)
                        table.redraw()

                    lended_book_name = table.model.getValueAt(selected_row, 0)
                    lib.lend_book(lended_book_name)

            table.bind('<Double-Button-1>', click_to_lend_book)
            root.mainloop()

    def get_personal_record(self):
        # Confirm if the current user is a visitor and doesn't login.
        if lib.current_user_account == None:
            messagebox.showwarning(
                'Warning', 'Please login to get personal record.')
        elif len(lib.all_historical_records[lib.all_historical_records['使用者帳號'] == lib.current_user_account]) == 0:
            messagebox.showwarning('Warning', 'No record.')
        else:
            window = ctk.CTkToplevel()
            window.geometry('750x450')
            window.title('Personal Record')
            frame = ctk.CTkFrame(window)
            frame.pack(fill='both', expand=True)

            # Confirm if the expected returing date is overdue.
            for i in range(len(lib.all_historical_records)):
                if lib.all_historical_records.at[i, '到期日'] < datetime.date.today():
                    lib.all_historical_records.at[i, '狀態'] = '已逾期'

            shown_table = lib.all_historical_records[lib.all_historical_records['使用者帳號']
                                                     == lib.current_user_account]
            shown_table.reset_index(inplace=True, drop=True)
            shown_table = shown_table.drop('使用者帳號', axis=1)

            return_button_col = []
            for i in range(len(shown_table)):
                if shown_table.at[i, '狀態'] == ('借閱中' or '已逾期'):
                    return_button_col.append('雙擊還書')
                else:
                    return_button_col.append(' ')
            shown_table[' '] = return_button_col

            table = Table(frame, dataframe=shown_table,
                          showstatusbar=True, showtoolbar=True)
            table.show()

            def click_to_return_book(event):
                selected_row = table.get_row_clicked(event)
                selected_col = table.get_col_clicked(event)
                if table.model.getValueAt(selected_row, selected_col) == '雙擊還書':

                    table.model.setValueAt(' ', selected_row, selected_col)
                    table.model.setValueAt('已歸還', selected_row, selected_col-1)
                    table.model.setValueAt(
                        datetime.date.today(), selected_row, selected_col-2)
                    table.updateModel(table.model)
                    table.setSelectedCells(
                        selected_row, selected_row, selected_col, selected_col)
                    table.redraw()

                    returned_book_name = table.model.getValueAt(
                        selected_row, 0)
                    lib.return_book(returned_book_name)

            table.bind('<Double-Button-1>', click_to_return_book)
            root.mainloop()

    def back_to_login_page(self):
        lib.current_user_account = None
        self.page.destroy()
        LoginPage(self.root)


users_dic = {'name': ['Tom', 'Joe'], 'account': [
    'tom', 'joe'], 'password': ['tom', 'joe']}
users = pd.DataFrame(users_dic, index=range(2))
# users = pd.DataFrame(columns=['name','account','password'])
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')
lib = Library()

root = ctk.CTk()
LoginPage(root)
root.mainloop()
