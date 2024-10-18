from db import check_password, execute_select_query

get_password_query = ''' SELECT password FROM users WHERE user_name LIKE %s'''
password = execute_select_query(get_password_query, ("admin",))

print(check_password(
    'admin', "dbe9787aaf4002c6662e490b3f1f7512807459b6dee2e1c2e56738e1cbbd993c"))
