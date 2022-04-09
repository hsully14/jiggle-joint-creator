# TOOLS *********************************************************************
# content = assignment
#
# deliver = Upload the files to your git repository
#           and share it in the assignment submission form.
#
# date    = 2022-03-13
# email   = contact@alexanderrichtertd.com
#***************************************************************************
"""



NOTE: Give yourself the time to play around with the tools,
      make sure everything works properly and note down your questions for our Q&A.




#******************************************************************************
# 01. ADVANCED SCRIPT EDITOR
#******************************************************************************
Let's explore and advance in our use of the script editor:

    a) Install and try one unfamiliar but promising script editor
       that you will use through out the masterclass:

        * Sublime Text 3
        * Visual Studio Code
        * PyCharm
        * ATOM
        * VIM
        * ...

    -I've used PyCharm before, will stick with VSCode to stay in line with company worfklows

    b) Check out the settings and plugins and add these or more:
        * user settings
        * git
        * spell check
        * color theme
        * ...

    -Added new color theme, editor ruler line, and PEP8 linting with pycodestyle to VSCode

    c) USE a few new shortcuts

    https://code.visualstudio.com/assets/docs/getstarted/tips-and-tricks/KeyboardReferenceSheet.png
    https://www.shortcutfoo.com/app/dojos/python-strings/cheatsheet

    d) ADD one helpful snippet and use it through out the masterclass

    TODO: this


NOTE: Nothing to upload in this task.









#******************************************************************************
# 02. SHELL
#******************************************************************************
1) Do the following steps only using a shell:

    a) Create the directory "shell_test"

    # C:\Program Files>cd C:\Users\hsull\Desktop
    # C:\Users\hsull\Desktop>mkdir shell_test

    b) Create the file "test_print.py" with a simple print into the directory

    # C:\Users\hsull\Desktop\shell_test>echo print('Hello World!') > test_print.py

    c) Rename the file to "new_test_print.py"

    # C:\Users\hsull\Desktop\shell_test>ren test_print.py new_test_print.py

    d) List what is in the directory "shell_test" including their file permissions

    # C:\Users\hsull\Desktop\shell_test>icacls C:\Users\hsull\Desktop\shell_test

    e) Execute the Python file and call the simple print

    # C:\Users\hsull\Desktop\shell_test>python new_test_print.py

    f) Remove the directory "shell_test" with its content

    # C:\Users\hsull\Desktop>del C:\Users\hsull\Desktop\shell_test

    BONUS: Solve the tasks without looking them up.












2) CREATE a custom .bat or .sh that does the following:

    a) STARTS a DCC of your choice (Maya, Nuke, Houdini, ...)


    b) ADDS custom script paths


    c) ADDITIONAL overwrites (paths, menus, ...)


    d) Make sure everything works as intended


    # I have questions for this part, need to continue researching 



    #TODO: finish this



#******************************************************************************
# 03. GIT
#******************************************************************************

1) STUDY git example
-----------------------------------------------------------
Before we start to work with git let's make sure to get familiar with the workflow
and how a git project should look like.
Browse through the folders and Wiki of my Open Source Pipeline Plex
which also serves as a code and documentation example throughout this masterclass:

    a) EXPLORE the Plex git repository and look into the code:
    https://github.com/alexanderrichtertd/plex

    # Check!

    b) READ the Wiki to understand the basics of the pipeline:
    https://github.com/alexanderrichtertd/plex/wiki

    # Check!










2) CREATE an assignment repository
-----------------------------------------------------------
All the upcoming assignments must be uploaded to your git repository.
Use the git shell for the following tasks:

    a) Create a new repository for the assignments on GitHub/GitLab/... with the sub folders:
        * 01_tools
        * 02_style
        * 03_advanced
        * 04_ui

       NOTE: If you use sensitive (company) data make your repository private.
             Invite me using alexanderrichtertd@gmail.com
             (Keep the resources out of your repository.)

    # Check!

    b) ADD a README.mb file describing your application.

    # Check!

    c) ADD and fill out a .ignore file (must ignore all .pyc files)

    # Check!

    d) ADD, commit and push your initial code remote into "01_tools".

    # Check!

    IMPORTANT: In future assignments make sure to commit and push the original version
               before starting with the assignment so we have a before and after.
               The commit message must be: INIT 02_style/03_advanced/04_UI
               And: UPDATE 02_style/03_advanced/04_UI.


    e) MAKE changes, commit and push again

    # Check!

    f) CREATE a branch "develop", make small changes and push it remote

    # Check!

    g) MERGE your develop changes into master

    # Check!

    h) TEST and clone your remote repository into another directory (as if you are a user).

    # Check!

    i) SHARE your repository with our #python_advanced Discord community (if not private).

    #TODO: this










3) DID YOU GET THAT?
-----------------------------------------------------------
ANSWER the following questions:

    a) Why should you use git instead of Google Drive for your (teams) code?

    Git enables finer control over your files, and allows you to create branches to develop and make changes without 
    affecting your main production files. It enables you to track the detailed edits and changes made to each file, and 
    control when you merge files and updates.

    b) What does "git add" and "git commit" do? What is the difference?

    Git add - begins tracking a file for inclusion in commits and edits, takes a snapshot of changed files and prepares (stages) them 
        for commits
    Git commit - saves file changes in your repository and adds that change to the repository records 

    c) What is the difference between "git pull" and "git push"?

    Git pull - grabs changes from remote/online repository and merges them into the local repository 
    Git push - pushes changes from local repository to the remote repository

    d) What does the command "git checkout" do?
       What can you do if you cannot checkout because you have untracked files?

    Git checkout - swaps your current branch to the specified branch and updates your local repository; can use -b to 
        create a new branch and check it out at the same time
    If you can't checkout, you should commit your untracked files to your current working branch and then swap over

    e) When do you need branches?

    You need branches to separate experimental or in-progress dev work from your master files. This enables you to safely
    experiment and edit without changing your verified functional code base. Then you can merge your code later once you know
    your work in progress is good to go.


    TIP: Create a practical example if you're unsure.



"""
