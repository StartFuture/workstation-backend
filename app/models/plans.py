import logging

'''

Padroes preço:

horas, preço hora

'''


def get_price_hour(type_plan):
    valid_types = {'daily_plan', 'month_plan', 'custom_plan'}
    
    raw_price_hour = 10 # defined in bussines rule
    
    promotion_rate_percent = 1
    
    if type_plan in valid_types:

        if type_plan == 'month_plan':
            promotion_rate_percent = 0.9
        elif type_plan == 'custom_plan':
            promotion_rate_percent = 0.85
        
        price_hour = raw_price_hour * promotion_rate_percent
        
        return price_hour
    
    else:
        logging.warning(f'type: {type_plan} Invalid')
        return False    

def calculate_price_plan(hours : float, type_plan : str, price_hour=None):
    
    if not price_hour:
        price_hour = get_price_hour(type_plan=type_plan)
        if not price_hour:
            return False
    
    total_price = price_hour * hours
    
    return total_price