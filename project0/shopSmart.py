# shopSmart.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
 
    s1=fruitShops[0].getPriceOfOrder(orderList) #invoke getPriceOfOrder class function, fruitshops[0] means shop1
    s2=fruitShops[1].getPriceOfOrder(orderList) #invoke getPriceOfOrder class function, fruitshops[0] means shop2
    
    if s1 == s2 == None:   #shop1 and shop2 can't offer the fruit required in the order
        return None
    elif s1!= None and s2 == None:  #shop2 can't offer the fruit required in the order, the only choice is shop1
        return fruitShops[0]
    elif s1 == None and s2 != None:
        return fruitShops[1]
    elif s1 > s2:    #shop1 and shop2 can both meet the requirement, s1 is expensive so we should choose shop2
        return fruitShops[1]
    else:
        return fruitShops[0]
        
        

    
if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print ("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print ("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
