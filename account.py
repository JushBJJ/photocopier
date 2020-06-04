import json
import hashlib
import os
import draw
import Home

users={}
photocopier={}

def fix_file(file_path, photocopier_path):
    x=True

    with open(file_path, "r") as f:
        try:
            x=json.loads(f.read())
        except:
            x=False
    with open(photocopier_path, "r") as f:
        try:
            x=json.loads(f.read())
        except:
            x=False
    
    if x==False:
        with open(file_path, "w") as f:
            f.write(json.dumps(
                {"Admin":
                    {"Password": hashlib.sha256("admin".encode()).hexdigest(),
                        "Credits":1000
                    }
                })
            )

        with open(photocopier_path, "w") as f:
            f.write(json.dumps(
                {"Ink": 100,
                "Log":{}}
            ))

def register_or_login(args):
    # If register is false, login is switched on
    # Using CSV for this is just for testing, not for real security purposes.
    # Update: Relationship with CSV ended, json is now my new friend...again

    file_location=os.path.join(os.environ["HOMEPATH"],"Desktop\\Accounts.json") # File location.
    photocopier_location=os.path.join(os.environ["HOMEPATH"],"Desktop\\Photocopier.json")

    screen=args[0]
    register=args[1]

    if os.path.exists(file_location) and os.path.exists(photocopier_location): # Check if file existss
        fix_file(file_location, photocopier_location)

        with open(photocopier_location, "r") as p:
            photocopier=json.loads(p.read())

        with open(file_location, "r") as Accounts:
            users=json.loads(Accounts.read())
            rect=draw.rectangle(screen, int(os.get_terminal_size()[0]/2), 4)

            # Draw box at middle of screen.
            rect.draw(
                    int(screen.get_width()/2 - rect.width/2), 
                    int(screen.get_height()/2 - rect.height/2)
                    )

            title="Register" if register else "Login"
            rect.write(int(rect.width/2-len(title)/2), -1, title)
            rect.write(2, 1, "Username: ")
            rect.write(1, 2, "-"*rect.width)
            rect.write(2, 3, "Password: ")

            msg="Press enter to continue. Press q to exit."
            rect.write(int(rect.width/2-len(msg)/2), 6, msg)

            rect.to_pos(2+len("Username: "), 1)
            blacklisted_keys="\t\n\x0b\x0c"

            username=""
            password=""

            while True:
                # Input user the username and password
                info=screen.input(screen, limit=rect.width-len("Username: ")-2)

                if info=="8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf": # Quit code
                    screen.clear_screen()
                    return False, False
                elif info=="7ef2fad58d1f2f12f5d78bdf7fc7ba3ad9529010ebd071c14d69394153f6106b": # Reset code
                        # Clear username and password inputs
                        # Reusing code 100
                        rect.write(len("Username: ")+2, 1," "*(rect.width-len("Username: ")))
                        rect.write(len("Password: ")+2, 3," "*(rect.width-len("Password: ")))

                        rect.to_pos(2+len("Username: "), 1)

                        username=""
                        password=""
                        continue

                for key in info:
                    if key in blacklisted_keys:
                        if username!="":
                            rect.write(2, 1, "Username:"+" "*len(info))
                            username=""
                        elif password!="":
                            rect.write(2, 3, "Password:"+" "*len(info))
                            password=False

                        continue

                # str because it needs to be in a seperatre memory address
                if username=="" and info!="":
                    username=str(info)

                    rect.to_pos(2+len("Password: "), 3)

                elif password=="" and info!="":
                    password=hashlib.sha256(str(info).encode()).hexdigest() # Convert to sha256 hexdigest       

                    if register:
                        if username in users.keys():
                            # Clear
                            rect.to_pos(1, 6)
                            screen.clear_line()

                            msg="Username already exists."
                            rect.write(int(rect.width/2-len(msg)/2), 6, msg)

                            # Clear username and password inputs
                            rect.write(len("Username: ")+2, 1," "*(rect.width-len("Username: ")))
                            rect.write(len("Password: ")+2, 3," "*(rect.width-len("Password: ")))

                            rect.to_pos(2+len("Username: "), 1)

                            username=""
                            password=""
                
                            continue
                        else:
                            users[username]={"Password":password, "Credits":10}
                        break
                    else:
                        if username in users.keys():
                            if password==users[username]["Password"]:
                                return Home.home(screen, users, username, photocopier)
                        
                        # Clear
                        # I SERIOUSLY HATE COPY AND PASTING THIS THING I ALREADY MADE A FEW LINES ABOVE
                        rect.to_pos(1, 6)
                        screen.clear_line()

                        msg="Invaild username or password"
                        rect.write(int(rect.width/2-len(msg)/2), 6, msg)

                        rect.write(len("Username: ")+2, 1," "*(rect.width-len("Username: ")))
                        rect.write(len("Password: ")+2, 3," "*(rect.width-len("Password: ")))

                        rect.to_pos(2+len("Username: "), 1)

                        username=""
                        password=""
            
                        continue


        # Update file
        with open(file_location, "w") as f:
            f.write(json.dumps(users))
        
        # Return current users and current user in session
        return Home.home(screen, users, username, photocopier)
    else:
        # Recreate file putting admin account
        with open(file_location, "w") as f:
            f.write(json.dumps({"Admin":{"Password": hashlib.sha256("admin".encode()).hexdigest(), "Credits":1000}}))

        with open(photocopier_location, "w") as f:
            f.write(json.dumps(
                {"Ink": 100,
                "Log":{}}
            ))

        return register(screen)