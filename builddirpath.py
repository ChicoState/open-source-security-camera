#!/usr/bin/python
import os
def GetPath(): 
    path = []
    cur_path =''

    while True:
        cur_path =''
        choice = input("choose directory:")
        if choice == 'back':
            if len(path) == 0:
                path.append('../')
            else:
                path.pop()
        elif choice != 'back':
            path.append(choice)
        for el in path:
            cur_path+= '/' + el
        if cur_path != '':
            print()
            print("cur path is: " + cur_path)
            print()
            # print(os.listdir(cur_path))
            for sub in os.listdir(cur_path):
                subdir = os.path.join(cur_path, sub)
                if os.path.isdir(subdir):
                    print(sub)
        # else:
        #     print("cur path is: .")
        #     print(os.listdir('.'))
    return path
print(GetPath())