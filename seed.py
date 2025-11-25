from app import db
from app.models import ItemCardapio

itens = [
    ItemCardapio(
        nome="Morango do Amor",
        descricao="Morango coberto com chocolate e confeitos coloridos, uma explosão de fofura e sabor.",
        preco=12.50,
        disponivel=True,
        categoria="Sobremesa"
    ),
    ItemCardapio(
        nome="Dubai Chocolate",
        descricao="Delicioso chocolate cremoso servido com chantilly e lascas de amêndoas.",
        preco=15.00,
        disponivel=True,
        categoria="Sobremesa"
    ),
    ItemCardapio(
        nome="Sorvete de Pistache",
        descricao="Sorvete artesanal de pistache, cremoso e refrescante.",
        preco=10.00,
        disponivel=True,
        categoria="Sobremesa"
    ),
    ItemCardapio(
        nome="Bibimbap",
        descricao="Tradicional prato coreano com arroz, vegetais variados, ovo e molho picante.",
        preco=28.00,
        disponivel=True,
        categoria="Prato Principal"
    ),
    ItemCardapio(
        nome="Kimchi",
        descricao="Clássico acompanhamento coreano de repolho fermentado picante.",
        preco=8.00,
        disponivel=True,
        categoria="Acompanhamento"
    ),
    ItemCardapio(
        nome="Tteokbokki",
        descricao="Bolinhos de arroz cozidos em molho picante e doce, irresistível e divertido.",
        preco=18.50,
        disponivel=True,
        categoria="Lanche"
    ),
    ItemCardapio(
        nome="Chá de Flor de Cerejeira",
        descricao="Bebida delicada, floral e levemente adocicada.",
        preco=9.50,
        disponivel=True,
        categoria="Bebida"
    ),
    ItemCardapio(
        nome="Soju de Melancia",
        descricao="Bebida alcoólica coreana sabor melancia, refrescante e doce.",
        preco=22.00,
        disponivel=True,
        categoria="Bebida"
    ),
    ItemCardapio(
        nome="Dorayaki de Feijão Vermelho",
        descricao="Panquecas japonesas recheadas com pasta de feijão vermelho, fofinhas e doces.",
        preco=7.50,
        disponivel=True,
        categoria="Sobremesa"
    ),
    ItemCardapio(
        nome="Frappuccino Coreano",
        descricao="Bebida gelada com café, leite e cobertura de chantilly, divertida e colorida.",
        preco=14.00,
        disponivel=True,
        categoria="Bebida"
    )
]

for item in itens:
    db.session.add(item)

db.session.commit()
print("Itens do cardápio inseridos com sucesso!")
