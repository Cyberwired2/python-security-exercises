def generate_port_range(start, end):
    """Generate a list of ports from start to end (inclusive)"""
    if not (0 <= start <= 65535 and 0 <= end <= 65535):
        raise ValueError("Ports must be between 0-65535")
    return list(range(start, end + 1))

# Test
print(generate_port_range(80, 85))  # Output: [80, 81, 82, 83, 84, 85]