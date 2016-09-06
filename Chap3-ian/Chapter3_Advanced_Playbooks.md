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

### 변수로 파일 찾기

### 환경 변수

### 외부 데이터 검색

### 결과 저장

### [2nd Edition] 데이터 처리

### 플레이북 디버그
