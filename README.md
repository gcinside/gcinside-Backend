# gcinside-Server

## Test Server Deploy Setting 
> ***현재 배포는 우분투를 사용하기 때문에 우분투 기준으로 작성 하겠습니다.***
### python & python environment install
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

> test server status

```shell
python3 manage.py runserver 0.0.0.0:8000
```
0.0.0.0:8000 을 붙혀주는 이유는 붙혀주지 않는다면 local 에서 밖에 작동하지 않음

- open security group port 8000
  - AWS 혹은 다른 클라우드 공급자 의 서버 보안그룹을 8000 포트로 뚫어줍니다.

- goto chrome & insert << your aws ec2 instance url >>:8000
![스크린샷 2022-04-30 오전 1 40 15](https://user-images.githubusercontent.com/69895368/165987538-3e5b318d-a0c4-405b-8e6a-13441f4cf20f.jpg)


