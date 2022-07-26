loadhost:
	scp Makefile ns@192.168.51.118:
	scp -r Alice/ ns@192.168.51.118:
	scp -r Bob/ ns@192.168.51.118:
	scp -r Root/ ns@192.168.51.118:
	scp -r Trudy/ ns@192.168.51.118:

loadcontainers:
	lxc file push Root/root.crt alice1/root/
	lxc file push Root/root.crt bob1/root/
	lxc file push Root/root.crt trudy1/root/
	lxc file push -r Alice/ alice1/root/
	lxc file push -r Bob/ bob1/root/
	lxc file push -r Trudy/ trudy1/root/
	lxc file push Alice/secure_chat_app.py alice1/root/secure_chat_app.py
	lxc file push Bob/secure_chat_app.py bob1/root/secure_chat_app.py
	lxc file push Trudy/secure_chat_interceptor.py trudy1/root/secure_chat_interceptor.py
	lxc file push Trudy/MITM_attack.py trudy1/root/MITM_attack.py
	lxc file push Trudy/downgrade_attack.py trudy1/root/downgrade_attack.py
	lxc file push Trudy/ARP_poisioning.py trudy1/root/ARP_poisioning.py
	lxc file push Makefile alice1/root/
	lxc file push Makefile bob1/root/
	lxc file push Makefile trudy1/root/

hostclean:
	rm -r Alice/
	rm -r Bob/
	rm -r Trudy/
	rm -r Root/
	rm Makefile 

aliceclean:
	rm -r Alice/
	rm root.crt
	rm secure_chat_app.py
	rm Makefile

bobclean:
	rm -r Bob/
	rm root.crt
	rm secure_chat_app.py
	rm Makefile

trudyclean:
	rm -r Trudy/
	rm root.crt
	rm secure_chat_interceptor.py
	rm MITM_attack.py
	rm downgrade_attack.py
	rm ARP_poisioning.py
	rm Makefile
