import csv


def register():
    username = input("请输入您的账号：")
    password = input("请输入您的密码：")
    is_admin = input("是否为管理员？(y/n)：")
    is_admin = True if is_admin.lower() == 'y' else False

    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, is_admin])


def login():
    username = input("请输入您的账号：")
    password = input("请输入您的密码：")

    with open('users.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                if row[2] == 'True':
                    print("登录成功，您是管理员")
                    return username, True
                else:
                    print("登录成功，您是用户")
                    return username, False
        print("登录失败，用户名或密码错误")
        return None, False


def search_book():
    book_name = input("请输入书名：")
    with open('books.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if book_name in row[1]:
                print("书名：", row[1])
                print("作者：", row[2])
                print("出版社：", row[3])
                print("图书类别：", row[4])
                print("库存总量：", row[5])
                print("可借本数：", row[6])


def borrow_book(username):
    book_id = input("请输入图书ID：")
    with open('books.csv', 'r') as f:
        books = list(csv.reader(f))
    for i, book in enumerate(books):
        if book[0] == book_id:
            if int(book[6]) > 0:
                book[6] = str(int(book[6]) - 1)
                book[5] = str(int(book[5]) - 1)
                with open('books.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(books)
                print("借阅成功")
                with open('history.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([username, book_id])
                return
            else:
                print("该书已无库存")
                return
    print("未找到该书")


def change_password(username):
    new_password = input("请输入新密码：")
    with open('users.csv', 'r') as f:
        users = list(csv.reader(f))
    for user in users:
        if user[0] == username:
            user[1] = new_password
            with open('users.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(users)
            print("密码修改成功")
            return
    print("密码修改失败")


def view_history(username):
    with open('history.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:
                with open('books.csv', 'r') as f2:
                    reader2 = csv.reader(f2)
                    for book in reader2:
                        if book[0] == row[1]:
                            print("书名：", book[1])
                            print("作者：", book[2])
                            print("出版社：", book[3])
                            print("图书类别：", book[4])
                            print("库存总量：", book[5])
                            print("可借本数：", book[6])
                            print("------")


def user_menu(username):
    while True:
        print("0.退出")
        print("1.图书查询")
        print("2.图书借阅")
        print("3.修改账号密码")
        print("4.查询历史借阅记录")
        choice = input("请选择：")
        if choice == '0':
            break
        elif choice == '1':
            search_book()
        elif choice == '2':
            borrow_book(username)
        elif choice == '3':
            change_password(username)
        elif choice == '4':
            view_history(username)
        else:
            print("无效的选择，请重新选择")


def add_book():
    id = input("请输入图书ID：")
    name = input("请输入书名：")
    author = input("请输入作者：")
    press = input("请输入出版社：")
    type = input("请输入图书类别：")
    amount = input("请输入库存总量：")
    available = input("请输入可借本数：")
    with open('books.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id, name, author, press, type, amount, available])
    print("图书添加成功")


def modify_book():
    book_id = input("请输入需要修改的图书ID：")
    with open('books.csv', 'r') as f:
        books = list(csv.reader(f))
    for book in books:
        if book[0] == book_id:
            book[1] = input("请输入新的书名：")
            book[2] = input("请输入新的作者：")
            book[3] = input("请输入新的出版社：")
            book[4] = input("请输入新的图书类别：")
            book[5] = input("请输入新的库存总量：")
            book[6] = input("请输入新的可借本数：")
            with open('books.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(books)
            print("图书信息修改成功")
            return
    print("未找到该书")


def delete_book():
    book_id = input("请输入需要删除的图书ID：")
    with open('books.csv', 'r') as f:
        books = list(csv.reader(f))
    books = [book for book in books if book[0] != book_id]
    with open('books.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(books)
    print("图书删除成功")


def admin_menu(username):
    while True:
        print("0.退出")
        print("1.添加图书")
        print("2.修改图书信息")
        print("3.删除图书")
        print("4.修改账号密码")
        choice = input("请选择：")
        if choice == '0':
            break
        elif choice == '1':
            add_book()
        elif choice == '2':
            modify_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            change_password(username)
        else:
            print("无效的选择，请重新选择")


def main():
    while True:
        choice = input("请选择：1.登录 2.注册：")
        if choice == '1':
            username, is_admin = login()
            if username:
                if is_admin:
                    admin_menu(username)
                else:
                    user_menu(username)
        elif choice == '2':
            register()
        else:
            print("无效的选择，请重新选择")


if __name__ == "__main__":
    main()
