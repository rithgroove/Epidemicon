class Order():
    def __init__(self, oid, dest, when_ordered, food, grocery):
        self.oid = oid

        self.dest = dest
        self.dest_id = dest.homeId
        self.when_ordered = when_ordered

        self.retailer = None
        self.delivery_agent = None
        self.when_delivered = None

        self.is_food = food
        self.is_grocery = grocery

class OnlineShopping():
    n_orders = 0
    order_history = []
    
    orders_food = []
    orders_grocery = []
    
    delivery_type = "none" #"retail", "both", "none"
    is_delivery_retail     = False
    is_delivery_restaurant = False

    @staticmethod
    def set_delivery_type(delivery_type):
        OnlineShopping.delivery_type = delivery_type
        OnlineShopping.is_delivery_retail     = delivery_type=="retail"     or delivery_type=="both"
        OnlineShopping.is_delivery_restaurant = delivery_type=="restaurant" or delivery_type=="both"

    @staticmethod
    def place_order(dest, when_ordered, food_or_grocery):
        # print("Placing order #", OnlineShopping.n_orders)

        new_order = Order(OnlineShopping.n_orders, dest, when_ordered, food_or_grocery=="food", food_or_grocery=="grocery")        
        if food_or_grocery=="food":
            # dest.waiting_order_food = True
            OnlineShopping.orders_food.append(new_order)
        else:
            dest.waiting_order_grocery = True
            OnlineShopping.orders_grocery.append(new_order)
        
        OnlineShopping.order_history.append(new_order)
        OnlineShopping.n_orders +=1

    @staticmethod
    def get_orders(agent, n=1):
        my_orders = []
    
        if agent.mainJob.jobClass.name=="delivery_food":
            orders = OnlineShopping.orders_food
        else:#"delivery_grocery"
            orders = OnlineShopping.orders_grocery

        n = min(len(orders), n)

        for _ in range(n):
            my_new_order = orders.pop(0)

            my_new_order.retailer = agent.mainJob.building.buildingId
            my_new_order.delivery_agent = agent.agentId

            my_orders.append(my_new_order)

        return my_orders

    @staticmethod
    def delivery(order, when_delivered):
        order.when_delivered = when_delivered

        if order.is_food:
            order.dest.buyGroceries(n=1)
            # order.dest.waiting_order_food = False
        else:#order.is_grocery:
            order.dest.buyGroceries(n=6)
            order.dest.waiting_order_grocery = False
            

    @staticmethod
    def str_orders_history():
        out = [f"Total orders: {OnlineShopping.n_orders}"]
        out.append(f"ORDER_ID,HOME_ID,STORE_ID,WORKER_ID,ORDER_DATE,DELIVERY_DATE")
        for order in OnlineShopping.order_history:
            out.append(f"{order.oid},{order.dest_id},{order.retailer},{order.delivery_agent},{order.when_ordered},{order.when_delivered}")

        return "\n".join(out)