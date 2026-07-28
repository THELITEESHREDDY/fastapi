from pydantic import BaseModel


#DTO data transform objects
class ProductDTO(BaseModel):
    id:int
    title:str
    price:int = 0
    count:int = 0