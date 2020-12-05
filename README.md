# Pinkshift Website
A first draft of a website/e-commerce site for Pinkshift. This GitHub repository contains all of the files used in running a local website. The main goal of this project is build a website for my band, Pinkshift, to sell merchandise. The payment process is carried out through the Stripe payment service.

## Project Specs
#### Running the Pinkshift Webstore
The first thing to make sure to have done when running this project or starting on of your own is by starting a virtual environment. This can be done in your terminal by typing:``` pip install pipenv ```. Once you create a new directory or enter the one in this repository "Final_Projects", make sure you have django installed. This can be done in your terminal by typing:```pipenv install django```and then ```pipenv shell```. These two steps activate a new virtual environment. To run the Pinkshift Webstore on your local server, you will have to make sure you're in the very first Final_projects folder. You can confirm if you're in it by typing "ls" into your command line. If the files that pop up are the 'Final_Project db.sqlite3 manage.py static store' files, then you can run the following command: ```python manage.py runserver```. Running this line will start the development server and give you the http:// address at which you can view the site. In order to stop running the server, you can use the shortcut "ctrl + C".

Make sure you have the django, pillow, and stripe packages installed.

## Editing the website's layout
For this website, I implented a Bootstrap template (citation at the end) to begin laying out the design of the website. All of the icons/buttons were taken from fontawesome.com.

#### Creating Pages
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
#### Adding a page tab to the navbar
You can add this new page as a tab in your header. In the navbar.html file, you can add a linked list to the unordered list section where the dropdown menu bar is located. You can copy and paste:
```
<li class="nav-item"><a class="nav-link text-light font-weight-bold px-3" style="font-family:'Georgia'" href="{% url 'new' %}">tab_name</a></li>
```
Where the href name is the name you gave it in urls.py and the tab_name is just whatever text you want to have in the navbar. The above line of code continues the same example from the previous subsection.

#### Using FontAwesome icons to customize your website
If you wish to replace the buttons I used on my website, or remove them entirely, you must go to the html pages where they're implented. For example, the header/navbar has two icons: a yellow disk that serves as a home button, and a magnifying glass that serves as search button.


## Become an Adminstrator
In order to start uploading your products and all that fun stuff, you must become a a django adminstrator. When your local server isn't running, you can register to become a website admin by using the command: ```python manage.py createsuperuser```

A series of prompts will appear, asking you to set up a new username, email, password, etc. You can use that information to log into the admin page of your website.


## Webstore Models
The code already has category and product models in the models.py file. These classes are linked to the admin interface via the admin.py file and you can easily upload your products and sort them into your own categories. There are buttons that say "+ Add" next to categories and products which you can use to add products to your website. Creating a product or a category automatically creates a slug so you don't need to worry about that. As long as you fill out the product title, product description, and include an image, you should be able to view the product in its respective category. All of your products, no matter what category, are automatically displayed on the home page. (Which, by the way, you can access your home page via the 

#### Adding your categories to the navbar with a dropdown menu
As of right now, the only tab that has a dropdown menu is the "store" tab. You can create another tab with a dropdown menu by copying the html code that's there for the store tab. I placed it here for convenience:
```
 <li class="nav-item dropdown">
    <a class="nav-link text-light font-weight-bold px-3 dropdown-toggle" style="font-family:'Georgia'" href="" data-toggle="dropdown">store</a>
    <div class="dropdown-menu bg-dark">
        <a class="dropdown-item text-light font-weight-bold" style="font-family:'Georgia';font-style:italic" href="{% url 'home' %}">all merch</a>
        {% for category in links %}
        <a class="dropdown-item text-light" style="font-family:'Georgia';font-style:italic" href="{{category.get_url}}">{{category.name}}</a>
        {% endfor %}
    </div>
</li>
```
This html code automatically takes in ALL of the categories you created in the admin interface. If you want only certain categories in your dropdown menu, you will have to edit each <a> tag individually within the division.

#### Viewing and keeping track of orders
The other important model to keep track of when using the admin interface are "orders". When a customer purchases an item, their information gets sent to the Stripe dashboard while simultaneously getting logged on the admin page. You're able to click on the orders link on the left-hand side and view all past orders with their order numbers.

## Setting up Stripe payment
In order to use Stripe payment with this website, all you're going to need are your API keys. The first think you need to do is head over to https://stripe.com and create an account and create your business. After creating your account and linking your bank account and all that, you should be redirected to the main Stripe dashboard. Before going live, you're going to have to run some test purchases to see that everything is running smoothly.

On the bottom of the left-hand side of the Stripe dashboard, there should be an option to click a little slider called "Viewing test data". Once this slider is activated, you'll be able to view your test API keys on the home dashboard page. You will need to copy both the publishable key and the secret key into your code. If you open the settings.py file and scroll all the way to the bottom, there are two variables as such:
```
STRIPE_PUBLISHABLE_KEY = 'your publishable API key'
STRIPE_SECRET_KEY = 'your secret API key'
```
All you need to do is simply copy and paste your keys into the corresponding variable and you will be able to begin making test purchases, and they should appear on your stripe dashboard.

Once you're done testing and ready to go live, deactivate the "Viewing test data" slider and you should go back to where you found your test API keys. The API keys should have changed. These are your live API keys that should be implemented in your code when you're ready to run your store.
    
# Citations and other resources
There are two important templates I used that are integral to the website. The first template I used is Bootstraps starter template in order to get the base layout for the web pages:
https://getbootstrap.com/docs/4.5/getting-started/introduction/

The second important template is the checkout template that I integrated into the cart.html file. It is found at: https://stripe.com/docs/payments/checkout/migration

If you decide to create another app or start a new project, Django will create very base level views.py, manage.py, models.py, etc., files in order to begin routing your URL paths.

# Final Notes
This website is a very first draft and there are some things I definitely will continue to work on even after this course is completed! For time's sake, I wasn't able to create the "about", "media", and "tour" pages. These pages will mainly be HTML code with proper design efforts and hyperlinks to other Pinkshift-related URLs (socials, music streaming services, etc.)

When it comes to using this as a starting point for your own website/e-commerce site, all of the colors and fonts can be edited in the class="" portions of every HTML tags.

The next python-related features I want to include is perhaps a way for customers to create an account with this website so they can view previous orders and such. Perhaps it would also serve as a way for us to gather their email addresses and send them Pinkshift updates if they so desire. (The service I'm thinking of using would be Mailgun). I would also like to create a contact form for visitors to reach out and send messages/booking requests/etc. I also had the idea of including a comment section on the product detail page, kind of like a discussion section.

