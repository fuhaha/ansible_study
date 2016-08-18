# Ansible Configuration Management
Ansible 문서 참조 : <http://docs.ansible.com/ansible/>

작상자 : 전성욱(codetree@gmail.com)
작성일 : 20160816

## Chapter 2 : Simple Playbooks

### PlayBook 
* 한번에 하나이상의 작업을 수행하는 기능을 제공
* YAML file 형식을 사용한다. (<http://www.yaml.org/>,  <http://docs.ansible.com/ansible/YAMLSyntax.html>)
* 하나의 커멘드에서 다른 커멘드로 상태를 전달 할 수 있음 (변수활용)
* 멱등성(idempotence) 보장하기위해 노력한다.
	(** 멱등성(idempotence): 연산을 여러 번 적용하더라도 결과가 달라지지 않는 성질을 의미한다)
* command-line의 옵션을 Playbook Target Part에서 사용 가능 (EX : -k, -K)

~~~~
$ ansible-playbook example-play.yml
~~~~

### PlayBook Sections
* Target section (Hosts and Users) : 대상장비와 SSH사용자 관련 설정 
* Variable Section : PlayBook 사용할 변수를 정의 한다.
* Task Section : Ansible을 이용하여 실행할 모듈을 순서대로 열거한다.
* Handlers section : Task 수행 결과 무언가 변경이 발생 하였을 때 "notify"에 기술한 Handler가 호출된다.

~~~~
---
- hosts: webservers
  user: root
  vars:
	apache_version: 2.6
	motd_warning: 'WARNING: Use by ACME Employees ONLY'
	testserver: yes
  tasks:
	- name: setup a MOTD
	  copy:
	    dest: /etc/motd
	    content: "{{ motd_warning }}"		
또는 
	  copy: dest=/etc/motd content="{{ motd_warning }}"
~~~~

### The target section
대상장비와 접속사용자(SSH 사용자), 실행사용자(SUDO 사용자) 관련 설정을 한다.
~~~~
- hosts: webservers
  user: root
~~~~

* 줄의 처음은 "-"로 시작한다.
* hosts : Play가 실행될 대상 장비 설정
	* 정규식 (group name, a machine name, a glob, and a tilde (~),*(all)) 
* user : 대상장비에 연결할 사용자 계정

| 이름 | 설명 |
|-----|-----|
| sudo | 플레이에서 장비로 연결 이후 sudo를 이용한 root계정 수행을 원할 경우 yes |
| user | 대상장비 접속을 위한 사용자 계정 |
| sudo_user | sudo 처리를 위한 사용자 계정 |
| connection | 대상장비 접속 방법 : local 이나 ssh |
| gather_facts | setup module 자동 실행여부, (default :  setup module 실행) |

  * 아니다:no,false,off,0
  * 맞다:yes,true,on,1
### The variable section
모든 장비에서 사용되면 전체 Play에 적용할 모든 설정을 변수 정의

* 유지보수를 쉬운 Play를 만들수 있다
* play의 여러부분에서 동일한 변수의 변경을 막는다
* 변수 제공 방법 :
	* command-line
	* ansible prompt

* 변수는 Module 에의해 설정된 machine facts에 의해 변경될 수 있다

* vars : 변수 목록 정의
~~~~
vars:
	apache_version: 2.6
	motd_warning: 'WARNING: Use by ACME Employees ONLY'
	testserver: yes
~~~~

* vars_files : 변수로 load될 외부 YAML files 나열
~~~~
vars_files:
	conf/country-AU.yml
	conf/datacenter-SYD.yml
	conf/cluster-mysql.yml
~~~~

* 외부 YAML file 예제 (country-AU.yml와 같은...)
~~~~
---
ntp: ntp1.au.example.com
TZ: Australia/Sydney
~~~~

* vars_prompt: 변수를 사용자에게 입력받을 경우  
~~~~
vars_prompt:
  - name: https_passphrase
    prompt: Key Passphrase
    private: yes
~~~~

	* name: 변수명
	* prompt: 프람프트 앞에 표시
	* private: 입력내용 화면 표시 여부 (yes:표시하지 않음)

* 변수를 사용할때 표현방식
	* {{ variablename }}
	* {{ httpd.maxclients }} : httpd변수가 maxclients라는 key를 갖고 있는 경우
	* {{ ansible_eth0.ipv4.address }} : setup  module의 사용시 fact로부터 eth0의 ipv4 주소값 얻을 경우

* 변수부분에 설정된 변수는 같은 Playbook내에 서로 다른 play사이에서는 살아있지 않는다.
* setup module에 의해 수집된 fact 또는 set_fact에 의해 설정된 fact는 서로 다른 play사이에서는 살아있다. 
* gather_facts를 false로 하면 속도를 극적으로 빨라질 수도 있다. (자동으로 setup module을 실행하지 않으니까.)
* facts라는 것은 시스템 환경변수를 말한다.

### The task section
수행되기를 원하는 순서대로 Ansible이 수행할 action 목록을 포함한다.

* 기능이 많은 하나의 module을 사용할는 것을 피하는 것이 좋다. 
* CentOS장비에 Apache 설치,설정,시작을 위한 예제

~~~~
tasks:
  - name: install apache
    action: yum name=httpd state=installed

  - name: configure apache
    copy: src=files/httpd.conf dest=/etc/httpd/conf/httpd.conf

  - name: restart apache
    service:
      name: httpd
      state: restarted
~~~~
* 예제에서 "action", "copy", "service"가 module이름이다.
* module에 인수를 제공하는 2가지 방식

~~~~
tasks:
  - name: configure apache
(1) copy:
	  src: files/httpd.conf
	  dest: /etc/httpd/conf/httpd.conf	
또는 
(2)	copy: src=files/httpd.conf dest=/etc/httpd/conf/httpd.conf
~~~~

* 복잡한 양식의 인수를 전달할 경우 (1)과 같이 하는 것이 좋다.

* task에서 name을 사용하지 않을 수 있다 (권장하지 않음)
* ansible은 실행시 console에 어떤일이 일어났는지 보여준다. 이때 name을 사용한다.
* name이 없으면 ansible은 task와 handle부분의 action이 있는 줄을 출력한다.

### The handlers section
Task 수행 결과 무언가 변경이 발생 하였을 때 "notify"에 기술한 Handler가 호출된다.

* task의 리스트의 실행이 종료되면 triggered된 handler가 실행된다.
* task부분에서 여러번 실행해도 handle은 한번만 실행한다.
* handler는 업그레이드 나 설정변경 후 service(daemon)재시작 할경우 사용한다.

* ISC DHCP 서버를 최신버전으로 update하고 설정하고 재시작하는 예제:

~~~~
---
- hosts: dhcp
  tasks:

- name: update to latest DHCP
  yum:
    name: dhcp
    state: latest
  notify: restart dhcp

- name: copy the DHCP config
  copy:
    src: dhcp/dhcpd.conf
    dest: /etc/dhcp/dhcpd.conf
  notify: restart dhcp

- name: start DHCP at boot
  service:
    name: dhcpd
    state: started
    enabled: yes

handlers:
- name: restart dhcp
  service:
    name: dhcpd
    state: restarted
~~~~

* 하나의 task에서 여러개의 handler를 사용할 수 있다.
* Django 응용프로그램의 새버전을 checkout하는 경우 DB migration, static file 배포, apache 재시작 예제:

~~~~
---
- hosts: qroud
  tasks:
  - name: checkout Qroud
    git:
      repo: git@github.com:smarthall/Qroud.git
      dest: /opt/apps/Qroud force=no
    notify:
      - migrate db
      - generate static
      - restart httpd

  handlers:
  - name: migrate db
    command: ./manage.py migrate –all
      args:
      chdir: /opt/apps/Qroud

  - name: generate static
    command: ./manage.py collectstatic -c –noinput
    args:
      chdir: /opt/apps/Qroud

  - name: restart httpd
    service:
      name: httpd
      state: restarted
~~~~ 

### The playbook modules
playbook module은 command-line에서 module과 차이가 있다.

* setup module에서 많은 fact를 갖고 있다. (playbook 실행시 자동실행)
* 어떤 모듈은 변수를 사용하므로 command-line을 지원하지 않는다. (나중에 조사)
* 어떤 모듈은 command-line에서 동작하나 playbook에서 확장 기능을 제공한다. (나중에 조사)

#### The template module
설정 파일의 개요를 디자인할 수 있고 적절한 위치에 값을 입력할 수 있다.

* Jinja2 template은 훨씬 복잡한 조건절, for loop, macro등을 포함할 수 있다.
* BIND configuration을 위한 Jinja2 configuration template 예제:

~~~~
# {{ ansible_managed }}    <-- 해당 파일,장비,template의 수정시간과 사용자가 
                               어떤 template에서 왔는지 보여주는 주석을 설치
options {
  listen-on port 53 {
    127.0.0.1;
    {% for ip in ansible_all_ipv4_addresses %} <-- setup module인 fact ip List를 나열
      {{ ip }};
    {% endfor %}
  };
  listen-on-v6 port 53 { ::1; };
  directory "/var/named";
  dump-file "/var/named/data/cache_dump.db";
  statistics-file "/var/named/data/named_stats.txt";
  memstatistics-file "/var/named/data/named_mem_stats.txt";
};

zone "." IN {
  type hint;
  file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

{# Variables for zone config #}    <--  주석
{% if 'authorativenames' in group_names %}  <-- 조건절
  {% set zone_type = 'master' %}
  {% set zone_dir = 'data' %}
{% else %}
  {% set zone_type = 'slave' %}
  {% set zone_dir = 'slaves' %}
{% endif %}

zone "internal.example.com" IN {
  type {{ zone_type }};
  file "{{ zone_dir }}/internal.example.com";
  {% if 'authorativenames' not in group_names %} <-- 조건절
    masters { 192.168.2.2; };
  {% endif %}
};
~~~~

* template module 사용하기

~~~~
---
- name: Setup BIND
  host: allnames

  tasks:
  - name: configure BIND
    template: src=templates/named.conf.j2 dest=/etc/named.conf owner=root group=named mode=0640
~~~~

#### The set_fact module


#### The pause module

#### The wait_for module

#### The assemble module

#### The add_host module

#### The group_by module

#### The slurp module

#### Windows playbook modules

#### Cloud Infrastructure modules

#### The AWS modules

----
## Ansible Modules

* Bmc Modules : Boot devices, Power management
* Cloud Modules : Amazon AWS관련 모듈 
* Clustering Modules : Clustering관련 모듈
* Commands Modules : Execute command
* Database Modules : Database관련 Module 
    * Influxdb,mongodb,redis,riak,mssql,mysql,Postgresql,Vertica
* Files Modules : File Management Module
* Inventory Modules
* Messaging Modules : rabbitmq관리 module
* Monitoring Modules
* Network Modules
* Notification Modules
* Packaging Modules
* Source Control Modules
* System Modules
* Utilities Modules
* Web Infrastructure Modules
* Windows Modules