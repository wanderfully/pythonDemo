import os
def main():
    currentPath = os.getcwd();
    for i in range(1,5):
        if(os.path.exists("第"+str(i)+"页") is False):
            path = os.getcwd()
            os.mkdir("第"+str(i)+"页")
            os.chdir("第"+str(i)+"页")

            os.chdir(currentPath)
            print(currentPath)



if __name__ == '__main__':
    # print(os.path.pardir())
    main()
