def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
        if len(part) > 1 and part[0] == '0':
            return False
    return True


print(is_valid_ip("192.168.1.1"))     # True
print(is_valid_ip("0.0.0.0"))         # True
print(is_valid_ip("255.255.255.255")) # True
print(is_valid_ip("256.1.1.1"))       # False (256 > 255)
print(is_valid_ip("192.168.01.1"))    # False (leading zero)
print(is_valid_ip("192.168.1"))       # False (only 3 parts)
print(is_valid_ip("192.168.1.1.1"))   # False (5 parts)