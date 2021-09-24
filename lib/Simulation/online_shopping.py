class Order():
    def __init__(self, oid, dest, when_ordered, food, supplies):
        self.oid = oid

        self.dest = dest
        self.dest_id = dest.homeId
        self.when_ordered = when_ordered

        self.retailer = None
        self.delivery_agent = None
        self.when_delivered = None

        self.is_food = food
        # self.is_supplies = supplies

class OnlineShopping():
    order_history = []
    orders = []
    n_orders = 0

    @staticmethod
    def place_order(dest, when_ordered, food, supplies):
        # print("Placing order #", OnlineShopping.n_orders)

        dest.waiting_order = True
        new_order = Order(OnlineShopping.n_orders, dest, when_ordered, food, supplies)
        OnlineShopping.orders.append(new_order)
        OnlineShopping.order_history.append(new_order)
        OnlineShopping.n_orders +=1

    @staticmethod
    def get_orders(agent, n=1):
        my_orders = []

        n = min(len(OnlineShopping.orders), n)

        for _ in range(n):
            my_new_order = OnlineShopping.orders.pop(0)

            my_new_order.retailer = agent.mainJob.building.buildingId
            my_new_order.delivery_agent = agent.agentId

            my_orders.append(my_new_order)

        return my_orders

    @staticmethod
    def delivery(order, when_delivered):
        order.when_delivered = when_delivered

        if order.is_food:
            order.dest.buyGroceries()
            order.dest.waiting_order_food = False
        # if order.supplies:
        #     order.dest.buySupplies()
        #     order.dest.waiting_order_supplies = False

    @staticmethod
    def str_orders_history():
        out = [f"Total orders: {OnlineShopping.n_orders}"]
        out.append(f"ORDER_ID,HOME_ID,STORE_ID,WORKER_ID,ORDER_DATE,DELIVERY_DATE")
        for order in OnlineShopping.order_history:
            out.append(f"{order.oid},{order.dest_id},{order.retailer},{order.delivery_agent},{order.when_ordered},{order.when_delivered}")


        return "\n".join(out)
