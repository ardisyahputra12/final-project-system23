# Final Project - System23
Backend repository for System23


## IP
34.142.211.35


## Notes
- For testing project is work temporary: Run docker compose (use Makefile), then hit api with endpoint /image (in file universal.py). ex. 34.142.211.35:5000/image
- Table for database is not yet fix (in file utils.py)


## Connect to local with ssh (Windows/WSL)
- cd .ssh
- ssh-keygen -t rsa -f <FILENAME> -C <USERNAME> -b 2048
- type <FILENAME>.pub
- copy public key to GCP and add in security section
- finally you can connect via ssh using vs code 

Test connect in cmd:
- ssh <USERNAME>@34.142.211.35 -i <FILENAME>

Test IP, run command:
- make build
- curl 34.142.211.35:5000/image