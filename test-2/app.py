'''
เขียนโปรแกรมหาจำนวนเลข 0 ที่อยู่ติดกันหลังสุดของค่า factorial ด้วย Python โดยห้ามใช้ 
math.factorial เช่น 7! = 5040 มีเลข 0 ต่อท้าย 1 ตัว, 10! = 3628800 มีเลข 0 ต่อท้าย 2 ตัว
'''


def factorial(n):
    fact = 1
    for i in range(1, n +1):
        fact = fact * i
    print(f'ค่า factorial ของ {n} คือ {fact}')
    return fact

def check_zero(n):
    fac = factorial(n)
    num = 0
    for i in range(1, len(str(fac))+1):
        # print(str(fac)[-i])
        if str(fac)[-i] == '0':
            num += 1
        else:
            break
    return n, num, fac

fac = check_zero(10) # ใส่ค่า factorial ที่ต้องการหา
print(f'ค่า factorial ของ {fac[0]} คือ {fac[2]} มีเลข 0 ต่อท้าย {fac[1]} ตัว')