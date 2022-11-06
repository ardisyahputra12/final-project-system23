# **Final Project - System23**

Backend repository for System23

>**IP: 34.142.211.35**

## **Notes**

---

- For testing project is work temporary: Run docker compose (use Makefile), then hit api with endpoint /image (in file universal.py). ex. [127.0.0.1:5000/image] or [34.142.211.35:5000/image]
- Models is created, feel free for add or delete it if you think that's right

## **How to run query use sql or orm**

---
If you forget how to run query use sql or orm, this could be test in file routes/product. Example:

```py
@products_bp.route("test", methods=["GET"])
def test_only():
    run_query(f"DELETE FROM products", True)

    run_query(f"INSERT INTO products VALUES ('{uuid.uuid4()}', 'cid1', 'tas', 20, 'lorem', 'S', 'used', 'image1', '[image1, image2]', '{datetime_format()}', 'admin')", True)
    
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="baju", price=100, detail="lorem ipsum", size="L", condition="used", image="image1", images_url=["image4", "image5"], create_at=datetime_format(), create_by="Ardi"), True)

    run_query(f"INSERT INTO products (id, category_id, name, price, size, condition, image, create_by) VALUES ('{uuid.uuid4()}', 'cid1', 'tas', 101, 'M',  'new', 'image2', 'Saya')", True)
    
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="baju", price=100, detail="haloooooooo", condition="new", image="image2", create_by='Kamu'), True)

    query = run_query("SELECT * FROM products")
    orm = run_query(select(Products))

    return {
        "query": query,
        "orm": orm,
    },200
```

## **Connect to local with ssh (Windows/WSL)**

---

- cd .ssh
- ssh-keygen -t rsa -f [FILENAME] -C [USERNAME] -b 2048
- type [FILENAME].pub
- copy public key to GCP and add in security section
- finally you can connect via ssh using vs code

Test connect in cmd:

- ssh [USERNAME]@34.142.211.35 -i [FILENAME]

Test IP, run command:

- make build
- curl 34.142.211.35:5000/image

## **Endpoint section in requirements file**

---

>### Rully

- home.py: Home
- auth.py: Authentication
- user.py:
  - Profile page
  - Cart
  - Admin page

>### Faris

- universal.py: Universal
- order.py:
  - Profile page
  - Cart
  - Admin page
- cart.py:
  - Cart
  - Product detail page

>### Ardi

- product.py:
  - Product list
  - Product detail page
  - Admin page
- category.py:
  - Product list
  - Admin page
