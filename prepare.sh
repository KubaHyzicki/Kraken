if [[ ! $(ls | grep venv) ]]; then
	python3 -m virtualenv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
else
	deactivate &> /dev/null
	source venv/bin/activate
fi
