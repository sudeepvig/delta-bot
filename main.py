from delta_rest_client import DeltaRestClient, OrderType
import threading
import os

api_key = os.getenv("DELTA_API_KEY")
api_secret = os.getenv("DELTA_API_SECRET")

PRODUCT_ID = 84
ORDER_SIZE = 1


# =====================================
# THREAD LOCK
# =====================================

trade_lock = threading.Lock()


# =====================================
# DELTA CLIENT
# =====================================

delta_client = DeltaRestClient(
    base_url="https://cdn-ind.testnet.deltaex.org",
    api_key=api_key,
    api_secret=api_secret
)



# =====================================
# GET POSITION
# =====================================

def get_current_position():

    try:

        position = delta_client.get_position(PRODUCT_ID)

        print("\n========== CURRENT POSITION ==========")
        print(position)
        print("======================================\n")

        return float(position.get("size", 0))


    except Exception as e:

        print("Position Error:", e)

        return 0



# =====================================
# BUY ORDER
# =====================================

def open_long():

    print("Opening LONG", ORDER_SIZE)

    response = delta_client.place_order(

        product_id=PRODUCT_ID,
        size=ORDER_SIZE,
        side="buy",
        order_type=OrderType.MARKET

    )

    print(response)



# =====================================
# SELL ORDER
# =====================================

def open_short():

    print("Opening SHORT", ORDER_SIZE)

    response = delta_client.place_order(

        product_id=PRODUCT_ID,
        size=ORDER_SIZE,
        side="sell",
        order_type=OrderType.MARKET

    )

    print(response)



# =====================================
# MAIN TRADE FUNCTION
# =====================================

def place_trade(signal):


    # prevents multiple alerts running together
    with trade_lock:


        print("\n====================================")
        print("SIGNAL RECEIVED:", signal)
        print("====================================\n")


        current_size = get_current_position()



        # =============================
        # BUY SIGNAL
        # =============================

        if signal == "BUY":


            # already LONG
            if current_size > 0:

                print("Already LONG. Ignoring BUY.")
                return



            # SHORT exists
            if current_size < 0:


                print("SHORT position detected.")
                print("Closing SHORT first...")


                delta_client.place_order(

                    product_id=PRODUCT_ID,
                    size=abs(current_size),
                    side="buy",
                    order_type=OrderType.MARKET

                )


                print("SHORT closed.")



            open_long()



        # =============================
        # SELL SIGNAL
        # =============================

        elif signal == "SELL":



            # already SHORT
            if current_size < 0:


                print("Already SHORT. Ignoring SELL.")
                return




            # LONG exists
            if current_size > 0:


                print("LONG position detected.")
                print("Closing LONG first...")


                delta_client.place_order(

                    product_id=PRODUCT_ID,
                    size=current_size,
                    side="sell",
                    order_type=OrderType.MARKET

                )


                print("LONG closed.")




            open_short()



        else:


            print("Unknown signal:", signal)





# =====================================
# TEST POSITION
# =====================================

if __name__ == "__main__":


    print("Delta Bot Started")

    size = get_current_position()


    if size > 0:

        print("Current Position: LONG")


    elif size < 0:

        print("Current Position: SHORT")


    else:

        print("Current Position: NONE")