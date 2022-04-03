# Ansible modules for AWS Lightsail / модули для AWS Lightsail

Modules for interacting with the AWS Lightsail API<br>
The existing community.aws.lightsail module does not allow you to fully work with AWS Lightsail using Ansible, to be exact
manage the firewall, disks, static ip, etc., so I decided to write my own modules. <br>
A set of modules describing API Boto3 AWS Lightsail [link to documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html?highlight=lightsail#id437) <br>
Authorization through the standard AWS mechanism from the  [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

#### Manage:
  - Creating virtual machines
  - Starting, stoping, removing, rebooting and getting information about the virtual machine
  - Add static IP
  - Assign a static IP to the virtual machine
  - Unbind satic IP from virtual machine
  - Get IP information

#### Development plans:
Add firewall and virtual machine disk management
____________________________________________

Модули для взаимодействия с  AWS Lightsail API<br>
Имеющийся community.aws.lightsail модуль не дает полноценно работать с AWS Lightsail с помощью Ansible а точнее 
управлять фаерволом, дисками, статическим ip и т.п, поэтому решил написать свои модули.  <br>
Набор модулей описывающих API Boto3 AWS Lightsail [ссылка на документацию](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html?highlight=lightsail#id437) <br>
Авторизация через стандартный механизм AWS  из [документации](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

#### Умеет:
  - Создать виртульную машину 
  - Запустить, остановить, удалить, перезагрузить виртульную машину. А так же получить информацию о ней. 
  - Добавить статический IP
  - Присвоить статический IP виртуальной машине 
  - Отвязать сатический IP от виртуальной машины
  - Получить информации об IP

#### Планы по развитию: 
Добавить управление фаерволом и дисками виртульной машины

_____________________________________________
## Example \ Пример: 
      - name: Allocate static ip
        lightsail.ip:
          name: ipname 
          state:  new
          
      - name: Create VM
        lightsail.vm:
          name: vmname 
          state: new
          ip_type: ipv4
          blueprint_id: ubuntu_20_04
          bundle_id: small_2_0
          key_pair_name: my_open_key
          region: eu-central-1
          zone: eu-central-1a
        register: ubnt

      - name: delete VM
        lightsail.vm:
          name: vmname 
          state: delete


