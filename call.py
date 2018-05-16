import requests
import urllib, json
import math
import os
#Please note that just like the test cases provided the script takes in the path to the input txt file and output a
#txt file called output.txt. The user is prompted to enter both paths
#example of user input: input path: /users/blah/blah/blah/input.txt   output path: /users/blah/blah/blah/
#The reason I followed that input and output style is because it was the same as the sample test cases!
# Thank you for taking the time! :)

def callJSON():
    #open the file from the input path and load it as JSON data
    with open(inpPath) as json_data:
        inp = json.load(json_data)

    #Get necessary information from the referenced cart
    url1 = 'https://backend-challenge-fall-2018.herokuapp.com/carts.json?id='+str(inp['id'])+'&page=1'
    getInfo = requests.get(url1)
    info = getInfo.json()

    #Get number of items and number of pages information which will be used for our loops
    totalPages = math.ceil(float(info['pagination']['total'])/float(info['pagination']['per_page']))
    totalItems = info['pagination']['total']
    itemsPerPage = info['pagination']['per_page']
    #this is the dict that will store our final results that will later be dumped as JSON into a txt file
    outData = {}

    # Case 1: our discount is applied to the cart
    if inp['discount_type'] == 'cart':
        totalAmount = 0
        totalAmountAfterDiscount = 0
        i = totalItems
        j = 1

        #while there are still more pages
        while j != totalPages + 1:

            #Now we store the data from each page in order to do our calculations while considering items on each page
            url2 = 'https://backend-challenge-fall-2018.herokuapp.com/carts.json?id='+str(inp['id'])+'&page='+str(j)
            r = requests.get(url2)
            data = r.json()
            j = j+1

            #All the items in each page
            for p in range(0,itemsPerPage):

                #If we haven't considered all items in the cart yet
                if i != 0:
                    totalAmount = totalAmount + data['products'][p]['price']
                    i = i-1

                #If we reached the end we need to decide whether to do a discount or not, and consider all cases
                else:
                    #If there is no minimum cart value and out discount is greater then we simply pay 0
                    if 'cart_value' not in inp and inp['discount_value'] > totalAmount:
                        #Create output txt file and dump JSON data into it
                        open(outDirect+'/output.txt',"w+")
                        outData = {
                        "total_amount": totalAmount,
                        "total_after_discount": 0
                        }
                        with open(outDirect+'/output.txt', 'w') as outfile:
                            json.dump(outData, outfile, indent=2)

                    #If there is no cart value but our discount value is less or equal to out amount: do normal calc
                    if 'cart_value' not in inp and inp['discount_value'] <= totalAmount:

                        totalAmountAfterDiscount = totalAmount - inp['discount_value']
                        open(outDirect+'/output.txt',"w+")
                        outData = {
                        "total_amount": totalAmount,
                        "total_after_discount": totalAmountAfterDiscount
                        }
                        with open(outDirect+'/output.txt', 'w') as outfile:
                            json.dump(outData, outfile, indent=2)

                    #If we have a minimum cart value and our cart value is less than that: no discount
                    if 'cart_value' in inp and inp['cart_value'] > totalAmount:
                        open(outDirect+'/output.txt',"w+")
                        outData = {
                        "total_amount": totalAmount,
                        "total_after_discount": totalAmount
                        }
                        with open(outDirect+'/output.txt', 'w') as outfile:
                            json.dump(outData, outfile, indent=2)

                    #If we have a cart value and our total amount is greater than it and our total amount is greater than
                    #the discount value, do normal calculation
                    if 'cart_value' in inp and inp['cart_value'] <= totalAmount and inp['discount_value']<totalAmount:
                        totalAmountAfterDiscount = totalAmount - inp['discount_value']
                        open(outDirect+'/output.txt',"w+")
                        outData = {
                        "total_amount": totalAmount,
                        "total_after_discount": totalAmountAfterDiscount
                        }

                        with open(outDirect+'/output.txt', 'w') as outfile:
                            json.dump(outData, outfile, indent=2)

                    #If we have a cart value and our total amount is greater than or equal to it and our total amount is less than
                    #the discount value, we simply pay 0
                    if 'cart_value' in inp and inp['cart_value'] <= totalAmount and inp['discount_value']>totalAmount:
                        totalAmountAfterDiscount = 0
                        open(outDirect+'/output.txt',"w+")
                        outData = {
                        "total_amount": totalAmount,
                        "total_after_discount": totalAmountAfterDiscount
                        }
                        with open(outDirect+'/output.txt', 'w') as outfile:
                            json.dump(outData, outfile, indent=2)


    #If the discount type was product
    if inp['discount_type'] == 'product':
        totalAmount = 0
        totalAmountAfterDiscount = 0
        discountValue = 0
        i = totalItems
        j = 1

        while j != totalPages+1:
            url2 = 'https://backend-challenge-fall-2018.herokuapp.com/carts.json?id='+str(inp['id'])+'&page='+str(j)
            r = requests.get(url2)
            data = r.json()
            j = j+1


            for p in range(0,itemsPerPage):
                if i != 0:
                    #At every product add to the total amount
                    totalAmount = totalAmount + data['products'][p]['price']

                    #Considering all the cases where a discount applies to the product
                    if ('collection' not in inp and 'product_value' not in inp):
                        #if: if a product's price is less than the discount then the discount is
                        #just that product's price (i.e: we can't have negative numbers)
                        if data['products'][p]['price'] - inp['discount_value'] < 0:
                            discountValue = discountValue + data['products'][p]['price']
                        else:
                        #else the price of the product is equal or greater than the discount value, just do normal calculation
                            discountValue = discountValue + inp['discount_value']

                    if ('collection' not in inp and 'product_value' in inp and data['products'][p]['price'] > inp['product_value']):
                        if data['products'][p]['price'] - inp['discount_value'] < 0:
                            discountValue = discountValue + data['products'][p]['price']
                        else:
                            discountValue = discountValue + inp['discount_value']

                    if ('collection' in inp and 'collection' in data['products'][p] and data['products'][p]['collection'] == inp['collection'] and 'product_value' not in inp):
                        if data['products'][p]['price'] - inp['discount_value'] < 0:
                            discountValue = discountValue + data['products'][p]['price']
                        else:
                            discountValue = discountValue + inp['discount_value']
                        print totalAmountAfterDiscount

                    if ('collection' in inp and 'collection' in data['products'][p] and data['products'][p]['collection'] == inp['collection'] and 'product_value' in inp and data['products'][p]['price'] > inp['product_value']):
                        if data['products'][p]['price'] - inp['discount_value'] < 0:
                            discountValue = discountValue + data['products'][p]['price']
                        else:
                            discountValue = discountValue + inp['discount_value']

                    else:
                        totalAmountAfterDiscount = totalAmount - discountValue

                    i = i-1

                else:
                    #Dump the output values in JSON format onto txt file
                    open(outDirect+'/output.txt',"w+")
                    outData = {
                    "total_amount": totalAmount,
                    "total_after_discount": totalAmountAfterDiscount
                    }
                    with open(outDirect+'/output.txt', 'w') as outfile:
                        json.dump(outData, outfile, indent=2)


inpPath = raw_input("Where is your input JSON file? Please enter absolute path, and include the input file name in the path\n")
if os.path.exists(inpPath) == False:
    raise ValueError('The input path you entered does not exist')

outDirect = raw_input("Where would you like to save your output file? Please enter absolute path\n")
if os.path.isdir(outDirect) == False:
    raise ValueError('The output path you entered does not exist')



callJSON()
