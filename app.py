from sqlalchemy import create_engine,Column, Integer,String,ForeignKey,Date, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime as dt
from sqlalchemy import func
import csv



engine = create_engine('sqlite:///inventory.db',echo=False)
Session=sessionmaker(bind=engine)
session=Session()
Base=declarative_base()


class Brand(Base):
    __tablename__= 'brands'
    
    brand_id= Column (Integer,primary_key=True, autoincrement=True)
    brand_name= Column(String)
    products=relationship("Product",back_populates="brand")

    def __repr__(self):
        return f'brand_id:{self.brand_id} brand_name: {self.brand_name}'
  
    
class Product(Base):
    __tablename__= 'product'
    
    product_id= Column (Integer,primary_key=True, autoincrement=True)
    product_name= Column(String)
    product_price= Column(Integer)
    product_quantity= Column(Integer)    
    date_updated= Column(Date)
    brand_id=Column (Integer,ForeignKey("brands.brand_id"))
    brand = relationship("Brand", back_populates="products")
   
    
    def __repr__(self):
        return f'product_id:{self.product_id} product_name: {self.product_name} product_price: {self.product_price} product_quantity:{self.product_quantity} date_updated:{self.date_updated}brand_id:{self.brand_id}'  
        
      
def clean_price(price_str):
     return int(float(price_str[1:])*100)


def clean_date(date_str):
    month, day, year = map(lambda x: int(x), date_str.split('/'))
    return dt.date(year=year,  month=month, day=day)

#defining functions for PRODUCT CRUD Operation
def add_new_product():
    name= input('Product Name:  ')
    price = input('Product Price(Ex:$4.25): ')
    price_edit = clean_price(price)
    quantity=int(input('Product Quntity: '))
    # updated_date= input('Date Updated(Ex:1/20/2018): ')
    updated_date= dt.datetime.now()
    b_name = input("Brand Name: ")
    brand_d = get_brand_id(b_name)
    brand_d = int(brand_d.brand_id)
   
    pnew = Product(product_name=name, product_price=price_edit, product_quantity=quantity,date_updated = updated_date, brand_id = brand_d)
    session.add(pnew)
    session.commit()
    print("Product has been added")

    

def view_product_details():
    result = session.query(Product).all()
    for r in result:
        print(f'Product Id: {r.product_id}  Product Name:  {r.product_name}')
    while True:
        try: 
            opt = int(input("Enter Product Id: \n"))
        except ValueError:
            print("Must be a number!")
            continue
        break
    res = session.query(Product).filter(Product.product_id == opt).first()
    print(f"Name: {res.product_name}\nPrice: {res.product_price}\nQuantity: {res.product_quantity}\nUpdateD On:{res.date_updated}\nBrand Id:{res.brand_id}")    


def view_analysis():
   
   
    least_expensive= session.query(Product).order_by(Product.product_price).first()
    
    most_expensive=session.query(Product).order_by(Product.product_price.desc()).first()

    
    
    most_common_brand= session.query(Product.brand_id, func.count(Product.product_id).label('brand_id')).group_by(Product.brand_id).order_by(desc('brand_id')).first()
    popular_brand = get_brand_name(most_common_brand[0])


    print(f'''  
    \n****** PRODUCT ANALYSIS*****
    \r MOST EXPENSIVE: {most_expensive.product_name}
    \r LEAST EXPENSICE: {least_expensive.product_name}
    \r BRAND WITH THE MOST PRODUCTS:{popular_brand}   
    
    ''')


def create_backup_file_brands():
    
    # file2 = 'backup_inventory.csv'
    brands_list = []
    b_obj = {}
    brands = session.query(Brand).all()
    for brand in brands:
        b_obj = (brand.__dict__)
        
        for i in b_obj.copy():
            if i == "_sa_instance_state":
                b_obj.pop(i)
            elif i == "brand_id": 
                b_obj.pop(i)
        brands_list.append(b_obj)
   

    # getting  header for csv
    for j in brands_list:
        b_fieldname = list(j.keys())
        break
    
    # creating backup file for brands
    file1 = 'backup-inventory/backup_brands.csv'
    with open(file1 , 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=b_fieldname)
        writer.writeheader()
        writer.writerows(brands_list)

    print("Backup file for brands has been created!")

def create_backup_file_products():
    products_list = []
    p_obj = {}
    products = session.query(Product).all()
    for product in products:
        p_obj = (product.__dict__)
        for i in p_obj.copy():
            if i == "_sa_instance_state":
                p_obj.pop(i)
            elif i == "brand_id":
                b_name = get_brand_name(p_obj[i]) 
                p_obj.pop(i)
                p_obj['brand_name'] = str(b_name)
            
        products_list.append(p_obj)
   

    # getting  header for csv
    for j in products_list:
        p_fieldname = list(j.keys())
        break
    
    # creating backup file for products
    file2 = 'backup-inventory/backup_inventory.csv'
    with open(file2 , 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=p_fieldname)
        writer.writeheader()
        writer.writerows(products_list)

    print("Backup file for products has been created!")













def menu(): 
           
        print("\n Welcome to Grocery Inventory ")
        print("\n")
        print("----Menu ----")
        while True:
            print("\n Here are your choices:\nA) Display Menu \nB) Quit \n")
            option=input("\nEnter an option  A/B:  ").lower()
            if option== "":
                print("Option can't be left blank!")
                continue
            elif option.isnumeric():
                print("Can't be a number!Try again...")
                continue
            elif option != "a" and option != "b" :
                print("Not a valid option! Please select from the menu")      
            elif option == "a":
                while True:
                    print("""
                      \nINVENTORY MENU
                      \rv) View the details of a product
                      \rN) Add New Product
                      \rA) View Analysis
                      \rB) Backup the database """)
                                                                
                    UserOption=input('What would you like to do?').lower()                    
                    if UserOption == 'v':
                        view_product_details()
                    elif UserOption == 'n':
                        add_new_product()
                    elif UserOption == 'a':
                        view_analysis()
                    elif UserOption == 'b':
                        create_backup_file_brands()
                        create_backup_file_products()
                        
                      
                      
                      
            elif option =='b':
                print("Goodbye!")
                break

def brands_csv():
    with open("store-inventory/brands.csv",'r') as file:
        csvreader=csv.reader(file)
        for row in csvreader:
            if row [0] == 'brand_name':
                continue
            brand_name= row[0]
           

            new_brand = Brand(brand_name=brand_name)
           
            session.add(new_brand)
        session.commit()
            


def get_brand_id(name):
  
    b_id = session.query(Brand).filter(Brand.brand_name == name ).first()
    
    return b_id

def get_brand_name(id):
    b = session.query(Brand).filter(Brand.brand_id == id ).first()
    
    brand_name = b.brand_name
    return brand_name

def inventory_csv():
    csvRows = []
    with open("store-inventory/inventory.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'product_name':
                continue
            csvRows.append(row)
    for row in csvRows:
        product_in_db =session.query(Product).filter(Product.product_price==row[1]).one_or_none()
        if product_in_db == None:
            name= row[0]
            price= clean_price(row[1])
            quantity= int(row[2]) 
            date_updated=clean_date(row[3])
            brand_data = get_brand_id(row[4])
            brand_data = int(brand_data.brand_id)
            new_product= Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date_updated, brand_id = brand_data)
            session.add(new_product)
    session.commit()
   
    

    
               
          
            
            
        




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()   
  


    




