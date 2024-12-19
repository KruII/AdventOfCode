import time

def auto_send(requester, first, second, star):
    star_results = [0,0]
    
    if star == 0:
        star_results[0] = requester.send_result("1", first)
        star = requester.check_day_success()
        time.sleep(5)
    if star == 1:
        star_results[1] = requester.send_result("2", second)
    if (star == 2):
        star_results[0] = {1:"Completed"}
    star = requester.check_day_success()
    return ([first, second, star, star_results])