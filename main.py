from TeamMember import TeamMember
from SuperAdmin import SuperAdmin
from Project import Project
from Task import Task
from Project import Project
from Login import Login

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
    l.is_admin('Joe Bloggs')
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
    p.get_all_projects()
    sa.set_project_status('Top Secret', 'In-Progress')
    #TeamMember.send_project_email('Karl Gospel', 'karl.gospel25@gmail.com', 'karl.gospel25@gmail.com', 'you legend' )
    p.create_project_message(1, 'Do it again')
    #p.create_timeline('myProject')
    p.get_project_end_date('Top Secret')
    #p.add_members(1, 'Bubba')
    #p.delete_project(1)
    l.check_password('Joe Bloggs', 'ggg')
    print(p.get_description(1))
    print(l.get_users())
    p.get_project_id('myProject')
    people = (['jim', 'tom', 'pauline'])
    p.add_members('myProject', people)
    p.get_project_members('myProject')
    #p.create_task_messages_timeline(1)
    t.assign_task(1, 'Johnny')
    print(t.get_description(4))
    print(t.get_status(1))
    t.set_start_date(1)
    #sa.create_project("Find the holy grail", "Daisy Gospel", "Not Started", "Defeat the nazis and find the holy grail. Choose wisely" )