import os.path

index = 1
while os.path.isfile(f'input/entrada{index}.txt'):
    input = open(f'input/entrada{index}.txt', 'r')
    print(input.read())
    output = open(f'output/saida{index}.txt', 'w')
    output.write(f'Output number {index}')
    output.close()

    index += 1