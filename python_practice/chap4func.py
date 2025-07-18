def create_mail(receiver, bill):
    msg = f"""{receiver}様
祇園企画の長野です。
今月の請求額は、{bill}です。
"""
    print(msg)



def add_charge(bill):
    return int(bill * 1.07)
