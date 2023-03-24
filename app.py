# import models 
# main menu: view details, add, search, analysis,exit
#edit product
#delete them
#search books
# data cleaning 
#Make a back up file for the database




from sqlalchemy import create_engine,Column, Integer,String,ForeignKey,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db',echo=False)
Session=sessionmaker(bind=engine)
session=Session()
Base=declarative_base()


class Brands(Base):
    __tablename__= 'brands'
    
    brand_id= Column (Integer,primary_key=True)
    brand_name= Column(String)

    def __repr__(self):
        return f"""   
        \nBrand ID {self.brand_id}\r
        \nBrand Name {self.brand_name}\r
        
        """
    
  
    
class Product(Base):
    __tablename__= 'product'
    
    product_id= Column (Integer,primary_key=True)
    product_name= Column(String)
    product_quantity= Column(Integer)
    product_price= Column(Integer)
    date_updated= Column(Date)
    brand_id=Column (Integer,ForeignKey("brands.id"))
   
    
    def __repr__(self):
        return f"""   
        \nProduct ID {self.product_id}\r
        \nProduct Name {self.product_name}\r
        \nProduct Quantity{self.product_quantity}\r
        \nProduct Price{self.product_price}\r
        \nDate Updated{self.date_updated}\r
        \nBrand ID{self.brand_id}
        """
    
    
if __name__ == '__main__' : 
    Base.metadata.create_all(engine)
    