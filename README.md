
<p align="center">
  <a href="https://github.com/bbc/peaks.js"><img src="static/images/logo.svg" alt="Rafcart" height="120" /></a>
</p>

#

<p align="center">
  <strong>
  An e-commerce website built with Django and Tailwind CSS.
  </strong>
</p>



## Features
- [x] Pages - Contact | About
- [x] User - Register | Edit | Login | Logout | Password Reset | Password Change
- [ ] Authentication - Login with Google | 2FA | Account Verify (optional)
- [x] Categories - List | Detail
- [ ] Products - List | Detail | Search(live search with htmx) | Filter | Wishlist, Rating, Reviews, ProductSpecifications(like color, size, etc, depending on the product)
- [x] Cart - Add to Cart | Remove from Cart
- [ ] Checkout - Payment | Order Summary | Order History | Invoice


## Installation

1. Clone the repository
```bash 
git clone https://github.com/dashgin/awesome-commerce.git
``` 

2. Create a virtual environment and install the dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Migrate the database and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server
```bash
python manage.py runserver
```

### Visit the website at [http://localhost:8000](http://localhost:8000)


## Credits
HTML template credit: [https://github.com/fajar7xx/ecommerce-template-tailwind-1](https://github.com/fajar7xx/ecommerce-template-tailwind-1)


