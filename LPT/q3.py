def foo(size:int) -> None:
    for i in range(size):
        for _ in range(size-i-1):
            print(" ", end="")
        
        for k in range(i+1,0,-1):
            print(k, end="")
        print("")

foo(1)