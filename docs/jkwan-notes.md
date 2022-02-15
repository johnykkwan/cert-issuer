Testnet 
Address: mxiScB8Kc2j34PhrP5oVkBsKAvepAPPzD2
PK: cUmisFWNNbcsnK39VDf7a7LUeCexedUwMwCWqvvDKqzvn5Zfv9gS

docker build -t jk/cert-issuer-v2 .
docker run -it jk/cert-issuer-v2 bash

apk add --update vim

=========== config.ini =======================
issuing_address = mxiScB8Kc2j34PhrP5oVkBsKAvepAPPzD2

chain=bitcoin_testnet
####  bitcoind

usb_name=/etc/cert-issuer/
key_file=pk_issuer.txt

unsigned_certificates_dir=/etc/cert-issuer/data/unsigned_certificates
blockchain_certificates_dir=/etc/cert-issuer/data/blockchain_certificates
work_dir=/etc/cert-issuer/work

no_safe_mode

============== pk_issuer.txt
cUmisFWNNbcsnK39VDf7a7LUeCexedUwMwCWqvvDKqzvn5Zfv9gS


docker ps -l
docker commit <container for your bc/cert-issuer> my_cert_issuer

docker ps  // shows the docker containerId
docker cp <containerId>:/etc/cert-issuer/data/blockchain_certificates <localPath>/cert-viewer/cert_data

cert-issuer> docker cp 67ceea7688c4:/etc/cert-issuer/data/blockchain_certificates .\data

curl -H "origin: example.com" -v "https://tokenindo.com/blockcerts/issuer.json"


cert-issuer.exe -c .\conf_issuer_binus.ini


resolution for ssl or libeay32 error ================

 File "C:\vscode\cert-issuer\venv\lib\site-packages\bitcoin\rpc.py", line 48, in <module>
    from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
  File "C:\vscode\cert-issuer\venv\lib\site-packages\bitcoin\wallet.py", line 33, in <module>
    import bitcoin.core.key
  File "C:\vscode\cert-issuer\venv\lib\site-packages\bitcoin\core\key.py", line 34, in <module>
    _ssl = ctypes.cdll.LoadLibrary(ctypes.util.find_library('ssl') or 'libeay32')
  File "c:\users\jkwan\appdata\local\programs\python\python38-32\lib\ctypes\__init__.py", line 451, in LoadLibrary
    return self._dlltype(name)
  File "c:\users\jkwan\appdata\local\programs\python\python38-32\lib\ctypes\__init__.py", line 373, in __init__
    self._handle = _dlopen(self._name, mode)
FileNotFoundError: Could not find module 'libeay32' (or one of its dependencies). Try using the full path with constructor syntax.


Install https://slproweb.com/products/Win32OpenSSL.html
Change "C:\vscode\cert-issuer\venv\lib\site-packages\bitcoin\core\key.py", line 34 to

#_ssl = ctypes.cdll.LoadLibrary(ctypes.util.find_library('ssl') or 'libeay32')
_ssl = ctypes.cdll.LoadLibrary(ctypes.util.find_library('libeay32'))

## create pypi distribution
python setup.py sdist

## pip install from local folder
pip install ..\cert-core\dist\cert-core-2.1.11.tar.gz 


## setup local dependency
python setup.py install

## install current state
pip install . 
