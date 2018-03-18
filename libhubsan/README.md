# LibHubsan

A library for controlling a Hubsan X4 (Model H107*) via an Arduino Due with an A7105.

Forked from [https://github.com/NotionalLabs/libHubsan](https://github.com/NotionalLabs/libHubsan)

See the blog series that helped create the library here:

- [Part 1](http://www.jimhung.co.uk/?p=1349)
- [Part 2](http://www.jimhung.co.uk/?p=1424)
- [Part 3](http://www.jimhung.co.uk/?p=1638)
- [Part 4](http://www.jimhung.co.uk/?p=1704)


## Running the Python Controller

To run the python controller you should first install virtualenv (`sudo apt install python-virtualenv`). Once you have installed the virtualenvironment tool, run the following

```
cd controller
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

This will install all of the necessary requirements to the virtualenv so that it doesn't interefere with system python packages. Once installed and the arduino controller is connected to the PC, you can run the `pyHubsan.py` script.

```
python pyHubsan.py
```