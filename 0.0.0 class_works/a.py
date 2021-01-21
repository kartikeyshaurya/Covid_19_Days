

def validator(final_quantity,jug_1 , jug_2):
    '''
    takes three input and return whether it is applicapble or not 
    '''
    if(final_quantity > jug_1 or final_quantity):
        print("validation will not work")
        
def final_algo(jug_1, jug_2 , final_volume):
    state_1 = 0 
    state_2 = 0
    while(state_1 != final_volume and state_2 != final_volume):
        if(state_1 == 0) :
            state_1 = jug_1 
            print("current value of jug_1  is " + str(state_1) + "  and the second jug is " + str(state_2))
        elif(state_2 == jug_2):
            state_2 = 0
            print("current state of jog_1 is " + str(state_1) + " and the second jug is " + str(state_2))
        else :
            fin = min(jug_2-state_2 ,state_1 )
            state_2 = state_2 + fin
            state_1 = state_1 -fin
            print("current state of jUg_1 is " + str(state_1) + " and the second jug is " + str(state_2))

def waterjug():
    a = int(input("enter the total no of liter to find out "))
    jug1 = int(input("enter the quantiity of jug1 "))
    jug2 = int(input("enter the quantity of the jug2"))
    validator(a, jug1,jug2)
    final_algo(jug1,jug2,a)
    print("all right worked succesfully ")

waterjug()