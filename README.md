# wsb_sentiment

## Contexto
No final de Janeiro a empresa americana GameStop (sigla GME) teve um aumento de mais de 1000% no valor de suas ações. A empresa vem sofrendo descrédito no mercado por ser considerada uma decadente no varejo de jogos eletrônicos, o que ocasionou na prática de "shorting" por parte dos maiores fundos de investimento americanos. 

De forma resumida, o "shorting" é a prática de tomar emprestadas ações de uma determinada empresa, vendê-las ao preço atual e esperar que o preço caia, para assim comprar as ações em um preço mais baixo e quitar sua dívida, tendo como lucro essa diferença de preços. Ou seja, o investidor ganha com a queda do valor das ações.

Entretanto, ao tomar as ações emprestadas, o investidor se compromete em comprá-las no futuro, independente de qual seja o valor. 

Percebendo que mais de 100% das ações da GME estavam emprestadas, um grupo de integrantes do forúm Reddit, em específico a subreddit r/Wallstreetbets, iniciou um movimento de compra em massa dessas ações, pois estando emprestadas elas teriam que ser compradas de volta pelos fundos de investimento ao preço que for, mesmo que seja absurdamente alto, prática conhecida como "short squeeze".

fontes:https://www.usatoday.com/story/money/markets/2021/02/02/gamestop-stock-reddit-wallstreetbets-users-discuss-gme-short-squeeze/4310623001/

## A aplicação
Essa aplicação foi criada com o intuito de observar o impacto que os comentários na subreddit r/wallstreetbets teria nas ações da $GME e vice-versa.
A aplicação utiliza o pacote TextBlob para fazer a análise de sentimentos, que por sua vez é um wrapper para o NLTK. Em específico, os comentários do post de "Daily Discussion" são o alvo de análise.
O gŕafico superior esquerdo é uma média da polaridade dos comentários nos últimos 60 segundos. Tais comentários podem ser lidos na tabela a direita desse gráfico. Abaixo, o gráfico das ações da $GME atualizados por minuto, retirados do Yahoo Finance.
