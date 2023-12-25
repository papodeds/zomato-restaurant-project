# Projeto de conclusão do curso: <br> *Fast Track Course: analisando dados com Python* <br> pela *Comunidade DS*<br><br> Estudo de caso sobre a plataforma: *ZOMATO restaurant partners®*

# *Sobre a ZOMATO®*
Lançada em 2010, a *ZOMATO®* é uma plataforma tecnológica que atua como um elo entre clientes, restaurantes e entregadores, atendendo a várias necessidades.
Os clientes usam a plataforma para descobrir restaurantes, fazer avaliações, ver fotos, pedir comida, reservar mesas e pagar suas refeições.
Aos parceiros donos de restaurantes, oferecemos ferramentas de marketing especiais para ajudar a expandir seus negócios, além de um serviço de entrega confiável.
E não esquecemos dos parceiros de entrega, que têm a chance de ganhar dinheiro de forma transparente e flexível. 
Queremos que todos façam parte dessa experiência!

# *1. Problema de negócio*
A *ZOMATO®*, com a meta ambiciosa de alavancar seu negócio por meio de seu *marketplace* voltado para o segmento de restaurantes, contratou um novo CEO para reestruturar seu planejamento, ampliar seu *market share* e torná-la líder de mercado nesse segmento.
O CEO, por sua vez, planeja implementar uma cultura de decisões baseada em dados, utilizando o histórico de dados coletados no *marketplace* para orientar o início do projeto. 
Assim, ele precisou contratar um cientista de dados para extrair, transformar e carregar os dados da empresa, além de fornecer métricas detalhadas por meio de dashboards interativos. 
Isso permitirá que o CEO tome as melhores decisões e estruture o novo planejamento para a *ZOMATO®*.

# *2. Premissas assumidas para construir a solução*

- Foi assumido o modelo de *marketplace* para o negócio.
- A base de dados utilizada é pública e está disponível na plataforma Kaggle através do link:https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
- Foram construídos cinco painéis interativos para facilitar a visualização das principais métricas do negócio, sendo elas:
  - A visão geral dos dados cadastrados e localização geográfica dos restaurantes.
  - A visão por países.
  - A visão por cidades.
  - A visão por restaurantes.
  - A visão por tipo de culinárias.

# *3. Estratégia da solução*

A construção dos painéis interativos a partir da base de dados pública foi a opção adotada para facilitar a apresentação de métricas relevantes do negócio de uma forma visual e objetiva ao novo CEO, para auxiliá-lo a compreender melhor sobre o atual contexto da empresa.

Os painéis construídos foram organizados da seguinte maneira:

- A visão Geral
  - Países atendidos
  - Cidades atendidas
  - Restaurantes cadastrados
  - Culinárias oferecidas
  - Avaliações na plataforma
  - Mapa com a localização geográfica dos restaurantes cadastrados
  
- A visão por países
  - O número de restaurantes cadastrados por país
  - O número de cidades atendidas por país
  - Os tipos de culinárias oferecidas por país
  - A média de avaliações na plataforma por país
  - A média do custo de refeições para duas pessoas por país

- A visão por cidades
  - TOP "X" - Cidades com mais restaurantes cadastrados
  - TOP "X" - Cidades com mais restaurantes avaliados acima de 4.0
  - TOP "X" - Cidades com mais restaurantes avaliados abaixo de 2.5
  - TOP "X" - Cidades com mais tipos de culinárias disponíveis

- A visão por restaurantes
  - TOP "X" - Restaurantes com a melhor média de avaliação
  - TOP "X" - Restaurantes com o prato para duas pessoas mais caro
  - TOP "X" - Restaurantes com o prato para duas pessoas mais barato
  - Restaurantes que fazem entregas online
  - Restaurantes que fazem reservas de mesa
    
- A visão por culinárias
  - Restaurante cadastrado com a melhor avaliação média por tipo de culinária
  - TOP "X" - Culinárias com melhor média de avaliação e mais votos
  - TOP "X" - Culinária com maior preço médio de prato para duas pessoas
  - TOP "X" - Culinárias, cujos restaurantes aceitam pedidos online e fazem entregas

# *4. Principais insights*
- A *ZOMATO®* está presente em 5 dos 6 continentes: África, Américas, Ásia, Europa e na Oceania.
- Índia e EUA são os países com maior número de restaurantes e cidades cadastrados.
- Indonésia e Índia são os países com maior quantidade média de avaliações.
- Com execessão do Brasil todos os outros 14 países cadastrados tem a média de avaliações acima dos 4.0 pontos.
- Qatar, Inglaterra e Canadá possuem as cidades que oferecem a maior diversidade de culinárias.
- Três das dez cidades com mais restaurantes avaliados em média abaixo de 2.5 estão no Brasil.
- A maior parte dos restaurantes cadastrados não fazem entregas on-line (64,7%) e não reservam mesas (93,9%).
- As culinárias com maior número de avaliações e com maior média de avalição são: Continental, Européia, Barbecue, Indiana, Sushi e Cafeteria.
    
# *5. O produto final do projeto*
Um conjunto de painéis iterativos hospedados em cloud que está disponível para acesso de qualquer dispositivo com conexão à internet. 
Para acessá-los basta clicar no link a seguir: https://papodeds-zomato-restaurant-project.streamlit.app/

# *6. Conclusões*
A partir da implementação dos painéis interativos o novo CEO terá uma maior gama de informações e métricas relevantes sobre o negócio para elaborar com assertividade a reestruturação do planejamento de negócio que poderá levar a *ZOMATO®* a um outro patamar, tornando-a líder global no segmento dos *marketplaces* que atendem a restaurantes.

# *7. Próximos passos*
- Coletar dados dos clientes.
- Otimizar o banco de dados, eliminando colunas irrelevantes e adicionando colunas com dados originais e derivados que gerem maior valor ao negócio.
- A partir da coleta de dados dos clientes, implementar modelos de aprendizado de máquina preditivos e de recomendações.
- Adicionar novas visões de negócio.
