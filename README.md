# FTM

Uma característica comum a maioria dos crimes perpetrados através da internet é a transnacionalidade. Um website de distribuição de pornografia infantil, por exemplo, pode ter o nome de domínio Sueco (.se), um provedor Russo e um CDN (Content Delivery Network) sediado nos EUA com servidores espalhados por todo o mundo.

Qual o caminho a ser percorrido pela autoridade brasileira que estiver a cargo de identificar e responsabilizar o autor do delito? Os pedidos de cooperação internacional, ainda que haja acordo entre o Brasil e o país destinatário, demanda muito tempo. Por esta razão só devem ser utilizados quando forem estritamente necessários e da forma mais eficaz, buscando sempre alcançar a prova de autoria do delito com o menor número possível de interações internacionais.

Com o fito de auxiliar as autoridades brasileiras e as vítimas, desenvolvemos o Follow the Money – FTM, um software livre escrito em Python 3.5, que reúne informações publicamente disponíveis que possam levar à autoria do ilícito.

Para além das informações habituais relativas ao nome de domínio e a hospedagem (www), o FTM busca por todos os serviços vinculados ao domínio raiz (e-mails, blogs, panéis de administração e/ou desenvolvimento, etc) bem como aplicações relativas a estatísticas, publicidade e redes sociais fornecidas por empresas com representação no Brasil.

Importante ressaltar que não há qualquer mecanismo intrusivo. Todas as informações estão publicamente disponíveis e poderiam ser capturadas de maneira manual. A referida metodologia e o licenciamento livre, além de respeitarem a lei, permitem que a parte interessada possa reproduzir cada uma das etapas, garantindo, assim, o contraditório e a ampla defesa.

## Como contribuir?

* Clone o repositório. 
* Crie um virtualenv com Python 3.10.
* Ative o virtualenv. 
* Instale as dependências. 
* Rode `python manage.py migrate` para criar o banco de dados local.
* Rode `python manage.py runserver` para iniciar a aplicação.
* Execute os testes com `python manage.py test`.

##Autores 
Thiago Oliveira Castro Vieira e outros. 
Apoio da Comunidade Welcome to The Django 
