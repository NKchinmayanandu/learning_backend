temperatures = [73,74,75,71,69,72,76,73]
answers = []
l = []
for i,num in enumerate(temperatures):
    while answers:
        if num > temperatures[answers[-1]]:
            l.append(i-answers[-1])
            answers.pop(-1)
        else:
            break
    answers.append(i)
print(l)   
