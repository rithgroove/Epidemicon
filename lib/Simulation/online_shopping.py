class Order():
    def __init__(self, oid, dest, retailer, when_ordered, when_to_delivery):
        self.oid = oid
        
        self.dest     = dest
        self.retailer = retailer
        
        self.when_ordered     = when_ordered
        self.when_to_delivery = when_to_delivery

class OnlineShopping():
    orders = []
    n_orders = 0
    
    @staticmethod
    def place_order(dest, retailer, when_ordered):
        print("Placing order #", OnlineShopping.n_orders)
    
        when_to_delivery = when_ordered#+1day
        
        new_order = Order(OnlineShopping.n_orders, dest, retailer, when_ordered, when_to_delivery)
        OnlineShopping.orders.append(new_order)
        OnlineShopping.n_orders +=1
    
    @staticmethod
    def get_orders(n=1):
        try:
            n = min(len(OnlineShopping.orders), n)
            my_orders = [OnlineShopping.orders.pop(0) for _ in range(n)]
        except IndexError:#len(OnlineShopping.orders)==0:
            my_orders = []
            
        return my_orders
        
        
        
        