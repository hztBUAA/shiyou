def replace_chars(input_str, k):
    output_str = ""
    last_seen = {}

    for i, char in enumerate(input_str):
        if char in last_seen and i - last_seen[char] <= k:
            output_str += '-'
        else:
            output_str += char

        last_seen[char] = i

    return output_str

if __name__ == '__main__':
    input_str, input_k = input().split()
    input_k = int(input_k)
    
    print(replace_chars(input_str, input_k))