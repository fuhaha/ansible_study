# Ansible Configuration Management

Ansible 문서 참조 : <http://docs.ansible.com/ansible/>

작성자 : Ian Y. Choi
작성일 : Sep. 6, 2016

## Chapter 3 : Advaned Playbooks (플레이북 심화 내용)

### 복잡한 배포를 더욱 잘 수행하기 위한 방안들

* 병렬로 작업 실행
* 루핑
* 조건절 실행
* 태스크 위임
* 추가 변수
* 변수로 파일 찾기
* 환경 변수
* 외부 데이터 검색
* 결과 저장
* [2nd Edition] 데이터 처리
* 플레이북 디버그

### 병렬로 작업 실행

* 기본적으로 fork 개수는 최대 5개 까지
	* ansible.cfg 에서 "fork = 5" 를 변경할 수 있는 듯
* async 키워드: 병렬로 작업하도록 trigger하며 명령이 완료될 때까지 기다리는 값
* poll 키워드: 명령어가 완료되었는지 얼마나 자주 확인할 것인가?

~~~~
$ ansible-playbook -s codes/async.yml
~~~~

### 루핑

* (Peter 진행)

### 조건절 실행

* (Peter 진행)

### 태스크 위임

* Ansible이 동작하는 호스트 외 다른 곳에서 실행이 되어야 하는 경우 사용
* delegate_to 키워드를 사용
	* localhost 인 경우 local_action 으로 대체 가능

* delegate 를 쓰는 상황
	* 배포 전 로드밸런서에서 호스트 제거
	* 변경하려는 서버에서 트래픽을 제외하도록 DNS 변경
	* 저장 장치에 iSCSI 볼륨 생성
	* 네트워크 작업 바깥에 접근을 점검할 수 있게 외부 서버를 사용하기

### 추가 변수
* Ansible이 제공하는 변수
* hostvars
	* 현재 play 가 다루고 있는 모든 hosts를 가져오는 변수
	* hostvars와 다른 변수를 혼합해서 사용할 수 있다.
	* 예를 들어, 이름이 ns1 인 서버의 리눅스 배포판명을 가져오고 싶다면 ${hostvars.ns1.ansible_distribution}을 쓰면된다.
	* hostvars 를 쓰면, template 를 좀 더 추상화 할 수 있다.
	* 예) 머신 이름이 the_machine 이라는 변수에 있고, 이 머신의 ip주소를 가져오고 싶다면 {{hostvars.[the_machine].default_ipv4.address}} 라고 작성하면된다.
* groups
	* inventory group 에서 지정한 그룹에 속한 모든 hosts를 가져오는 변수.
	* groups 는 실제 hosts에 대한 내용을 가지진 않는다. 단지 inventory 에 있는 이름만 가지고 있다.
	* hostvars를 이용해서 해당 이름을 가진 host 정보를 가져올 수 있다.
* inventory_hostname
	* hostname 을 inventory 에 저장된 이름으로 사용하도록하는 변수
	* 이 host에 대해서는 setup module 을 실행하고 싶지 않거나, 다양한 이유에서 setup module 이 정상적이지 않을 경우 사용
* inventory_hostname_short
	* inventory_hostname 와 비슷하지만, 첫 번쨰 . 이전의 문자열만 포함한다.
	* 예를 들어, host.example.com 이 있다면, host 를 반환한다.
* inventory_dir
	* inventory 파일이 포함된 경로
* inventry_file
	* inventory_dir 과 비슷하지만, 파일명만 가져온다.

### 변수로 파일 찾기
* 변수를 이용해서 파일을 찾을 수 있다
* 변수의 값을 가져오려면 {{ }} 를 이용
* 예) copy: src=files/nrpe.{{ansible_architecture}}.conf
* first_available_file 을 이용하는 방법 [참고](https://github.com/fuhaha/ansible_study/blob/master/Chap3-ian/codes/filevariables.yml)

### 환경 변수
* unix command 를 실행하기 위한, 환경변수를 설정할 수 있음
* 예를 들어, aws shell 을 이용해서 AWS S3 에 파일을 업로드하고 싶다면 환경변수에 access / secret key 를 저장할 수 있다.
* 내부적으로 환경변수 설정을 위해 파이썬 코드를 사용하기에, 한 모듈에서 이미 환경변수를 설정했다면 다른 곳에서도 사용이 가능하다

### 외부 데이터 검색
* 버전 0.9 부터 lookup 플러그인 제공
* 직접 호출하거나, with_* keys 를 이용해서 실행 가능

### 결과 저장

### [2nd Edition] 데이터 처리

### 플레이북 디버그
