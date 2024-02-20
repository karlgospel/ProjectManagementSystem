import bcrypt

pwd = 'MyPassWord'

bytePwd = pwd.encode('utf-8')

# Generate salt
mySalt = bcrypt.gensalt()

# Hash password
pwd_hash = bcrypt.hashpw(bytePwd, mySalt)
password = 'MyPassWord'
password = password.encode('utf-8')
print(bcrypt.checkpw(password, pwd_hash))