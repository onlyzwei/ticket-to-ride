# Como Rodar o Projeto
1. Verifique o Go
   - No terminal, rode:
     
    $ go version
     
   - O comando deve retornar a versão do Go instalada tipo assim:
     
     go version go1.xx.x .....
     
   Caso o Go não esteja instalado, baixe e instale-o pelo site https://go.dev/doc/install

   !!Você tem que mover o go para path nas variaveis de ambiente!!!!!

2. Executar o Projeto
   - Comando:
     
     $ go run main.go
     
   - Isso fará o projeto iniciar, resolvendo as dependencias automaticamente

    E voce deve rodar o Index.hmtl separadamente!!!! Pode ser com liveserver do vscode
    [Link LiveServer extensão](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
    Só clicar com botão direito no index.html e gg "go live"

3. CASO fique alguma dependencia ainda
    - Rode:

    $ go mod tidy

4. Recomendo baixar alguma extensão para Go no vscode 
[GO - Extensão](https://marketplace.visualstudio.com/items?itemName=golang.Go)
