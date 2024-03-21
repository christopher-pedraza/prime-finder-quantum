n = 77

for g in range(2, n):
    # Check whether g shares a factor with n
    if n % g == 0:
        continue

    # Get a g to the power of r that is equals to mN+1, where m is a constant and N is the number we are testing
    # Test all g's to the power of r until we find one that satisfies the condition of being one more than a multiple of N and
    # having an even r
    r = 1
    while (g**r) % n != 1 or r % 2 == 1:
        r += 1

    print(f"{g}^{r} = {g**r} (mod {n})")
    continue
