## Django Sales Order API

### Quick Setup

Clone project using this command:

```commandline
git clone https://github.com/solanoize/sales-order-api.git
cd sales-order-api
```

Create virtual environment for this project and activate it with Command Prompt (no PowerShell) using this command:

```
python -m venv .venv
.venv\Script\activate
```

Install dependencies:

```commandline
pip install -r requirements.txt
```
Create super user (admin)

```commandline
python manage.py createsuperuser
```

generate products and customers

```commandline
python manage.py generate_fake_customer
python manage.py generate_fake_product
```

Run this project:

```commandline
python manage.py runserver
```

Access http://localhost:8000/admin in your browser and log in!