
PASSO A PASSO PARA INSTALAR AS DEPENDÊNCIAS DO SCRIPT

✅ 1. Verifique se o Python está instalado
--------------------------------------------------
Abra o terminal e digite:
    python --version

Você deve ver algo como:
    Python 3.x.x

Se não estiver instalado, baixe aqui:
    https://www.python.org/downloads/


✅ 2. (Opcional) Crie um ambiente virtual
--------------------------------------------------
Recomendado para evitar conflitos com outras bibliotecas:

    python -m venv venv

Ative o ambiente virtual:

No Windows:
    venv\Scripts\activate

No Linux/macOS:
    source venv/bin/activate


✅ 3. Instale as dependências
--------------------------------------------------
Digite no terminal:

    pip install yfinance pandas pytz


✅ 4. (Opcional) Verifique se tudo foi instalado corretamente
--------------------------------------------------
    pip list

Verifique se aparecem:
    - yfinance
    - pandas
    - pytz


✅ 5. Execute seu script Python
--------------------------------------------------
Salve o código em um arquivo, por exemplo:
    analise_fibonacci.py

E execute com:
    python analise_fibonacci.py


✅ Pronto! Agora o script está pronto para rodar.
