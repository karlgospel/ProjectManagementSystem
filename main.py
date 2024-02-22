from TeamMember import TeamMember
from SuperAdmin import SuperAdmin
from Project import Project
from Task import Task
from Project import Project
from Login import Login
from Email import Email
if __name__ == '__main__':


    sa = SuperAdmin()
    sa.set_project_status('Run Forrest Run', 'In-Progress')
    sa.allocate_task(1, 'Kate Marten')
    #sa.edit_task(1, 'build a lego house', 'i want a blue house','complete')
    sa.create_login('Joe Bloggs', 'password', True)
    print("creating new user")
    sa.create_login('a', 'a', True)
    sa.change_password('Joe Bloggs', 'password', 'password999')
    l = Login()
    l.sign_in('a', 'a')

    # sa.create_task('Draw a hat', 'make it a fancy hat', 1)
    sa.allocate_task(1, 'Forrest Gump')
    t = Task()
    t.add_comment('Do it faster', 1, 'Karl Gospel')
    t.add_comment('working away', 1, 'Bubba Gump')
    t.set_percentage_complete(80, 1)
    t.set_status('Complete', 1)
    p = Project()
    p.check_owner('Karl Gospel', 'Top Secret')
    t.set_description('1', 'Changed my mind. I want a shoe')

    sa.set_project_status('Top Secret', 'In-Progress')
    #TeamMember.send_project_email('Karl Gospel', 'karl.gospel25@gmail.com', 'karl.gospel25@gmail.com', 'you legend' )

    p.create_project_message('myProject', 'Help me')
    p.create_timeline('myProject')
    p.get_project_end_date('Top Secret')
    #p.add_members(1, 'Bubba')
    #p.delete_project(1)
    l.check_password('Joe Bloggs', 'ggg')
    print(p.get_description(1))
    print(l.get_users())
    p.get_project_id('myProject')
    people = (['jim', 'tom', 'pauline'])
    #p.add_members('myProject', people)

    #p.create_task_messages_timeline(1)
    t.assign_task(1, 'Johnny')
    print(t.get_description(4))
    print(t.get_status(1))
    t.set_start_date(1)
    print(p.get_all_projects())
    p.get_project_members('myProject')
    p.get_project_messages('myProject')

    print(Login.current_user)
    p.update_percentage_complete('myProject')

    print('usernames are')
    users = l.get_users()
    members = p.get_project_members('Make dinner')
    print(list((set(users) | set(members)) - (set(users) & set(members))))
    print(t.get_project_for_task(1))
    print(t.is_assigned_to(1))
    print(t.get_owner_from_task(1))
    print(l.is_admin('a'))
    # l.sign_in('a','a')
    # print(Login.current_user)
    e = Email()
    e.send_task_assignmnent_email('Karl Gospel', 1)
    # e.send_project_emails('myProject')
    #e.send_project_completed_emails('myProject')
    #sa.create_project("Find the holy grail", "Daisy Gospel", "Not Started", "Defeat the nazis and find the holy grail. Choose wisely" )