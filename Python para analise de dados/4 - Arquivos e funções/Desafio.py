def investimento_cds (cds: int, valor: float):
    for i in range(cds):
        valor += float(input(f'Digite o valor do CD {i+1}: '))
    print(f'Preço total: R${valor:.2f}\nMédia de custo por CD: R${valor/cds:.2f}')

cds = int(input('Digite a quantidade de CDs: '))
valor = 0

investimento_cds(cds=cds, valor=valor)