# Pinkshift Website
A first draft of a website/e-commerce site for Pinkshift. This GitHub repository contains all of the files used in running a local website. The main goal of this project is build a website for my band, Pinkshift, to sell merchandise.

# Project Specs
### Running the Pinkshift Webstore ###
The first thing to make sure to have done when running this project or starting on of your own is by starting a virtual environment. This can be done in your terminal by typing:
```
pip install pipenv
```
Once you create a new directory or enter the one in this repository "Final_Projects", make sure you have django installed. This can be done in your terminal by typing:
```
pipenv install django
```
and then by typing:
```
pipenv shell
```
These two steps activate a new virtual environment. To run the Pinkshift Webstore on your local server, you will have to make sure you're in the very first Final_projects folder. You can confirm if you're in it by typing "ls" into your command line. If the files that pop up are the 'Final_Project db.sqlite3 manage.py static store' files, then you can run the following command:
```
python manage.py runserver
```
Running this line will start the development server and give you the http:// address at which you can view the site.

# Bootstrap Framework
For this website, I implented Bootstrap 4
### Creating Pages ###
In the store folder, the views.py file is where you can begin adding a new view function. A simple empty page takes in one request argument and should return a direction to an .html page. The return spits out an http response of a django template using django's render function. Make sure that when you call the render function, you input two arguments: request, 'new_page.html'. A very simple example can be written like:
```
def newPage(request):
    return render(request, 'new_page.html')
```
The next step is to create a new .html page. You can create it to your liking and make sure the file is called 'new_page.html' or whatever the second argument in the render call is.

Once that's done, you can go to the urls.py file in the store folder and add a path to your new page in the urlpatterns list. The django path function takes in 3 arguments. The first is the slug you want your page to have, the second is the specific function from the views.py file for direction, and the third is the name you want to give the url when called between your code. To continue with the example, you could add this to the urlpatterns list:
```
path('newpage/', views.newPage, name='new')
```
### Adding a page tab to the navbar ###
You can add this new page as a tab in your header. In the navbar.html file, you can add a linked list to the unordered list section where the dropdown menu bar is located. You can copy and paste:
```
<li class="nav-item"><a class="nav-link text-light font-weight-bold px-3" style="font-family:'Georgia'" href="{% url 'new' %}">tab_name</a></li>
```
Where the href name is the name you gave it in urls.py and the tab_name is just whatever text you want to have in the navbar. The above line of code continues the same example from the previous subsection.
