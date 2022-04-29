# gcinside-Server

## Test Server Deploy Setting 
> ***현재 배포는 우분투를 사용하기 때문에 우분투 기준으로 작성 하겠습니다.***
- clone git repository
```shell
cd /srv
git clone -b develop https://github.com/gcinside/gcinside-Backend.git
```
- install python virtual environment
```shell
sudo apt-get install python3-venv
```
- apply python virtual environment 
```shell
source /srv/gcinside-Backend/bin/actiavate
```
- install mysql-devel ,pip3, etc for mysql-client
```shell
sudo apt-get install python3-pip python-dev python3-dev libmysqlclient-dev gcc 
```
- install requirement.txt using pip
```shell
pip3 install -r requirements.txt
```

