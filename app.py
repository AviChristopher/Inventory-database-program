#Auto generate product ID
#auto generate brand ID in brands model and product model as a foreign key


from sqlalchemy import create_engine,Column, Integer,String,ForeignKey,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime as dt
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

                    
                    if UserOption in [ 'v','n','a','b']:
                       return UserOption
                    else:
                        print(''' 
                        \rPlease choose from the list!
                        \rPress enter to try again''')                          
            
                      
                      
                      
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
            #print(f'>>>>>{brand_name}')

            new_brand = Brand(brand_name=brand_name)
            #print(f"Here you go {new_brand}") 
            session.add(new_brand)
        session.commit()
            


def get_brand_id(name):
    b_id = session.query(Brand).filter(Brand.brand_name == name ).first()

    return b_id

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
   
    

#Capturing User option and running the app

def start_app():
    while True:
       UserOption=menu()
       if UserOption == 'V':
         #View a single product 
         # Query                
           pass       
       elif UserOption == 'N':
        #   product_name= input('Product Name:  ')
        #   product_price = input('Product Price(Ex:$4.25): ')
        #   product_quantity=input('Product Quntity: ')
        #   date_updated= input('Date Updated(Ex:1/20/2018): ')

           #Query session .query. add()
           pass
       elif UserOption == 'A':
           #View Analysis
           #filter and conditions
           pass
       elif UserOption == 'B':
           #Back Up the data
           pass
       else:
           print('Good bye')
           
           
       




if __name__ == '__main__':
    Base.metadata.create_all(engine)   
    #start_app()
    #clean_price ( '$5.70')
    #clean_date('12/19/2018')
    brands_csv()
    inventory_csv()

    # result = session.query(Product).all()
    # for r in result:
    #     print(f'Loop for rrrrr{r}')

    for product in session.query(Product):
        print(product)





