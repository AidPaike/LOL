list = [("w",2),('a',6),('f',56),('wr',23)]
dislike = ["w","a"]
for i in range(0,len(dislike)):
    for j in range(0,len(list)):
        if dislike[i] in list[j]:
            list.remove(list[j])
            break
print(list)